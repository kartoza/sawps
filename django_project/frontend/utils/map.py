"""Helper function for map."""
import os
import json
import time
import ast
import math
from enum import Enum
from django.db import connection
from django.contrib.sites.models import Site
from django.conf import settings
from django.urls import reverse
from core.settings.utils import absolute_path
from species.models import Taxon
from frontend.utils.color import linear_gradient


# number of breaks to generate stops for color gradient of population count
CHOROPLETH_NUMBER_OF_BREAKS = 5
DEFAULT_BASE_COLOR = '#FF5252'


class PopulationQueryEnum(Enum):
    PROVINCE_LAYER = 'Province Layer'
    PROPERTIES_LAYER = 'Properties Layer'
    PROPERTIES_POINTS_LAYER = 'Properties Points Layer'
    SUMMARY_COUNT = 'SUMMARY COUNT'


def get_map_template_style(request, theme_choice: int = 0, token: str = None):
    """
    Fetch map template style from file.

    :param theme_choice: 0 light, 1 dark
    :return: json map style
    """
    load_normal_map = True
    if hasattr(request.user, 'user_profile'):
        user_role = str(
            request.user.user_profile.user_role_type_id
        )
        if "Decision Maker" in user_role:
            style_file_path = absolute_path(
                'frontend', 'utils', 'country_level_light_v2.json'
            )
            if theme_choice == 1:
                style_file_path = absolute_path(
                    'frontend', 'utils', 'country_level_dark_v2.json'
                )
            load_normal_map = False
    if load_normal_map:
        style_file_path = absolute_path(
            'frontend', 'utils', 'sanbi_styling_light.json'
        )
        if theme_choice == 1:
            style_file_path = absolute_path(
                'frontend', 'utils', 'sanbi_styling_dark.json'
            )
    styles = {}
    with open(style_file_path) as config_file:
        styles = json.load(config_file)
    # update sanbi source URL
    schema = 'https://'
    domain = Site.objects.get_current().domain
    if settings.DEBUG:
        schema = 'http://'
        tegola_dev_port = os.environ.get('TEGOLA_DEV_PORT', '9191')
        domain = f'localhost:{tegola_dev_port}'
    elif 'localhost' in domain:
        schema = 'http://'
    if 'sources' in styles and 'sanbi' in styles['sources']:
        tile_url = f'{schema}{domain}/maps/sanbi/{{z}}/{{x}}/{{y}}'
        if settings.DEBUG:
            tile_url = tile_url + '.pbf'
        if not settings.DEBUG and token:
            tile_url = tile_url + f'?token={token}'
        styles['sources']['sanbi']['tiles'] = [tile_url]
    if 'sources' in styles and 'NGI Aerial Imagery' in styles['sources']:
        url = (
            reverse('aerial-map-layer', kwargs={
                'z': 0,
                'x': 0,
                'y': 0
            })
        )
        url = request.build_absolute_uri(url)
        url = url.replace('/0/0/0', '/{z}/{x}/{y}')
        if not settings.DEBUG:
            # if not dev env, then replace with https
            url = url.replace('http://', schema)
        styles['sources']['NGI Aerial Imagery']['tiles'] = [url]
    # add properties layer
    if 'sources' in styles:
        url = (
            reverse('properties-map-layer', kwargs={
                'z': 0,
                'x': 0,
                'y': 0
            })
        )
        url = request.build_absolute_uri(url)
        url = url.replace('/0/0/0', '/{z}/{x}/{y}')
        if not settings.DEBUG:
            # if not dev env, then replace with https
            url = url.replace('http://', schema)
        # add epoch datetime
        url = url + f'?t={int(time.time())}'
        # TODO: add query params if there is species filter
        styles['sources']['sanbi-dynamic'] = {
            "type": "vector",
            "tiles": [url],
            "minzoom": 5,
            "maxzoom": 24
        }
        styles['layers'].append(get_highlighted_layer('erf'))
        styles['layers'].append(get_highlighted_layer('holding'))
        styles['layers'].append(get_highlighted_layer('farm_portion'))
        styles['layers'].append(get_highlighted_layer('parent_farm'))
    # update maptiler api key
    styles = replace_maptiler_api_key(styles)
    return styles


