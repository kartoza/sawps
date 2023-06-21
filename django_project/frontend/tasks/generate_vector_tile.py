from celery import shared_task
import os
import shutil
import logging
from frontend.utils.vector_tile import generate_vector_tiles

logger = logging.getLogger(__name__)


@shared_task(name="generate_vector_tiles")
def generate_vector_tiles_task(tiling_task_id: str,
                               overwrite: bool = True):
    from frontend.models.context_layer import ContextLayerTilingTask

    tiling_task = ContextLayerTilingTask.objects.get(id=tiling_task_id)
    logger.info(f'Generating vector tiles - {tiling_task_id}')
    generate_vector_tiles(tiling_task, overwrite=overwrite)


def resume_ongoing_vector_tile_task():
    """
    Resume any ongoing vector tile task.

    This should be called at startup.
    """
    from frontend.models.context_layer import ContextLayerTilingTask

    tiling_task = ContextLayerTilingTask.objects.filter(
        status=ContextLayerTilingTask.TileStatus.PROCESSING
    ).order_by('-id').first()
    if tiling_task:
        task = generate_vector_tiles_task.delay(tiling_task.id, False)
        tiling_task.task_id = task.id
        tiling_task.save()
        return tiling_task.id
    return 0


@shared_task(name="clear_older_vector_tiles")
def clear_older_vector_tiles():
    tile_path = os.path.join(
        '/',
        'opt',
        'layer_tiles',
        'sanbi'
    )
    if os.path.exists(tile_path):
        shutil.rmtree(tile_path)
