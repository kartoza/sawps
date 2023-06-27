"""Helper function for map."""
import os
import json
import time
from django.contrib.sites.models import Site
from django.conf import settings
from django.urls import reverse
from core.settings.utils import absolute_path


def get_map_template_style(request, theme_choice: int = 0, token: str = None):
    """
    Fetch map template style from file.

    :param theme_choice: 0 light, 1 dark
    :return: json map style
    """
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
        styles['sources']['properties'] = {
            "type": "vector",
            "tiles": [url],
            "minzoom": 12,
            "maxzoom": 24
        }
        # FF5252
        styles['layers'].append({
            "id": "properties",
            "type": "fill",
            "source": "properties",
            "source-layer": "properties",
            "minzoom": 12,
            "maxzoom": 24,
            "layout": {"visibility": "visible"},
            "paint": {
                "fill-color": "rgba(255, 82, 82, 1)",
                "fill-opacity": 0.8
            }
        })
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
        "line-color": "#008000",
        "line-width": [
          "case",
          ["boolean",
           ["feature-state", "parcel-selected-highlighted"], False], 4,
          0
      ],
        "line-opacity": 1
      }
    }
