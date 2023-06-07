"""Helper function for map."""
import os
import json
from django.contrib.sites.models import Site
from django.conf import settings
from django.urls import reverse
from core.settings.utils import absolute_path


def get_map_template_style(request, theme_choice: int = 0):
    """
    Fetch map template style from file.
    
    :param theme_choice: 0 light, 1 dark
    :return: json map style
    """
    style_file_path = absolute_path(
        'frontend', 'utils', 'sanbi_styling_v7_light.json'
    )
    if theme_choice == 1:
        style_file_path = absolute_path(
            'frontend', 'utils', 'sanbi_styling_v7_dark.json'
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
    if 'sources' in styles and 'sanbi' in styles['sources']:
        styles['sources']['sanbi']['tiles'] = [
            f'{schema}{domain}/maps/sanbi/{{z}}/{{x}}/{{y}}.pbf'
        ]
    if 'sources' in styles and 'NGI Aerial Imagery' in styles['sources']:
        url = (
            reverse('aerial-map-tile', kwargs={
                'z': 0,
                'x': 0,
                'y': 0
            })
        )
        url = request.build_absolute_uri(url)
        url = url.replace('/0/0/0', '/{z}/{x}/{y}')
        if not settings.DEBUG:
            # if not dev env, then replace with https
            url = url.replace('http://', 'https://')
        styles['sources']['NGI Aerial Imagery']['tiles'] = [url]
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
