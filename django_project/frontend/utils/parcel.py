"""Common functions for parcel."""
from area import area
from django.db import connection
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Centroid
from frontend.models.parcels import (
    Erf,
    Holding,
    FarmPortion,
    ParentFarm
)
from property.models import Province


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


def select_parcel_by_centroid(parcels, other: GEOSGeometry):
    """Select parcel by using its centroid."""
    selected_parcels = []
    cnames = []
    if other.num_geom > 1:
        # if multipart, then search for each polygon
        for i in range(other.num_geom):
            geom_part = other[i]
            for parcel in parcels:
                centroid = parcel.centroid
                if centroid.within(geom_part) and parcel.cname not in cnames:
                    selected_parcels.append(parcel)
                    cnames.append(parcel.cname)
    else:
        for parcel in parcels:
            centroid = parcel.centroid
            if centroid.within(other) and parcel.cname not in cnames:
                selected_parcels.append(parcel)
                cnames.append(parcel.cname)
    return selected_parcels, cnames


def find_parcel_base(cls, serialize_cls,
                     other: GEOSGeometry):
    """Base function to find parcel."""
    results = []
    cname_list = []
    parcels = cls.objects.filter(geom__bboverlaps=other)
    parcels = parcels.annotate(
        centroid=Centroid('geom')).order_by('cname').distinct('cname')
    if parcels.exists():
        selected_parcels, cname_list = select_parcel_by_centroid(
            parcels, other)
        if selected_parcels:
            results = serialize_cls(
                selected_parcels,
                many=True
            ).data
    return results, cname_list


def find_province(geom: GEOSGeometry, default: Province):
    """
    Find province for given geometry (SRID 3857).

    :param geom: Geometry
    :param default: Default Province if no result
    :return: Province that has biggest overlap with geom
    """
    query = (
        """
        with input_geom as (select ST_GeomFromText(%s, 3857) as geom)
        select zpss.adm1_en as name,
        ST_AREA(ST_Intersection(ig.geom, zpss.geom)) / ST_AREA(zpss.geom)
        as overlap
        from layer.zaf_provinces_small_scale zpss
        inner join input_geom ig on ST_Intersects(ig.geom, zpss.geom)
        order by overlap desc limit 1
        """
    )
    query_values = [geom.ewkt]
    province_name = None
    with connection.cursor() as cursor:
        cursor.execute(query, query_values)
        row = cursor.fetchone()
        if row:
            province_name = row[0]
    if province_name is None:
        return default
    province = Province.objects.filter(
        name=province_name
    ).first()
    return province if province else default


def get_geom_size_in_ha(geom: GEOSGeometry):
    """
    Calculate geometry size in ha.

    :param geom: Geometry
    :return: Size in ha
    """
    if geom is None:
        return 0
    meters_sq = area(geom.geojson)
    acres = meters_sq * 0.000247105381  # meters^2 to acres
    return acres / 2.471
