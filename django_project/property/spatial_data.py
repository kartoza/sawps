from typing import Dict, List, Tuple, AnyStr

from django.db import connection
from django.db.utils import InternalError

from frontend.models.spatial import SpatialDataModel, SpatialDataValueModel
from property.models import Property
from frontend.models import ContextLayer, Layer

TABLE_SCHEMA = 'layer'
NO_VALUE = '-'
GEOMETRY_KEY = 'geometry'


class ColumnInfo:
    def __init__(self, column_name: AnyStr, data_type: AnyStr, srid: AnyStr):
        self.column_name = column_name
        self.data_type = data_type
        self.srid = srid


def get_distinct_srids(table_name: str) -> List:
    """
    Retrieve distinct SRIDs from the specified table's geometry column.

    :param table_name: Name of the table to check.

    :return: A list of distinct SRIDs.
    """
    query = (
        f"SELECT DISTINCT ST_SRID(geom) AS srid "
        f"FROM {TABLE_SCHEMA}.{table_name};"
    )

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    return [row[0] for row in rows if row[0] is not None]


def columns_and_srid(table_name: AnyStr) -> Tuple[List[ColumnInfo], AnyStr]:
    """
    Retrieve all column names along with their SRID (if applicable)
    for a given table in the database schema "layer".

    :param table_name: Table name for which column information is required.

    :return: Tuple[list[ColumnInfo], str]: A tuple containing two elements:
            1. A list of ColumnInfo objects detailing each column.
            2. A string representing the SRID of a geometry column, if present;
               returns an empty string if no geometry column is found.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                col.column_name,
                col.data_type,
                COALESCE(geom.srid::text, %s) AS srid
            FROM information_schema.columns col
            LEFT JOIN geometry_columns geom
                ON col.table_schema = geom.f_table_schema
                AND col.table_name = geom.f_table_name
                AND col.column_name = geom.f_geometry_column
            WHERE col.table_schema = %s
            AND col.table_name = %s;
        """, [NO_VALUE, TABLE_SCHEMA, table_name])

        rows = cursor.fetchall()

        columns = [ColumnInfo(
            row[0],
            row[1] if row[2] == NO_VALUE else GEOMETRY_KEY,
            row[2]
        )
            for row in rows
        ]
        srid = ''
        for column in columns:
            if column.srid != NO_VALUE:
                srid = column.srid

        if srid == "0":  # could not get srid information from table
            srids = get_distinct_srids(table_name)
            if len(srids) > 0:
                srid = srids[0]
            else:
                srid = ''

        return columns, srid


def extract_spatial_data_from_property_and_layer(
        target_property: Property,
        context_layer: ContextLayer
) -> Dict:
    """
    Intersect a target property with a given context layer to
    extract spatial data.

    :param target_property: The property object that needs to be intersected.
    :type target_property: Property

    :param context_layer: The layer that provides contextual spatial data.
    :type context_layer: ContextLayer

    :return: The spatial data extracted from the intersection of the target
    property and context layer.
    Returns an empty dictionary if no spatial data is found.
    """
    if not target_property.geometry:
        return {}

    spatial_data = {}

    for layer in (
            context_layer.layer_set.filter(
                spatial_filter_field__isnull=False
            ).exclude(spatial_filter_field='')):
        layer_name = layer.name
        columns, srid = columns_and_srid(layer_name)

        if not srid:  # Table with geometry not found, continue
            continue

        column_names = [
            col.column_name for col in columns if col.srid == NO_VALUE
        ]

        query = f"""
            SELECT {'e.' + ',e.'.join(column_names)}
            FROM layer.{layer_name} e
                JOIN public.property p ON ST_Intersects(
                e.geom, ST_Transform(p.geometry, {int(srid)}))
            WHERE p.id = %s;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, [target_property.id])
                rows = cursor.fetchall()

                spatial_data_values = []

            for row in rows:
                row_dict = dict(zip(column_names, row))
                spatial_data_values.append(row_dict)

                spatial_data[layer_name] = spatial_data_values
        except InternalError as e:
            print(e)

    return spatial_data


def save_spatial_values_from_property_layers(target_property: Property):
    """
    Extract spatial data from the given property for all context layers
    and save the extracted values to SpatialDataModel.

    :param target_property: The property object to be extracted
    :type target_property: Property
    """
    context_layers = ContextLayer.objects.filter(
        layer__spatial_filter_field__isnull=False
    ).distinct()

    layers = {layer.name: layer for layer in Layer.objects.all()}

    for context_layer in context_layers:
        spatial_data_by_layers = extract_spatial_data_from_property_and_layer(
            target_property,
            context_layer
        )
        if not spatial_data_by_layers:
            continue

        spatial_data_obj, _ = SpatialDataModel.objects.get_or_create(
            property=target_property,
            context_layer=context_layer
        )

        for layer_name, spatial_layer_data in spatial_data_by_layers.items():
            layer = layers.get(layer_name)
            if layer is None:
                continue

            for spatial_layer_value in spatial_layer_data:
                filter_field = layer.spatial_filter_field
                if filter_field not in spatial_layer_value:
                    continue
                SpatialDataValueModel.objects.update_or_create(
                    layer=layer,
                    spatial_data=spatial_data_obj,
                    context_layer_value=(
                        spatial_layer_value[filter_field]
                    )
                )
