from celery import shared_task
import logging
import traceback
import os
import time
import csv
import subprocess
from datetime import datetime
import requests
from django.core.files.base import ContentFile
from frontend.models.base_task import (
    DONE, ERROR
)
from frontend.models.statistical import (
    StatisticalTaskRequest
)
from population_data.models import (
    AnnualPopulation
)


logger = logging.getLogger(__name__)
# when running with more than 1 worker, this needs to be a list
PLUMBER_PORT = 8000
# when the code contains one of plot functions, output to png
R_PLOT_FUNCTIONS = [
    'plot',
    'hist',
    'ggplot',
    'barplot',
    'pie',
    'boxplot',
    'pairs',
    'coplot'
]


@shared_task(name="run_statistical_model")
def run_statistical_model(request_id):
    request_task = StatisticalTaskRequest.objects.get(id=request_id)
    # reset result fields
    request_task.reset()
    request_task.task_on_started()
    write_r_code(request_task)
    write_r_data(request_task)
    process = spawn_r_plumber(request_task)
    if process:
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
    else:
        # failed to spawn the plumber
        request_task.status = ERROR
        request_task.error = 'Unexepected error while running plumber!'
        request_task.finished_at = datetime.now()
        request_task.progress_text = 'Error'
        request_task.save()


def is_graph_output(code: str):
    for f in R_PLOT_FUNCTIONS:
        if f'{f}(' in code:
            return True
    return False


def write_r_code(request: StatisticalTaskRequest):
    """Write R statistical code to file."""
    if (
        request.statistical_model.code is None or
        request.statistical_model.code == ''
    ):
        logger.warn(
            'Empty code in the statistical '
            f'model of {request.statistical_model}!')
        return
    r_file_path = os.path.join(
        '/home/web/plumber_data',
        f'{str(request.uuid)}.R'
    )
    lines = [
        '# plumber.R',
        '',
        '#* Echo back the input',
        '#* @get /echo',
        'function() {',
        '    list(msg = paste0("Plumber is working!"))',
        '}',
        '',
        f'#* Task Request {str(request.uuid)}',
    ]
    if is_graph_output(request.statistical_model.code):
        if 'ggplot(' in request.statistical_model.code:
            """we need to bypass png serializer
            https://stackoverflow.com/questions/50033857/
            serve-arbitrary-image-files-through-plumber
            """
            lines.append("#* @serializer contentType list(type='image/png')")
        else:
            lines.append('#* @serializer png')
    lines.append(f'#* @get /{str(request.uuid)}')
    lines.append('function() {')
    # add read data
    r_data_path = os.path.join(
        '/home/web/plumber_data',
        f'{str(request.uuid)}.csv'
    )
    lines.append(f"  data=read.csv('{r_data_path}')")
    code_lines = request.statistical_model.code.splitlines()
    for code in code_lines:
        lines.append(f'  {code}')
    lines.append('}')
    with open(r_file_path, 'w') as f:
        for line in lines:
            f.write(line)
            f.write('\n')


def write_r_data(request: StatisticalTaskRequest):
    """Export data to csv for R input."""
    # export population data
    # cols: property (name), species, year, estimate (annual total),
    #       survey_method, count_method
    r_data_path = os.path.join(
        '/home/web/plumber_data',
        f'{str(request.uuid)}.csv'
    )
    header = [
        'property', 'species', 'year', 'estimate_population',
        'survey_method', 'count_method'
    ]
    with open(r_data_path, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        rows = AnnualPopulation.objects.select_related(
            'owned_species', 'survey_method', 'count_method'
        ).filter(
            owned_species__property__organisation=request.organisation,
            owned_species__taxon=request.taxon
        ).order_by('year')
        for row in rows:
            writer.writerow([
                row.owned_species.property.name,
                row.owned_species.taxon.scientific_name,
                row.year,
                row.total,
                row.survey_method.name,
                row.count_method.name
            ])


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


def spawn_r_plumber(request: StatisticalTaskRequest):
    """Run Plumber API server."""
    command_list = (
        [
            'R',
            '-e',
            (
                "pr <- plumber::plumb("
                f"'/home/web/plumber_data/{str(request.uuid)}.R'); "
                f"args <- list(host = '0.0.0.0', port = {PLUMBER_PORT}); "
                "do.call(pr$run, args)"
            )
        ]
    )
    logger.info('Starting plumber API')
    process = None
    try:
        process = subprocess.Popen(
            command_list
        )
        # sleep for 2 seconds to wait the API is up
        time.sleep(2)
        # we can also use polling to echo endpoint for health check
        plumber_health_check()
    except Exception as ex:  # noqa
        logger.error(ex)
        logger.error(traceback.format_exc())
        if process:
            process.terminate()
            process = None
    return process


def stop_r_plumber(process):
    """Kill running plumber."""
    process.terminate()


def plumber_health_check():
    """Check whether API is up and running."""
    request_url = f'http://0.0.0.0:{PLUMBER_PORT}/echo'
    retry = 0
    max_retry = 25
    req = requests.get(request_url)
    while req.status_code != 200 and retry < max_retry:
        time.sleep(1)
        req = requests.get(request_url)
        retry += 1
    if retry < max_retry:
        logger.info('Plumber API is up and running!')
    return retry < max_retry


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
