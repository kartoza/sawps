import re
import os
import subprocess
from django.db import connection
from datetime import datetime
from uuid import uuid4
import shutil
import logging
import math

from core.settings.utils import absolute_path
from frontend.models.context_layer import ContextLayerTilingTask

logger = logging.getLogger(__name__)


def get_country_bounding_box():
    """Get South Africa bbox."""
    bbox = []
    iso3 = 'ZAF'
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT ST_Extent(w.geom) as bextent FROM layer.world w '
            'WHERE w."ISO_A3"=%s', [iso3]
        )
        extent = cursor.fetchone()
        if extent:
            try:
                bbox = re.findall(r'[-+]?(?:\d*\.\d+|\d+)', extent[0])
            except TypeError:
                pass
    return bbox


def generate_configuration_file() -> str:
    """Generate tegola config file."""
    template_config_file = absolute_path(
        'frontend', 'utils', 'config.conf'
    )
    result = ''
    try:
        out_config_file = os.path.join(
            '/',
            'opt',
            'tegola_config',
            f'context-layer-{uuid4()}.conf'
        )
        shutil.copy(template_config_file, out_config_file)
        result = out_config_file
    except Exception as ex:
        logger.error('Error generating configuration file ', ex)
    return result


def convert_size(size_bytes):
    """Convert size in bytes to readable text."""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def get_folder_size(directory_path):
    """Get directory size in bytes."""
    if not os.path.exists(directory_path):
        return '0'
    folder_size = 0
    # get size
    for path, dirs, files in os.walk(directory_path):
        for f in files:
            fp = os.path.join(path, f)
            folder_size += os.stat(fp).st_size
    return convert_size(folder_size)


def calculate_vector_tile_size() -> str:
    """Get directory total size."""
    tile_path = os.path.join(
        '/',
        'opt',
        'layer_tiles',
        'sanbi'
    )
    return get_folder_size(tile_path)


def generate_vector_tiles(tiling_task: ContextLayerTilingTask,
                          overwrite: bool = False):
    """Generate vector tiles for static context layers."""
    bbox = get_country_bounding_box()
    if not overwrite and tiling_task.config_path:
        config_file = tiling_task.config_path
    else:
        config_file = generate_configuration_file()
    tiling_task.status = ContextLayerTilingTask.TileStatus.PROCESSING
    tiling_task.started_at = datetime.now()
    tiling_task.finished_at = None
    tiling_task.total_size = 0
    tiling_task.task_return_code = None
    tiling_task.log = None
    tiling_task.error_log = None
    tiling_task.config_path = config_file
    tiling_task.save(
        update_fields=[
            'status', 'started_at', 'finished_at',
            'total_size', 'task_return_code', 'log',
            'error_log', 'config_path'
        ]
    )

    command_list = (
        [
            '/opt/tegola',
            'cache',
            'seed',
            '--config',
            config_file,
            '--overwrite' if overwrite else '',
            '--concurrency',
            '2',
        ]
    )
    _bbox = []
    for coord in bbox:
        _bbox.append(str(round(float(coord), 3)))
    command_list.extend([
        '--bounds',
        ','.join(_bbox)
    ])
    command_list.extend([
        '--min-zoom',
        '0',
        '--max-zoom',
        '24'
    ])
    logger.info('Starting vector tile generation')
    result = subprocess.run(command_list)
    return_code = result.returncode
    logger.info(
        f'Finished generating vector tile with return code {return_code}')
    # move temporary folder to sanbi folder
    destination_tile_path = os.path.join(
        '/',
        'opt',
        'layer_tiles',
        'sanbi'
    )
    source_tile_path = os.path.join(
        '/',
        'opt',
        'layer_tiles',
        'tmp',
        'sanbi'
    )
    if os.path.exists(destination_tile_path):
        shutil.rmtree(destination_tile_path)

    try:
        shutil.move(
            source_tile_path,
            destination_tile_path
        )
    except FileNotFoundError as ex:
        return_code = 999
        logger.error('Unable to move vector tile directory', ex)
    logger.info('Finished moving vector tile to sanbi directory')
    # finish generation
    tiling_task.finished_at = datetime.now()
    tiling_task.total_size = calculate_vector_tile_size()
    tiling_task.status = (
        ContextLayerTilingTask.TileStatus.DONE if return_code == 0 else
        ContextLayerTilingTask.TileStatus.ERROR
    )
    tiling_task.task_return_code = return_code
    tiling_task.save(
        update_fields=[
            'status', 'finished_at',
            'total_size', 'task_return_code', 'log',
            'error_log'
        ]
    )
