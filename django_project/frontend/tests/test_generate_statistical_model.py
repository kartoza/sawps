import os
import mock
import datetime
import csv
import requests_mock
import json
from django.test import TestCase
from species.factories import TaxonF, TaxonRankFactory
from population_data.factories import AnnualPopulationF
from frontend.models.base_task import DONE, PROCESSING, ERROR, PENDING
from frontend.models.statistical import (
    NATIONAL_TREND,
    NATIONAL_GROWTH,
    SpeciesModelOutput,
    CACHED_OUTPUT_TYPES,
    OutputTypeCategoryIndex
)
from frontend.tests.model_factories import (
    StatisticalModelF,
    SpeciesModelOutputF
)
from frontend.utils.statistical_model import (
    remove_plumber_data,
    PLUMBER_PORT
)
from frontend.tasks.generate_statistical_model import (
    clean_old_model_output,
    check_oudated_model_output,
    export_annual_population_data,
    save_model_data_input,
    save_model_output_on_success,
    save_model_output_on_failure,
    trigger_generate_species_model_output,
    check_affected_model_output,
    generate_species_statistical_model,
    add_json_metadata,
    sort_output_type_categories
)
from frontend.admin import (
    trigger_generate_species_statistical_model
)


def mocked_cache_op(self, *args, **kwargs):
    return 1


class DummyTask:
    def __init__(self, id):
        self.id = id

    def message_user(self, request, msg, type):
        pass


def mocked_process_func(*args, **kwargs):
    return DummyTask(1)


def mocked_raise_exception_func(*args, **kwargs):
    raise Exception('Test')


