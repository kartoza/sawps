import os
from django.test import TestCase
import mock
import requests_mock
from collections import OrderedDict
from species.factories import TaxonF, TaxonRankFactory
from frontend.models.statistical import (
    NATIONAL_TREND,
    PROVINCE_TREND,
    CACHED_OUTPUT_TYPES,
    SpeciesModelOutput
)
from frontend.utils.statistical_model import (
    write_plumber_file,
    write_plumber_data, 
    remove_plumber_data,
    execute_statistical_model,
    PLUMBER_PORT,
    plumber_health_check,
    kill_r_plumber_process,
    spawn_r_plumber,
    store_species_model_output_cache,
    clear_species_model_output_cache,
    mark_model_output_as_outdated_by_model,
    mark_model_output_as_outdated_by_species_list,
    init_species_model_output_from_generic_model,
    init_species_model_output_from_non_generic_model
)
from frontend.utils.process import write_pidfile
from frontend.tests.model_factories import (
    StatisticalModelF,
    SpeciesModelOutputF,
    StatisticalModelOutputF
)


def mocked_cache_get(self, *args, **kwargs):
    return OrderedDict({
        'test': '12345'
    })


def mocked_clear_cache(self, *args, **kwargs):
    return 1


def mocked_os_kill(self, *args, **kwargs):
    return 1


def find_r_line_code(lines, code):
    filtered = [line for line in lines if code in line]
    return len(filtered) > 0


class DummyProcess:
    def __init__(self, pid):
        self.pid = pid


def mocked_process(*args, **kwargs):
    return DummyProcess(1)