def replace_maptiler_api_key(styles):
    """Replace maptiler_key."""
    map_tiler_key = settings.MAPTILER_API_KEY
    if 'glyphs' in styles and styles['glyphs']:
        styles['glyphs'] = styles['glyphs'].replace(
            '{{MAPTILER_API_KEY}}',
            map_tiler_key
        )
    return styles


def get_highlighted_layer(layer_name):
    # green
    return {
        "id": f"{layer_name}-highlighted",
        "type": "line",
        "source": "sanbi",
        "source-layer": f"{layer_name}",
        "minzoom": 12,
        "layout": {"visibility": "visible", "line-join": "bevel"},
        "paint": {
            "line-color": "#ffffff",
            "line-width": [
                "case",
                [
                    "boolean",
                    ["feature-state", "parcel-selected-highlighted"],
                    False
                ],
                4,
                0
            ],
            "line-opacity": 1
        }
    }


def get_query_condition(
        organisation_id: int,
        filter_start_year: int,
        filter_end_year: int,
        filter_species_name: str,
        filter_organisation: str,
        filter_activity: str,
        filter_spatial: str):
    """Generate query condition from filters dynamic VT."""
    sql = 't.scientific_name=%s '
    query_values = [filter_species_name]
    if filter_start_year and filter_end_year:
        sql = sql + 'AND ap.year between %s and %s '
        query_values.append(filter_start_year)
        query_values.append(filter_end_year)
    if filter_organisation:
        sql = sql + 'AND p.organisation_id IN %s '
        query_values.append(ast.literal_eval('('+filter_organisation+')'))
    else:
        sql = sql + 'AND p.organisation_id=%s '
        query_values.append(organisation_id)
    if filter_activity:
        sql = sql + 'AND aa.name=%s '
        query_values.append(filter_activity)
    # TODO: filter_spatial
    return sql, query_values


def get_population_query(
        type: PopulationQueryEnum,
        z: int, x: int, y: int,
        organisation_id: int,
        filter_start_year: int,
        filter_end_year: int,
        filter_species_name: str,
        filter_organisation: str,
        filter_activity: str,
        filter_spatial: str):
    """Generate query for population count."""
    where_sql, query_values = get_query_condition(
        organisation_id, filter_start_year, filter_end_year,
        filter_species_name, filter_organisation, filter_activity,
        filter_spatial
    )
    additional_join=(
        'inner join activity_activitytype aa '
        'on aa.id=ap.activity_type_id' if filter_activity else ''
    )
    population_table=(
        'annual_population_per_activity' if filter_activity else
        'annual_population'
    )
    sql = ''
    if type == PopulationQueryEnum.PROVINCE_LAYER:
        sql = (
            """
            select prov.id as id, sum(ap.total) as count
            from {population_table} ap
            inner join owned_species os on os.id=ap.owned_species_id
            inner join taxon t on os.taxon_id=t.id
            inner join property p on os.property_id=p.id
            inner join province prov on prov.id=p.province_id
            {additional_join}
            where {where_sql} group by prov.id
            """
        ).format(
            additional_join=additional_join,
            population_table=population_table,
            where_sql=where_sql
        )
    elif type == PopulationQueryEnum.SUMMARY_COUNT:
        sql = (
            """
            select p.id, p.name, sum(ap.total) as count
            from {population_table} ap
            inner join owned_species os on os.id=ap.owned_species_id
            inner join taxon t on os.taxon_id=t.id
            inner join property p on os.property_id=p.id
            {additional_join}
            where {where_sql} group by p.id
            """
        ).format(
            additional_join=additional_join,
            population_table=population_table,
            where_sql=where_sql
        )
    elif (
        type == PopulationQueryEnum.PROPERTIES_LAYER or
        type == PopulationQueryEnum.PROPERTIES_POINTS_LAYER
    ):
        geom_field = (
            'centroid' if
            type == PopulationQueryEnum.PROPERTIES_POINTS_LAYER else
            'geometry'
        )
        where_sql = (
            'p.{geom_field} && TileBBox(%s, %s, %s, 4326) AND ' + where_sql
        ).format(geom_field=geom_field)
        sql = (
            """
            select p.id,
            ST_AsMVTGeom(ST_Transform(p.{geom_field}, 3857),
                TileBBox(%s, %s, %s, 3857)) as geom,
            p.name, sum(ap.total) as count
            from {population_table} ap
            inner join owned_species os on os.id=ap.owned_species_id
            inner join taxon t on os.taxon_id=t.id
            inner join property p on os.property_id=p.id
            {additional_join}
            where {where_sql} group by p.id
            """
        ).format(
            geom_field=geom_field,
            additional_join=additional_join,
            population_table=population_table,
            where_sql=where_sql
        )
        tilebbox_values = [z, x, y, z, x, y]
        tilebbox_values.extend(query_values)
        query_values = tilebbox_values
    else:
        raise ValueError(f'Invalid PopulationQuery type: {type}')
    return sql, query_values


