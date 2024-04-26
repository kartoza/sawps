"""Task to generate statistical model for a species."""
import os
import logging
import traceback
import json
import time
from datetime import datetime, timedelta
from django.core.files import File
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.utils import timezone
from celery import shared_task
from species.models import Taxon
from population_data.models import AnnualPopulation
from frontend.models.base_task import DONE, ERROR, PENDING
from frontend.models.statistical import (
    StatisticalModel,
    SpeciesModelOutput,
    NATIONAL_GROWTH,
    PROVINCIAL_GROWTH,
    NATIONAL_GROWTH_CAT,
    OutputTypeCategoryIndex
)
from frontend.utils.statistical_model import (
    write_plumber_data,
    execute_statistical_model,
    remove_plumber_data,
    store_species_model_output_cache,
    clear_species_model_output_cache,
    mark_model_output_as_outdated_by_model,
    init_species_model_output_from_generic_model,
    init_species_model_output_from_non_generic_model
)
from frontend.utils.celery import cancel_task
from core.settings.utils import absolute_path


logger = logging.getLogger(__name__)


def export_annual_population_data(taxon: Taxon):
    """Export annual population to csv data."""
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


def save_model_data_input(model_output: SpeciesModelOutput, data_filepath):
    """Store csv data of annual population data."""
    taxon_name = slugify(model_output.taxon.scientific_name).replace('-', '_')
    if data_filepath and os.path.exists(data_filepath):
        with open(data_filepath, 'rb') as input_file:
            input_name = f'{model_output.id}_{taxon_name}.csv'
            model_output.input_file.save(input_name, File(input_file))


def sort_output_type_categories(data_set: set, category_index_list):
    """Sort set of categories by OutputTypeCategoryIndex list."""
    result = []
    for category in category_index_list:
        find_val = [val for val in data_set if category.val in val]
        if find_val:
            result.append(find_val[0])
            data_set.remove(find_val[0])
    if data_set:
        for val in data_set:
            result.insert(0, val)
    return result


def add_json_metadata(json_data):
    """
    Generate metadata for category values sorted
    by OutputTypeCategoryIndex.
    """
    metadata = json_data.get('metadata', {})
    # growth output types should have categories in field_name:
    # period and pop_change_cat
    growth_output_types = [
        NATIONAL_GROWTH, PROVINCIAL_GROWTH, NATIONAL_GROWTH_CAT
    ]
    for growth_type in growth_output_types:
        if growth_type not in json_data:
            continue
        periods = set()
        pop_change_cats = set()
        period_cat_index = (
            OutputTypeCategoryIndex.objects.find_category_index(
                growth_type, 'period'
            )
        )
        pop_change_cat_index = (
            OutputTypeCategoryIndex.objects.find_category_index(
                growth_type, 'pop_change_cat'
            )
        )
        data = json_data[growth_type]
        for item in data:
            period_str = item.get('period', '')
            pop_change_cat_str = item.get('pop_change_cat', '')
            if period_str:
                periods.add(period_str.lower())
            if pop_change_cat_str:
                pop_change_cats.add(pop_change_cat_str.lower())
        metadata[growth_type] = {
            'period': sort_output_type_categories(periods, period_cat_index),
            'pop_change_cat': sort_output_type_categories(
                pop_change_cats, pop_change_cat_index),
        }
    json_data['metadata'] = metadata
    return json_data


def save_model_output_on_success(model_output: SpeciesModelOutput, json_data):
    """Store the result from successful execution of R statistical model."""
    model_output.finished_at = timezone.now()
    model_output.status = DONE
    model_output.errors = None
    model_output.generated_on = timezone.now()
    model_output.is_outdated = False
    model_output.outdated_since = None
    model_output.save()
    taxon_name = slugify(model_output.taxon.scientific_name).replace('-', '_')
    json_data = add_json_metadata(json_data)
    output_name = f'{model_output.id}_{taxon_name}.json'
    model_output.output_file.save(
        output_name, ContentFile(json.dumps(json_data)))
    # update cache: national and provincial data
    store_species_model_output_cache(model_output, json_data)
    # set previous model is_latest to False
    latest_output = SpeciesModelOutput.objects.filter(
        taxon=model_output.taxon,
        is_latest=True
    ).exclude(id=model_output.id)
    for output in latest_output:
        clear_species_model_output_cache(output)
        output.is_latest = False
        output.save()
    # last update the model output with is_latest = True
    model_output.is_latest = True
    model_output.save(update_fields=['is_latest'])


