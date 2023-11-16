import mock
from django.test import TestCase
from frontend.utils.celery import cancel_task


def mocked_task_revoke(self, *args, **kwargs):
    return 1


def mocked_raise_exception_func(*args, **kwargs):
    raise Exception('Test')


class CeleryTestCase(TestCase):

    @mock.patch('core.celery.app.control.revoke')
    @mock.patch('frontend.utils.celery.AsyncResult.ready')
    def test_cancel_task_ready(self, mocked_ready, mocked_revoke):
        mocked_ready.return_value = False
        mocked_revoke.side_effect = mocked_task_revoke
        cancel_task('123')
        mocked_ready.assert_called_once()
        mocked_revoke.assert_called_once()

    @mock.patch('core.celery.app.control.revoke')
    @mock.patch('frontend.utils.celery.AsyncResult.ready')
    def test_cancel_task_ready_with_ex(self, mocked_ready, mocked_revoke):
        mocked_ready.return_value = False
        mocked_revoke.side_effect = mocked_raise_exception_func
        cancel_task('123')
        mocked_ready.assert_called_once()
        mocked_revoke.assert_called_once()

    @mock.patch('core.celery.app.control.revoke')
    @mock.patch('frontend.utils.celery.AsyncResult.ready')
    def test_cancel_task_not_ready(self, mocked_ready, mocked_revoke):
        mocked_ready.return_value = True
        mocked_revoke.side_effect = mocked_task_revoke
        cancel_task('123')
        mocked_ready.assert_called_once()
        mocked_revoke.assert_not_called()
