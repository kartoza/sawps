"""Helper function for map."""
import os
import json
import time
import ast
import math
from enum import Enum
from django.db import connection
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from core.settings.utils import absolute_path
from species.models import Taxon
from frontend.models.map_session import MapSession
from frontend.utils.color import linear_gradient


User = get_user_model()
# number of breaks to generate stops for color gradient of population count
CHOROPLETH_NUMBER_OF_BREAKS = 5
DEFAULT_BASE_COLOR = '#FF5252'


class PopulationQueryEnum(Enum):
    PROVINCE_LAYER = 'Province Layer'
    PROPERTIES_LAYER = 'Properties Layer'
    PROPERTIES_POINTS_LAYER = 'Properties Points Layer'
    SUMMARY_COUNT = 'SUMMARY COUNT'


def get_map_template_style(request, session, theme_choice: int = 0,
                           token: str = None):
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
        url = url + f'?t={int(time.time())}&session={session}'
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


def get_query_condition_for_population_query(
        organisation_id: int,
        filter_start_year: int,
        filter_end_year: int,
        filter_species_name: str,
        filter_organisation: str,
        filter_activity: str,
        filter_spatial: str):
    """Generate query condition from filters dynamic VT."""
    sql_conditions = []
    query_values = []
    if filter_species_name:
        sql_conditions.append('t.scientific_name=%s')
        query_values.append(filter_species_name)
    if filter_start_year and filter_end_year:
        sql_conditions.append('ap.year between %s and %s')
        query_values.append(filter_start_year)
        query_values.append(filter_end_year)
    if filter_organisation:
        sql_conditions.append('p.organisation_id IN %s')
        query_values.append(ast.literal_eval('(' + filter_organisation + ')'))
    else:
        sql_conditions.append('p.organisation_id=%s')
        query_values.append(organisation_id)
    if filter_activity:
        sql_conditions.append('aa.name=%s')
        query_values.append(filter_activity)
    if filter_spatial:
        spatial_filter_values = tuple(
            filter(None, filter_spatial.split(','))
        )
        if spatial_filter_values:
            spatial_sql = (
                """
                select 1 from frontend_spatialdatavaluemodel fs2
                inner join frontend_spatialdatamodel fs3 on
                fs3.id = fs2.spatial_data_id
                where fs3.property_id=p.id and fs2.context_layer_value in %s
                """
            )
            sql_conditions.append(
                'exists({spatial_sql})'.format(spatial_sql=spatial_sql)
            )
            query_values.append(spatial_filter_values)
    sql = ' AND '.join(sql_conditions)
    return sql, query_values


def get_population_query(
        is_province_view: bool,
        organisation_id: int,
        filter_start_year: int,
        filter_end_year: int,
        filter_species_name: str,
        filter_organisation: str,
        filter_activity: str,
        filter_spatial: str):
    """Generate query for population count."""
    where_sql, query_values = get_query_condition_for_population_query(
        organisation_id, filter_start_year, filter_end_year,
        filter_species_name, filter_organisation, filter_activity,
        filter_spatial
    )
    additional_join = (
        'inner join activity_activitytype aa '
        'on aa.id=ap.activity_type_id' if filter_activity else ''
    )
    population_table = (
        'annual_population_per_activity' if filter_activity else
        'annual_population'
    )
    id_field = 'province_id' if is_province_view else 'id'
    sql = (
        """
        select p.{id_field} as id, sum(ap.total) as count
        from {population_table} ap
        inner join owned_species os on os.id=ap.owned_species_id
        inner join taxon t on os.taxon_id=t.id
        inner join property p on os.property_id=p.id
        {additional_join}
        {where_sql} group by p.{id_field}
        """
    ).format(
        additional_join=additional_join,
        population_table=population_table,
        where_sql=f'where {where_sql}' if where_sql else '',
        id_field=id_field
    )
    return sql, query_values


