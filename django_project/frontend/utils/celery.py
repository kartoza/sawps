import logging
from celery.result import AsyncResult
from core.celery import app

logger = logging.getLogger(__name__)


def cancel_task(task_id: str):
    """
    Cancel task if it's ongoing.

    :param task_id: task identifier
    """
    try:
        res = AsyncResult(task_id)
        if not res.ready():
            # find if there is running task and stop it
            app.control.revoke(
                task_id,
                terminate=True,
                signal='SIGKILL'
            )
    except Exception as ex:
        logger.error(f'Failed cancel_task: {task_id}')
        logger.error(ex)
