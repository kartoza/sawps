"""Common functions for parcel."""
from django.contrib.gis.geos import GEOSGeometry
from frontend.models.parcels import (
    Erf,
    Holding,
    FarmPortion,
    ParentFarm
)


def find_layer_by_cname(cname: str):
    """Find layer name+id by cname."""
    obj = Erf.objects.filter(cname=cname).first()
    if obj:
        return 'erf', obj.id
    obj = Holding.objects.filter(cname=cname).first()
    if obj:
        return 'holding', obj.id
    obj = FarmPortion.objects.filter(cname=cname).first()
    if obj:
        return 'farm_portion', obj.id
    obj = ParentFarm.objects.filter(cname=cname).first()
    if obj:
        return 'parent_farm', obj.id
    return None, None


def find_parcel_base(cls, serialize_cls,
                     other: GEOSGeometry, parcel_keys=[]):
    """Base function to find parcel."""
    parcels = cls.objects.filter(geom__within=other)
    if parcel_keys:
        parcels = parcels.exclude(
            cname__in=parcel_keys
        )
    if parcels:
        results = serialize_cls(
            parcels,
            many=True
        ).data
        return results, [a['cname'] for a in results]
    return [], []