def get_count_summary_of_population(
        is_province_layer: bool,
        session: MapSession):
    """
    Return (Min, Max) for population query count.
    Materialized view for current session must be created.

    :return: Tuple[int, int]: A tuple of (Min, Max) population count
    """
    sql = (
        """
        select min(count), max(count) from "{view_name}"
        """
    ).format(
        view_name=(
            session.province_view_name if is_province_layer else
            session.properties_view_name
        )
    )
    max = 0
    min = 0
    with connection.cursor() as cursor:
        cursor.execute(sql)
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
    if max == 0 and min == 0:
        result.append({
            'minLabel': 0,
            'maxLabel': 0,
            'value': 0,
            'color': '#ffffff'
        })
        return result
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
        session: MapSession,
        filter_species_name: str):
    min, max = get_count_summary_of_population(is_province_layer, session)
    base_color = DEFAULT_BASE_COLOR
    taxon = Taxon.objects.filter(scientific_name=filter_species_name).first()
    if taxon and taxon.colour:
        base_color = taxon.colour
    return generate_population_count_categories_base(min, max, base_color)


def create_map_materialized_view(view_name: str, sql: str, query_values):
    """Execute sql to create materialized view."""
    view_sql = (
        """
        CREATE MATERIALIZED VIEW "{view_name}"
        AS {sql}
        """
    ).format(
        view_name=view_name,
        sql=sql
    )
    index_sql = (
        """
        CREATE UNIQUE INDEX "{view_name}_idx" ON "{view_name}" (id)
        """
    ).format(view_name=view_name)
    with connection.cursor() as cursor:
        cursor.execute(view_sql, query_values)
        cursor.execute(index_sql)
        if '_province' in view_name:
            # need to add index by name
            index_sql = (
                """
                CREATE UNIQUE INDEX "{view_name}_name_idx"
                ON "{view_name}" (name)
                """
            ).format(view_name=view_name)
            cursor.execute(index_sql)


def drop_map_materialized_view(view_name: str):
    """Execute sql to drop materialized view."""
    view_sql = (
        """
        DROP MATERIALIZED VIEW IF EXISTS "{view_name}"
        """
    ).format(view_name=view_name)
    with connection.cursor() as cursor:
        cursor.execute(view_sql)


def refresh_map_materialized_view(view_name: str):
    """Execute sql to refresh materialized view."""
    view_sql = (
        """
        REFRESH MATERIALIZED VIEW "{view_name}"
        """
    ).format(view_name=view_name)
    with connection.cursor() as cursor:
        cursor.execute(view_sql)


def delete_expired_map_materialized_view():
    """Remove expired materialized view."""
    sessions = MapSession.objects.filter(
        expired_date__lt=timezone.now()
    )
    total_count = sessions.count()
    for session in sessions:
        session.delete()
    return total_count


def generate_map_view(
        session: MapSession,
        is_province_view: bool,
        organisation_id: int,
        filter_start_year: int = None,
        filter_end_year: int = None,
        filter_species_name: str = None,
        filter_organisation: str = None,
        filter_activity: str = None,
        filter_spatial: str = None):
    if is_province_view:
        drop_map_materialized_view(session.province_view_name)
    else:
        drop_map_materialized_view(session.properties_view_name)
    sub_sql, query_values = get_population_query(
        is_province_view, organisation_id, filter_start_year,
        filter_end_year, filter_species_name, filter_organisation,
        filter_activity, filter_spatial
    )
    table_name = 'province' if is_province_view else 'property'
    is_choropleth_view = True if filter_species_name else False
    sql_view = (
        """
        select p2.id, p2.name, COALESCE(population_summary.count, 0) as count
        from {table_name} p2
        {pop_join} ({sub_sql}) as population_summary
        on p2.id=population_summary.id
        """
    ).format(
        table_name=table_name,
        sub_sql=sub_sql,
        pop_join='left join' if is_choropleth_view else 'inner join'
    )
    create_map_materialized_view(
        session.province_view_name if is_province_view else
        session.properties_view_name, sql_view, query_values
    )
    # store queryparams
    query_params = (
        """
        start_year={start_year}&end_year={end_year}&species={species}&
        organisation={organisation}&activity={activity}&
        spatial_filter_values={spatial_filter_values}
        """
    ).format(
        start_year=filter_start_year,
        end_year=filter_end_year,
        species=filter_species_name,
        organisation=filter_organisation,
        activity=filter_activity,
        spatial_filter_values=filter_spatial
    )
    session.query_params = query_params
    session.save(update_fields=['query_params'])