class TestGenerateStatisticalModel(TestCase):

    def test_export_annual_population_data(self):
        taxon = TaxonF.create()
        pop_1 = AnnualPopulationF.create(
            taxon=taxon
        )
        file_path = export_annual_population_data(taxon)
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r') as csv_file:
            csv_dict_reader = csv.DictReader(csv_file)
            headers = csv_dict_reader.fieldnames
            self.assertIn('species', headers)
            self.assertIn('property', headers)
            self.assertIn('province', headers)
            self.assertIn('year', headers)
            self.assertIn('pop_est', headers)
            self.assertIn('lower_est', headers)
            self.assertIn('upper_est', headers)
            self.assertIn('survey_method', headers)
            self.assertIn('ownership', headers)
            self.assertIn('property_size_ha', headers)
            self.assertIn('area_available_to_species', headers)
            self.assertIn('open_closed', headers)
            rows = list(csv_dict_reader)
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual(row['species'], taxon.scientific_name)
            self.assertEqual(row['property'], pop_1.property.name)
            self.assertEqual(row['province'], pop_1.property.province.name)
            self.assertEqual(row['year'], pop_1.year)
            self.assertEqual(row['pop_est'], str(pop_1.total))
        output = SpeciesModelOutputF.create(
            is_latest=False,
            is_outdated=False,
            status=DONE,
            generated_on=datetime.datetime(2000, 8, 14, 8, 8, 8)
        )
        save_model_data_input(output, file_path)
        self.assertTrue(output.input_file)
        self.assertTrue(
            output.input_file.storage.exists(output.input_file.name))
        output.delete()
        remove_plumber_data(file_path)
        self.assertFalse(os.path.exists(file_path))

    @mock.patch('django.core.cache.cache.set')
    @mock.patch('django.core.cache.cache.delete')
    def test_save_model_output_on_success(self, mocked_clear, mocked_set):
        mocked_clear.side_effect = mocked_cache_op
        mocked_set.side_effect = mocked_cache_op
        output = SpeciesModelOutputF.create(
            is_latest=False,
            is_outdated=False,
            status=PROCESSING,
            generated_on=datetime.datetime(2000, 8, 14, 8, 8, 8)
        )
        # ADD LATEST
        SpeciesModelOutputF.create(
            taxon=output.taxon,
            model=output.model,
            is_latest=True,
            is_outdated=False,
            status=DONE,
            generated_on=datetime.datetime(2000, 8, 14, 8, 8, 8)
        )
        save_model_output_on_success(output, {
            NATIONAL_TREND: 'abcdef'
        })
        output.refresh_from_db()
        self.assertEqual(output.status, DONE)
        self.assertFalse(output.errors)
        self.assertFalse(output.is_outdated)
        self.assertTrue(output.output_file)
        self.assertTrue(
            output.output_file.storage.exists(output.output_file.name))
        mocked_set.assert_called_once()
        self.assertTrue(output.is_latest)
        self.assertEqual(mocked_clear.call_count, len(CACHED_OUTPUT_TYPES))

    def test_save_model_output_on_failure(self):
        output = SpeciesModelOutputF.create(
            is_latest=False,
            is_outdated=False,
            status=PROCESSING,
            generated_on=datetime.datetime(2000, 8, 14, 8, 8, 8)
        )
        save_model_output_on_failure(output, errors='Test')
        output.refresh_from_db()
        self.assertEqual(output.status, ERROR)
        self.assertEqual(output.errors, 'Test')
        self.assertFalse(output.is_outdated)

    @mock.patch('frontend.tasks.generate_statistical_model.cancel_task')
    @mock.patch('frontend.tasks.generate_statistical_model.'
                'generate_species_statistical_model.delay')
    def test_trigger_generate_species_model_output(self,
                                                   mocked_process,
                                                   mocked_cancel):
        mocked_cancel.side_effect = mocked_process_func
        mocked_process.side_effect = mocked_process_func
        output = SpeciesModelOutputF.create(
            is_latest=False,
            is_outdated=False,
            status=PROCESSING,
            generated_on=datetime.datetime(2000, 8, 14, 8, 8, 8),
            task_id='123'
        )
        trigger_generate_species_model_output(output)
        mocked_cancel.assert_called_once()
        mocked_process.assert_called_once()
        output.refresh_from_db()
        self.assertEqual(output.status, PENDING)
        self.assertFalse(output.is_outdated)
        self.assertEqual(output.task_id, '1')

    @mock.patch('frontend.tasks.start_plumber.'
                'start_plumber_process.apply_async')
    def test_check_affected_model_output(self, mocked_process):
        species_rank = TaxonRankFactory.create(
            name='Species'
        )
        taxon_a = TaxonF.create(taxon_rank=species_rank)
        taxon_b = TaxonF.create(taxon_rank=species_rank)
        non_generic_model = StatisticalModelF.create(
            taxon=taxon_a
        )
        mocked_process.side_effect = mocked_process_func
        # test generic model
        model_1 = StatisticalModelF.create(
            taxon=None
        )
        check_affected_model_output(model_1.id, True)
        output_1 = SpeciesModelOutput.objects.filter(model=model_1)
        self.assertEqual(output_1.count(), 1)
        mocked_process.assert_called_once()
        mocked_process.reset_mock()
        # test non generic model
        check_affected_model_output(non_generic_model.id, False)
        output_1 = SpeciesModelOutput.objects.filter(model=non_generic_model)
        self.assertEqual(output_1.count(), 1)
        mocked_process.assert_called_once()
        mocked_process.reset_mock()
        # test existing model outputs
        model = StatisticalModelF.create(
            taxon=taxon_b
        )
        output = SpeciesModelOutputF.create(
            model=model,
            is_latest=True,
            is_outdated=False
        )
        check_affected_model_output(model.id, False)
        output.refresh_from_db()
        self.assertTrue(output.is_outdated)
        mocked_process.assert_called_once()

    @mock.patch('frontend.tasks.generate_statistical_model.cancel_task')
    @mock.patch('frontend.tasks.generate_statistical_model.'
                'generate_species_statistical_model.delay')
    def test_check_oudated_model_output(self, mocked_process, mocked_cancel):
        mocked_cancel.side_effect = mocked_process_func
        mocked_process.side_effect = mocked_process_func
        output_1 = SpeciesModelOutputF.create(
            is_latest=True,
            is_outdated=True,
            status=DONE,
            generated_on=datetime.datetime(2000, 8, 14, 8, 8, 8)
        )
        output_2 = SpeciesModelOutputF.create(
            is_latest=True,
            is_outdated=True,
            status=DONE,
            generated_on=datetime.datetime(2000, 8, 14, 8, 8, 8),
            task_id=None
        )
        save_model_output_on_success(output_2, {
            NATIONAL_TREND: 'abcdef'
        })
        output_2.is_outdated = True
        output_2.save()
        check_oudated_model_output()
        self.assertEqual(mocked_process.call_count, 2)
        output_2.refresh_from_db()
        self.assertFalse(output_2.is_outdated)
        self.assertEqual(output_2.status, DONE)
        self.assertFalse(output_2.task_id)
        output_1.refresh_from_db()
        self.assertFalse(output_1.is_outdated)
        self.assertEqual(output_1.status, PENDING)
        self.assertEqual(output_1.task_id, '1')
        new_output = SpeciesModelOutput.objects.filter(
            model=output_2.model,
            taxon=output_2.taxon,
            is_latest=False,
            is_outdated=False,
            status=PENDING,
            task_id='1'
        ).first()
        self.assertTrue(new_output)
        # cleanup
        output_2.delete()

    @mock.patch('django.core.cache.cache.set')
    def test_generate_species_statistical_model(self, mocked_set):
        mocked_set.side_effect = mocked_cache_op
        output = SpeciesModelOutputF.create(
            is_latest=True,
            is_outdated=True,
            status=PENDING,
            generated_on=datetime.datetime(2000, 8, 14, 8, 8, 8)
        )
        model = output.model
        pop_1 = AnnualPopulationF.create(
            taxon=output.taxon
        )
        # mock failed
        with requests_mock.Mocker() as m:
            json_response = {'error': 'Internal server error'}
            m.post(
                f'http://plumber:{PLUMBER_PORT}/statistical/api_{model.id}',
                json=json_response,
                headers={'Content-Type':'application/json'},
                status_code=500
            )
            generate_species_statistical_model(output.id)
            output.refresh_from_db()
            self.assertEqual(output.status, ERROR)
            self.assertIn('Internal server error', output.errors)
            self.assertFalse(output.is_outdated)
        # mock success
        with requests_mock.Mocker() as m:
            json_response = {'national_trend': 'abcde'}
            m.post(
                f'http://plumber:{PLUMBER_PORT}/statistical/api_{model.id}',
                json=json_response,
                headers={'Content-Type':'application/json'},
                status_code=200
            )
            generate_species_statistical_model(output.id)
            output.refresh_from_db()
            self.assertEqual(output.status, DONE)
            self.assertFalse(output.errors)
            self.assertFalse(output.is_outdated)
            self.assertTrue(output.output_file)
            self.assertTrue(
                output.output_file.storage.exists(output.output_file.name))
            mocked_set.assert_called_once()
            mocked_set.reset_mock()
            self.assertTrue(output.is_latest)
        # mock success for generic model
        generic_model = StatisticalModelF.create(
            taxon=None
        )
        taxon = TaxonF.create()
        output = SpeciesModelOutputF.create(
            model=generic_model,
            taxon=taxon,
            is_latest=True,
            is_outdated=True,
            status=PENDING,
            generated_on=datetime.datetime(2000, 8, 14, 8, 8, 8)
        )
        with requests_mock.Mocker() as m:
            json_response = {'national_trend': 'abcde'}
            m.post(
                f'http://plumber:{PLUMBER_PORT}/statistical/generic',
                json=json_response,
                headers={'Content-Type':'application/json'},
                status_code=200
            )
            generate_species_statistical_model(output.id)
            output.refresh_from_db()
            self.assertEqual(output.status, DONE)
            self.assertFalse(output.errors)
            self.assertFalse(output.is_outdated)
            self.assertTrue(output.output_file)
            self.assertTrue(
                output.output_file.storage.exists(output.output_file.name))
            mocked_set.assert_called_once()
            mocked_set.reset_mock()
            self.assertTrue(output.is_latest)

    def test_clean_old_model_output(self):
        output = SpeciesModelOutputF.create(
            is_latest=False,
            is_outdated=False,
            status=DONE,
            generated_on=datetime.datetime(2000, 8, 14, 8, 8, 8)
        )
        output_1 = SpeciesModelOutputF.create(
            is_latest=True,
            is_outdated=False,
            status=DONE,
            generated_on=datetime.datetime.now()
        )
        clean_old_model_output()
        self.assertFalse(SpeciesModelOutput.objects.filter(
            id=output.id
        ).exists())
        self.assertTrue(SpeciesModelOutput.objects.filter(
            id=output_1.id
        ).exists())

    @mock.patch('frontend.admin.'
                'generate_species_statistical_model.delay')
    def test_trigger_action(self, mocked_process):
        mocked_process.side_effect = mocked_process_func
        output = SpeciesModelOutputF.create(
            is_latest=False,
            is_outdated=False,
            status=DONE,
            generated_on=datetime.datetime(2000, 8, 14, 8, 8, 8),
            task_id=None
        )
        qs = SpeciesModelOutput.objects.filter(
            id=output.id
        )
        trigger_generate_species_statistical_model(DummyTask('1'), None, qs)
        mocked_process.assert_called_once()
        output.refresh_from_db()
        self.assertEqual(output.task_id, '1')

    def test_sort_output_type_categories(self):
        data_set = set()
        category_index_list = []
        result = sort_output_type_categories(data_set, category_index_list)
        self.assertFalse(result)
        data_set = set(
            [
                'stable (-2% to 2%)', 'steady decrease (2-5% pa)',
                'steady increase (2-5% pa)', 'increasing rapidly (>5% pa)'
            ]
        )
        OutputTypeCategoryIndex.objects.create(
            type='period',
            value='Steady Decrease',
            sort_index=1
        )
        OutputTypeCategoryIndex.objects.create(
            type='period',
            value='stable',
            sort_index=2
        )
        OutputTypeCategoryIndex.objects.create(
            type='period',
            value='steady Increase',
            sort_index=3
        )
        category_index_list = (
            OutputTypeCategoryIndex.objects.find_category_index(
                'test', 'period'
            )
        )
        result = sort_output_type_categories(data_set, category_index_list)
        self.assertTrue(result)
        self.assertEqual(
            result,
            ['increasing rapidly (>5% pa)', 'steady decrease (2-5% pa)',
             'stable (-2% to 2%)', 'steady increase (2-5% pa)']
        )

    def test_add_json_metadata(self):
        json_data = {
            NATIONAL_GROWTH: [
                {
                    "pop_size_cat": "large",
                    "pop_size_cat_label": "\u003E40",
                    "period": "Most recent 10 yrs",
                    "pop_change_cat": "stable (-2% to 2%)",
                    "count": 4,
                    "percentage": 50,
                    "count2": "n=4"
                },
                {
                    "pop_size_cat": "large",
                    "pop_size_cat_label": "\u003E40",
                    "period": "Most recent 10 yrs",
                    "pop_change_cat": "Steady Increase (2-5% pa)",
                    "count": 2,
                    "percentage": 25,
                    "count2": "n=2"
                },
                {
                    "pop_size_cat": "large",
                    "pop_size_cat_label": "\u003E40",
                    "period": "Most recent 10 yrs",
                    "pop_change_cat": "increasing Rapidly (\u003E5% pa)",
                    "count": 2,
                    "percentage": 25,
                    "count2": "n=2"
                },
                {
                    "pop_size_cat": "large",
                    "pop_size_cat_label": "\u003E40",
                    "period": "Most recent 5 yrs",
                    "pop_change_cat": "Stable (-2% to 2%)",
                    "count": 4,
                    "percentage": 50,
                    "count2": "n=4"
                }
            ]
        }
        OutputTypeCategoryIndex.objects.create(
            type='pop_change_cat',
            value='stable',
            sort_index=1
        )
        OutputTypeCategoryIndex.objects.create(
            type='pop_change_cat',
            value='steady Increase',
            sort_index=2
        )
        OutputTypeCategoryIndex.objects.create(
            type='pop_change_cat',
            value='Increasing Rapidly',
            sort_index=3
        )
        results = add_json_metadata(json_data)
        self.assertIn('metadata', results)
        self.assertIn(NATIONAL_GROWTH, results['metadata'])
        metadata = results['metadata'][NATIONAL_GROWTH]
        self.assertIn('period', metadata)
        self.assertIn('pop_change_cat', metadata)
        self.assertEqual(len(metadata['period']), 2)
        self.assertEqual(len(metadata['pop_change_cat']), 3)
        self.assertEqual(
            metadata['pop_change_cat'],
            ['stable (-2% to 2%)', 'steady increase (2-5% pa)',
             'increasing rapidly (\u003E5% pa)']
        )
