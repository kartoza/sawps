from typing import List
import logging
from celery import shared_task
from django.db import connection
from django.db.models import Q
from django.utils import timezone
from area import area
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon
from property.models import PropertyOverlaps


logger = logging.getLogger(__name__)


class OverlapItem(object):

    def __init__(self, property_id, other_id, intersect_geom) -> None:
        self.property_id = property_id
        self.other_id = other_id
        if isinstance(intersect_geom, Polygon):
            self.intersect_geom = MultiPolygon([intersect_geom], srid=4326)
        else:
            self.intersect_geom = intersect_geom
        self.overlap_area_size = area(intersect_geom.geojson)

    def get_queryset(self):
        return PropertyOverlaps.objects.filter(
            Q(
                property_id=self.property_id,
                other_id=self.other_id
            ) | Q(
                property_id=self.other_id,
                other_id=self.property_id
            )
        )

    def is_new(self):
        qs = self.get_queryset()
        return not qs.exists()

    def get_existing(self):
        qs = self.get_queryset()
        return qs.first()

    def store(self, existing: PropertyOverlaps = None):
        if existing:
            existing.reported_at = timezone.now()
            existing.overlap_geom = self.intersect_geom
            existing.overlap_area_size = self.overlap_area_size
            existing.resolved = False
            existing.resolved_at = None
            existing.save()
            return existing
        return PropertyOverlaps.objects.create(
            property_id=self.property_id,
            other_id=self.other_id,
            reported_at=timezone.now(),
            overlap_geom=self.intersect_geom,
            overlap_area_size=self.overlap_area_size
        )


def check_overlaps_in_properties() -> List[OverlapItem]:
    """
    Check overlapping properties by using ST_Overlaps.

    :return: List of OverlapItem
    """
    sql = (
        """
        select a.id as prop_id, b.id as other_id,
            st_intersection(a.geometry, b.geometry) as intersects
        from property a, property b
        where a.id < b.id and st_overlaps(a.geometry, b.geometry);
        """
    )
    results: List[OverlapItem] = []
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            geom = GEOSGeometry(row[2])
            results.append(OverlapItem(row[0], row[1], geom))
    return results


def check_for_resolved_overlaps(overlap_data: List[OverlapItem]) -> int:
    """
    Check for pending overlap record and mark it as resolved
    if the record is not in overlap_data.

    :param overlap_data: List of OverlapItem
    :return: number of resolved records
    """
    num_of_resolved = 0
    existing_overlaps = PropertyOverlaps.objects.filter(
        resolved=False
    ).order_by('reported_at')
    for overlap in existing_overlaps.iterator(chunk_size=1):
        is_not_resolved = len(
            [a for a in overlap_data if
             (a.property_id == overlap.property.id and
              a.other_id == overlap.other.id) or
             (a.property_id == overlap.other.id and
              a.other_id == overlap.property.id)
             ]
        ) > 0
        if not is_not_resolved:
            num_of_resolved += 1
            overlap.resolved = True
            overlap.resolved_at = timezone.now()
            overlap.save(update_fields=['resolved', 'resolved_at'])
    return num_of_resolved


@shared_task(name='property_check_overlaps_each_other')
def property_check_overlaps_each_other():
    logger.info('Checking overlapping properties...')
    results = check_overlaps_in_properties()
    logger.info(f'Overlapping properties result size {len(results)}')
    new_overlap = 0
    for result in results:
        if result.is_new():
            result.store()
            new_overlap += 1
        else:
            existing = result.get_existing()
            if not existing:
                continue
            if existing.resolved:
                result.store(existing)
    resolved = check_for_resolved_overlaps(results)
    return (new_overlap, resolved)
