from celery import shared_task
import logging
from frontend.utils.statistical_model import (
    kill_r_plumber_process,
    spawn_r_plumber,
    write_plumber_file
)


logger = logging.getLogger(__name__)


@shared_task(name="start_plumber_process")
def start_plumber_process():
    """Start plumber process when there is R code change."""
    logger.info('Starting plumber process')
    # kill existing process
    kill_r_plumber_process()
    # Generate plumber.R file
    write_plumber_file()
    # spawn the process
    plumber_process = spawn_r_plumber()
    if plumber_process:
        logger.info(f'plumber process pid {plumber_process.pid}')
    else:
        raise RuntimeError('Cannot execute plumber process!')
