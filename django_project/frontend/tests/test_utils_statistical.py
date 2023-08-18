import os
from django.test import TestCase
import mock
import requests_mock
from species.factories import TaxonF
from frontend.models.statistical import NATIONAL_TREND, PROVINCE_TREND
from frontend.utils.statistical_model import (
    write_plumber_file,
    write_plumber_data, 
    remove_plumber_data,
    get_statistical_model_output_cache_key,
    execute_statistical_model,
    PLUMBER_PORT,
    plumber_health_check,
    kill_r_plumber_process,
    spawn_r_plumber,
    clear_statistical_model_output_cache
)
from frontend.utils.process import write_pidfile
from frontend.tests.model_factories import StatisticalModelF


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


class DummyCacheClient:
    def __init__(self, results = []):
        self.results = results

    def keys(self, key_pattern):
        return self.results


class DummyCacheHandler:
    def __init__(self, results = []):
        self.results = results
        self._cache = self

    def get_client(self):
        return DummyCacheClient(self.results)
    
    def delete(self, key):
        return 1


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

    @mock.patch(
        'frontend.utils.statistical_model.'
        'clear_statistical_model_output_cache',
        mock.Mock(side_effect=mocked_clear_cache)
    )
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
            self.assertFalse(response)

    @mock.patch(
        'frontend.utils.statistical_model.'
        'clear_statistical_model_output_cache',
        mock.Mock(side_effect=mocked_clear_cache)
    )
    def test_write_plumber_file(self):
        taxon = TaxonF.create()
        model = StatisticalModelF.create(
            taxon=None
        )
        model = StatisticalModelF.create(
            taxon=taxon
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

    def test_get_statistical_model_output_cache_key(self):
        taxon = TaxonF.create()
        cache_key = get_statistical_model_output_cache_key(
            taxon, NATIONAL_TREND)
        self.assertEqual(cache_key, f'species-{taxon.id}-national-trend')
        cache_key = get_statistical_model_output_cache_key(
            taxon, PROVINCE_TREND, 'Gauteng')
        self.assertEqual(
            cache_key, f'species-{taxon.id}-province-trend-gauteng')

    @mock.patch('frontend.utils.statistical_model.cache')
    def test_clear_statistical_model_output_cache(self, mocked_cached):
        mocked_cached.return_value = DummyCacheHandler()
        taxon = TaxonF.create()
        clear_statistical_model_output_cache(taxon)
        clear_statistical_model_output_cache(None)
