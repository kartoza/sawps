from celery import shared_task
import logging
import os
import time
import subprocess
from datetime import datetime
import requests
from django.core.files.base import ContentFile
from django.conf import settings
from frontend.models.base_task import (
    DONE
)
from frontend.models.statistical import (
    StatisticalTaskRequest
)

logger = logging.getLogger(__name__)
# when running with more than 1 worker, this needs to be a list
PLUMBER_PORT = 8000

@shared_task(name="run_statistical_model")
def run_statistical_model(request_id):
    request_task = StatisticalTaskRequest.objects.get(id=request_id)
    # reset result fields
    request_task.reset()
    request_task.task_on_started()
    write_r_code(request_task)
    write_r_data(request_task)
    process = spawn_r_plumber()
    execute_statistical_model(request_task)
    # stop the process
    process.kill()
    # clean files
    clean_r_files(request_task)
    # update status of the task
    request_task.status = DONE
    request_task.finished_at = datetime.now()
    request_task.progress = 100
    request_task.progress_text = 'Finished'
    request_task.save()


def write_r_code(request: StatisticalTaskRequest):
    """Write R statistical code to file."""
    pass


def write_r_data(request: StatisticalTaskRequest):
    """Export data to csv for R input."""
    pass


def clean_r_files(request: StatisticalTaskRequest):
    """Clear generated R file and R data."""
    r_file_path = os.path.join(
        '/home/web/plumber_data',
        f'{str(request.uuid)}.R'
    )
    if os.path.exists(r_file_path):
        os.remove(r_file_path)
    r_data_path = os.path.join(
        '/home/web/plumber_data',
        f'{str(request.uuid)}.csv'
    )
    if os.path.exists(r_data_path):
        os.remove(r_data_path)


def spawn_r_plumber():
    """Run Plumber API server."""
    command_list = (
        [
            'R',
            '-e',
            (
                "pr <- plumber::plumb('/home/web/plumber_data/plumber.R'); "
                f"args <- list(host = '0.0.0.0', port = {PLUMBER_PORT}); "
                "do.call(pr$run, args)"
            )
        ]
    )
    logger.info('Starting plumber API')
    process = subprocess.Popen(
        command_list
    )
    # sleep for 2 seconds to wait the API is up 
    time.sleep(2)
    # we can also use polling to echo endpoint for health check
    plumber_health_check()
    return process


def stop_r_plumber(process):
    """Kill running plumber."""
    process.terminate()


def plumber_health_check():
    """Check whether API is up and running."""
    request_url = f'http://0.0.0.0:{PLUMBER_PORT}/echo'
    req = requests.get(request_url)
    while req.status_code != 200:
        time.sleep(1)
        req = requests.get(request_url)
    logger.info('Plumber API is up and running!')


def execute_statistical_model(request: StatisticalTaskRequest):
    """Execute R Model."""
    request_url = f'http://0.0.0.0:{PLUMBER_PORT}/{str(request.uuid)}'
    logger.info(f'Calling plumber request at {request_url}')
    response = requests.get(request_url)
    logger.info(f'Plumber request status code {response.status_code}')
    request.return_code = response.status_code
    request.is_success = response.status_code == 200
    if not request.is_success:
        request.error = str(response.json())
    content_type = response.headers['Content-Type']
    if content_type == 'application/json':
        request.response = response.json()
    elif content_type.startswith('image/png'):
        request.image.save(
            f'{str(request.uuid)}.png',
            ContentFile(response.content)
        )
    if request.error:
        logger.error(request.error)
    request.save()
    # save is valid in the model
    request.statistical_model.is_valid = request.is_success
    if not request.is_success:
        request.statistical_model.last_error = request.error
    request.statistical_model.save()
