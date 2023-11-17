import os
import mock
import datetime
import csv
import requests_mock
import json
from django.test import TestCase
from species.factories import TaxonF
from population_data.factories import AnnualPopulationF
from frontend.models.base_task import DONE, PROCESSING, ERROR, PENDING
from frontend.models.statistical import (
    NATIONAL_TREND,
    SpeciesModelOutput,
    CACHED_OUTPUT_TYPES
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
    generate_species_statistical_model
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
        taxon_a = TaxonF.create()
        taxon_b = TaxonF.create()
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