class TestStatisticalUtils(TestCase):


    def test_plumber_health_check(self):
        with requests_mock.Mocker() as m:
            json_response = {'echo': 'ok'}
            m.get(
                f'http://0.0.0.0:{PLUMBER_PORT}/statistical/echo',
                json=json_response,
                headers={'Content-Type':'application/json'},
                status_code=200
            )
            is_running = plumber_health_check(max_retry=1)
            self.assertTrue(is_running)
        with requests_mock.Mocker() as m:
            json_response = {'echo': 'ok'}
            m.get(
                f'http://0.0.0.0:{PLUMBER_PORT}/statistical/echo',
                json=json_response,
                headers={'Content-Type':'application/json'},
                status_code=400
            )
            is_running = plumber_health_check(max_retry=1)
            self.assertFalse(is_running)
    
    @mock.patch('subprocess.Popen',
                mock.Mock(side_effect=mocked_process))
    def test_spawn_r_plumber(self):
        with requests_mock.Mocker() as m:
            json_response = {'echo': 'ok'}
            m.get(
                f'http://0.0.0.0:{PLUMBER_PORT}/statistical/echo',
                json=json_response,
                headers={'Content-Type':'application/json'},
                status_code=200
            )
            process = spawn_r_plumber()
        self.assertEqual(process.pid, 1)

    @mock.patch('os.kill')
    def test_kill_r_plumber_process(self, mocked_os):
        mocked_os.side_effect = mocked_os_kill
        pid_path = '/tmp/plumber.pid'
        write_pidfile(26, pid_path)
        kill_r_plumber_process()
        self.assertEqual(mocked_os.call_count, 1)

    def test_execute_statistical_model(self):
        data_filepath = '/home/web/plumber_data/test.csv'
        model = StatisticalModelF.create()
        with requests_mock.Mocker() as m:
            json_response = {'national_trend': 'abcde'}
            m.post(
                f'http://plumber:{PLUMBER_PORT}/statistical/api_{model.id}',
                json=json_response,
                headers={'Content-Type':'application/json'},
                status_code=200
            )
            is_success, response = execute_statistical_model(data_filepath,
                                                             model.taxon,
                                                             model)
            self.assertTrue(is_success)
            self.assertEqual(response, json_response)
        with requests_mock.Mocker() as m:
            json_response = {'error': 'Internal server error'}
            m.post(
                f'http://plumber:{PLUMBER_PORT}/statistical/api_{model.id}',
                json=json_response,
                headers={'Content-Type':'application/json'},
                status_code=500
            )
            is_success, response = execute_statistical_model(data_filepath,
                                                             model.taxon,
                                                             model)
            self.assertFalse(is_success)
            self.assertEqual('Internal server error', response['error'])
        with requests_mock.Mocker() as m:
            data_response = 'Test'
            m.post(
                f'http://plumber:{PLUMBER_PORT}/statistical/api_{model.id}',
                json=data_response,
                headers={'Content-Type':'text/plain'},
                status_code=500
            )
            is_success, response = execute_statistical_model(data_filepath,
                                                             model.taxon,
                                                             model)
            self.assertFalse(is_success)
            self.assertEqual('Invalid response content type: text/plain',
                             response)

    def test_write_plumber_file(self):
        taxon = TaxonF.create()
        model = StatisticalModelF.create(
            taxon=None
        )
        model = StatisticalModelF.create(
            taxon=taxon
        )
        StatisticalModelOutputF.create(
            model=model,
            type=NATIONAL_TREND,
            variable_name='test_var1'
        )
        StatisticalModelOutputF.create(
            model=model,
            type=PROVINCE_TREND,
            variable_name=None
        )
        r_file_path = write_plumber_file(
            os.path.join(
                '/home/web/plumber_data',
                'plumber_test.R'
            )
        )
        with open(r_file_path, 'r') as f:
            lines = f.readlines()
        self.assertTrue(find_r_line_code(lines, '@get /statistical/echo'))
        self.assertTrue(
            find_r_line_code(lines, '@post /statistical/generic'))
        self.assertTrue(
            find_r_line_code(lines,
                             f'@post /statistical/api_{str(model.id)}')
        )
        if os.path.exists(r_file_path):
            os.remove(r_file_path)

    def test_manage_plumber_data(self):
        headers = ['province', 'count_total']
        csv_data = [
            ['Gauteng', 10],
            ['Western Cape', 20]
        ]
        file_path = write_plumber_data(headers, csv_data)
        self.assertTrue(os.path.exists(file_path))
        remove_plumber_data(file_path)
        self.assertFalse(os.path.exists(file_path))

    @mock.patch('django.core.cache.cache.set')
    @mock.patch('django.core.cache.cache.delete')
    def test_species_model_output_cache(self, mocked_clear, mocked_set):
        mocked_clear.side_effect = mocked_clear_cache
        mocked_set.side_effect = mocked_clear_cache
        latest_model = SpeciesModelOutputF.create(
            is_latest=True
        )
        store_species_model_output_cache(latest_model, {
            NATIONAL_TREND: 'test',
            'abcdef': 'test123'
        })
        mocked_set.assert_called_once()
        clear_species_model_output_cache(latest_model)
        self.assertEqual(mocked_clear.call_count, len(CACHED_OUTPUT_TYPES))

    def test_mark_model_output_as_outdated(self):
        model = StatisticalModelF.create()
        output = SpeciesModelOutputF.create(
            model=model,
            is_latest=True,
            is_outdated=False
        )
        mark_model_output_as_outdated_by_model(model)
        output.refresh_from_db()
        self.assertTrue(output.is_outdated)
        output.is_outdated = False
        output.save()
        mark_model_output_as_outdated_by_species_list([output.taxon.id])
        output.refresh_from_db()
        self.assertTrue(output.is_outdated)

    def test_init_species_model_output(self):
        species_rank = TaxonRankFactory.create(
            name='Species'
        )
        family_rank = TaxonRankFactory.create(
            name='Family'
        )
        taxon_a = TaxonF.create(
            taxon_rank=species_rank
        )
        taxon_b = TaxonF.create(
            taxon_rank=species_rank
        )
        taxon_c = TaxonF.create(
            taxon_rank=family_rank
        )
        non_generic_model = StatisticalModelF.create(
            taxon=taxon_a
        )
        generic_model = StatisticalModelF.create(
            taxon=None
        )
        init_species_model_output_from_generic_model(generic_model)
        output_1 = SpeciesModelOutput.objects.filter(model=generic_model)
        self.assertEqual(output_1.count(), 1)
        output_1 = output_1.first()
        self.assertEqual(output_1.taxon.id, taxon_b.id)
        non_generic_model_2 = StatisticalModelF.create(
            taxon=taxon_b
        )
        init_species_model_output_from_non_generic_model(non_generic_model_2)
        output_1 = SpeciesModelOutput.objects.filter(model=generic_model)
        self.assertEqual(output_1.count(), 0)
        output_2 = SpeciesModelOutput.objects.filter(
            model=non_generic_model_2)
        self.assertEqual(output_2.count(), 1)
        output_2 = output_2.first()
        self.assertEqual(output_2.taxon.id, taxon_b.id)
