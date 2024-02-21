from django.test import TestCase, override_settings
import mock
import os
import uuid
import shutil
from datetime import datetime, timedelta
from django.conf import settings
from frontend.tasks.clean_download_data import clean_download_data


class MockStat(object):

    def __init__(self, mtime) -> None:
        self.st_mtime = mtime


def return_mock_state_1(*args, **kwargs):
    current_ts = datetime.now().timestamp() - 10
    return MockStat(current_ts)


def return_mock_state_2(*args, **kwargs):
    current_ts = datetime.now() - timedelta(days=3)
    return MockStat(current_ts.timestamp())


TEST_MEDIA_ROOT = '/home/web/media/media_test'


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class TestCleanDownloadData(TestCase):

    def setUp(self) -> None:
        self.uuid = str(uuid.uuid4())
        self.path = os.path.join(
            settings.MEDIA_ROOT,
            "download_data"
        )
        self.dir_path = os.path.join(self.path, self.uuid)
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path, exist_ok=True)
        self.file_path = os.path.join(self.dir_path, 'test.txt')
        with open(self.file_path, 'w') as out:
            out.write('tests')
        self.assertTrue(os.path.exists(self.file_path))

    def tearDown(self) -> None:
        if os.path.exists(TEST_MEDIA_ROOT):
            shutil.rmtree(TEST_MEDIA_ROOT)

    @mock.patch("os.stat")
    def test_clean_download_data(self, mocked_stat):
        # create new path that has been created, should return 0
        mocked_stat.reset_mock()
        mocked_stat.side_effect = return_mock_state_1
        total = clean_download_data()
        mocked_stat.assert_called_once()
        self.assertEqual(total, 0)
        # the dir is created 3 days ago, should be cleaned
        mocked_stat.reset_mock()
        mocked_stat.side_effect = return_mock_state_2
        total = clean_download_data()
        self.assertTrue(mocked_stat.called)
        self.assertEqual(total, 1)
