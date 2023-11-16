"""Task to generate statistical model for a species."""
import os
import logging
import traceback
import json
from django.core.files import File
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.utils import timezone
from celery import shared_task
from species.models import Taxon
from population_data.models import AnnualPopulation
from frontend.models.base_task import DONE, ERROR
from frontend.models.statistical import SpeciesModelOutput
from frontend.utils.statistical_model import (
    write_plumber_data,
    execute_statistical_model,
    remove_plumber_data
)


logger = logging.getLogger(__name__)


def export_annual_population_data(taxon: Taxon):
    csv_headers = [
        'species', 'property', 'province', 'year', 'pop_est',
        'lower_est', 'upper_est', 'survey_method',
        'ownership', 'property_size_ha',
        'area_available_to_species', 'open_closed'
    ]
    rows = AnnualPopulation.objects.select_related(
        'survey_method',
        'taxon',
        'property',
        'property__province',
        'property__property_type',
        'property__open'
    ).filter(
        taxon=taxon
    ).order_by('year')
    csv_data = [
        [
            taxon.scientific_name,
            row.property.name,
            row.property.province.name,
            row.year,
            row.total,
            'NA',
            'NA',
            row.survey_method.name if row.survey_method else 'NA',
            row.property.property_type.name,
            row.property.property_size_ha,
            row.area_available_to_species,
            row.property.open.name if row.property.open else 'NA',
        ] for row in rows
    ]
    return write_plumber_data(csv_headers, csv_data)


def save_model_output_on_success(model_output: SpeciesModelOutput, data_filepath, json_data):
    model_output.finished_at = timezone.now()
    model_output.status = DONE
    model_output.errors = None
    model_output.generated_on = timezone.now()
    model_output.is_outdated = False
    model_output.outdated_since = None
    model_output.save()

    taxon_name = slugify(model_output.taxon.scientific_name).replace('-', '_')
    if data_filepath and os.path.exists(data_filepath):
        with open(data_filepath, 'rb') as input_file:
            input_name = f'{model_output.id}_{taxon_name}.csv'
            model_output.input_file.save(input_name, File(input_file))
    if json_data:
        output_name = f'{model_output.id}_{taxon_name}.json'
        model_output.output_file.save(
            output_name, ContentFile(json.dumps(json_data)))
    # TODO: update cache: national and provincial data
    # set previous model is_latest to False
    SpeciesModelOutput.objects.filter(
        taxon=model_output.taxon
    ).exclude(id=model_output.id).update(is_latest=False)
    # last update the model output with is_latest = True
    model_output.is_latest = True
    model_output.save(update_fields=['is_latest'])


def save_model_output_on_failure(model_output: SpeciesModelOutput, errors=None):
    model_output.finished_at = timezone.now()
    model_output.status = ERROR
    model_output.errors = errors
    model_output.save(update_fields=['finished_at', 'status', 'errors'])


@shared_task(name="check_oudated_model_output")
def check_oudated_model_output():
    """
    Check for outdated model output and trigger a job to generate.
    
    CSV Data Upload Flow:
    CSV Upload -> List of species -> mark latest model output as outdated

    Online Form Flow:
    Input data for a species -> mark latest model output as outdated

    R Code Update:
    StatisticalModel Update -> mark latest model output as outdated -> restart plumber
    -> Plumber ready -> trigger check_oudated_model_output manually

    R Code Create:
    StatisticalModel Create -> create model output with outdated=True
    -> restart plumber -> Plumber ready -> trigger check_oudated_model_output manually

    This check_outdated_model_output will check every model output
    that needs to be refreshed.
    """
    pass


@shared_task(name="generate_species_statistical_model")
def generate_species_statistical_model(request_id):
    """Generate species statistical model."""
    model_output = SpeciesModelOutput.objects.get(id=request_id)
    model_output.task_on_started()
    data_filepath = None
    try:
        data_filepath = export_annual_population_data(model_output.taxon)
        is_success, json_data = execute_statistical_model(
            data_filepath, model_output.taxon, model=model_output.model)
        if is_success:
            save_model_output_on_success(model_output, data_filepath, json_data)
        else:
            save_model_output_on_failure(model_output, errors=str(json_data))
    except Exception as ex:
        logger.error(traceback.format_exc())
        save_model_output_on_failure(model_output, errors=str(ex))
    finally:
        if data_filepath:
            remove_plumber_data(data_filepath)


@shared_task(name="clean_old_model_output")
def clean_old_model_output():
    """Remove old model output that has more recent model."""
    pass