def get_count_summary_of_population(
        is_province_layer: bool,
        organisation_id: int,
        filter_start_year: int,
        filter_end_year: int,
        filter_species_name: str,
        filter_organisation: str,
        filter_activity: str,
        filter_spatial: str):
    """
    Return (Min, Max) for population query count.
    
    :return: Tuple[int, int]: A tuple of (Min, Max) population count
    """
    type = (
        PopulationQueryEnum.PROVINCE_LAYER if is_province_layer else
        PopulationQueryEnum.SUMMARY_COUNT
    )
    sub_sql, query_values = get_population_query(
        type, 0, 0, 0, organisation_id,
        filter_start_year, filter_end_year, filter_species_name,
        filter_organisation, filter_activity, filter_spatial
    )
    sql = (
        """
        select min(count), max(count) from ({sub_sql}) as population_count
        """
    ).format(sub_sql=sub_sql)
    max = 0
    min = 0
    with connection.cursor() as cursor:
        cursor.execute(sql, query_values)
        row = cursor.fetchone()
        if row:
            min = row[0] if row[0] else 0
            max = row[1] if row[1] else 0
    return (min, max)


def generate_population_count_categories_base(
        min: int,
        max: int,
        base_color: str):
    """
    Generate population count categories for choropleth map.
    Using equal interval classification.
    http://wiki.gis.com/wiki/index.php/Equal_Interval_classification
    
    :param min: minimum population count
    :param max: maximum population count
    :param base_color: base color in ex to calculate color gradient
    :return: list of dict of minLabel, maxLabel, value and color.
    """
    result = []
    colors = linear_gradient(base_color, n=CHOROPLETH_NUMBER_OF_BREAKS)['hex']
    colors = colors[::-1]
    break_val = math.ceil((max - min) / CHOROPLETH_NUMBER_OF_BREAKS)
    if break_val == 0:
        # case min = max
        break_val = 1
    val = min
    for t in range(0, CHOROPLETH_NUMBER_OF_BREAKS):
        result.append({
            'minLabel': val,
            'maxLabel': val + break_val,
            'value': val,
            'color': ''
        })
        val += break_val
        if val > max:
            break
    t = CHOROPLETH_NUMBER_OF_BREAKS - 1
    for element in reversed(result):
        element['color'] = colors[t]
        t -= 1
        if t <= -1:
            break
    return result


def generate_population_count_categories(
        is_province_layer: bool,
        organisation_id: int,
        filter_start_year: int,
        filter_end_year: int,
        filter_species_name: str,
        filter_organisation: str,
        filter_activity: str,
        filter_spatial: str):
    min, max = get_count_summary_of_population(
        is_province_layer, organisation_id, filter_start_year,
        filter_end_year, filter_species_name, filter_organisation,
        filter_activity, filter_spatial
    )
    base_color = DEFAULT_BASE_COLOR
    taxon = Taxon.objects.filter(scientific_name=filter_species_name).first()
    if taxon and taxon.colour:
        base_color = taxon.colour
    return generate_population_count_categories_base(min, max, base_color)