def save_model_output_on_failure(model_output: SpeciesModelOutput,
                                 errors=None):
    """Store failure from execution R statistical model."""
    model_output.finished_at = timezone.now()
    model_output.status = ERROR
    model_output.errors = errors
    model_output.is_outdated = False
    model_output.outdated_since = None
    model_output.save(update_fields=['finished_at', 'status',
                                     'errors', 'is_outdated',
                                     'outdated_since'])


def trigger_generate_species_model_output(model_output: SpeciesModelOutput):
    """Trigger generate species model output job."""
    logger.info(f'Regenerating statistical model output for {model_output}')
    if model_output.task_id:
        cancel_task(model_output.task_id)
    model_output.status = PENDING
    model_output.is_outdated = False
    model_output.outdated_since = None
    model_output.save(update_fields=['status', 'is_outdated',
                                     'outdated_since'])
    task = generate_species_statistical_model.delay(model_output.id)
    model_output.task_id = task.id
    model_output.save(update_fields=['task_id'])


@shared_task(name="check_affected_model_output")
def check_affected_model_output(model_id, is_created):
    """
    Triggered when model is created/updated.
    """
    from frontend.tasks.start_plumber import (
        start_plumber_process
    )
    if is_created:
        time.sleep(2)
    model = StatisticalModel.objects.get(id=model_id)
    model_outputs = SpeciesModelOutput.objects.filter(
        model=model
    )
    if model_outputs.exists():
        mark_model_output_as_outdated_by_model(model)
    else:
        # create model output with outdated = True
        if model.taxon:
            # non generic model
            init_species_model_output_from_non_generic_model(model)
        else:
            # generic model - create new
            init_species_model_output_from_generic_model(model)
    # restart plumber to load new R codes
    start_plumber_process.apply_async(queue='plumber')


@shared_task(name="check_oudated_model_output", ignore_result=True)
def check_oudated_model_output():
    """
    Check for outdated model output and trigger a job to generate.

    CSV Data Upload Flow:
    CSV Upload -> List of species -> mark latest model output as outdated

    Online Form Flow:
    Input data for a species -> mark latest model output as outdated

    R Code Update:
    StatisticalModel Update -> mark latest model output as outdated
    -> restart plumber -> Plumber ready
    -> trigger check_oudated_model_output manually

    R Code Create:
    StatisticalModel Create -> create model output with outdated=True
    -> restart plumber -> Plumber ready
    -> trigger check_oudated_model_output manually

    This check_outdated_model_output will check every model output
    that needs to be refreshed.
    """
    outputs = SpeciesModelOutput.objects.filter(
        is_outdated=True,
        is_latest=True
    )
    for model_output in outputs:
        if model_output.output_file:
            # create a new model output
            model_output.is_outdated = False
            model_output.outdated_since = None
            model_output.save(update_fields=['is_outdated', 'outdated_since'])
            new_model_output = SpeciesModelOutput.objects.create(
                model=model_output.model,
                taxon=model_output.taxon,
                is_latest=False,
                is_outdated=True,
                outdated_since=timezone.now()
            )
            trigger_generate_species_model_output(new_model_output)
        else:
            # this is from initialization
            trigger_generate_species_model_output(model_output)


@shared_task(name="generate_species_statistical_model")
def generate_species_statistical_model(request_id):
    """Generate species statistical model."""
    model_output = SpeciesModelOutput.objects.get(id=request_id)
    model_output.task_on_started()
    data_filepath = None
    try:
        data_filepath = export_annual_population_data(model_output.taxon)
        save_model_data_input(model_output, data_filepath)
        model = model_output.model
        if model.taxon is None:
            # this is generic model
            model = None
        # is_success, json_data = execute_statistical_model(
        #     data_filepath, model_output.taxon, model=model)
        is_success = True
        file_path = absolute_path(
            'frontend', 'tasks', 'dummy.json'
        )
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)
        if is_success:
            save_model_output_on_success(model_output, json_data)
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
    datetime_filter = datetime.now() - timedelta(days=30)
    old_outputs = SpeciesModelOutput.objects.filter(
        is_latest=False,
        status=DONE,
        generated_on__lte=datetime_filter
    )
    total_count, _ = old_outputs.delete()
    logger.info(f'Clear old model output: {total_count} counts')
