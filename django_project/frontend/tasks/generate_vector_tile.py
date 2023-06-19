from celery import shared_task
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
