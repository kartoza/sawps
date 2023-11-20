from django.test import TestCase
from frontend.apps import (
    create_clear_uploaded_boundary_files,
    create_clear_expired_map_session,
    create_clear_old_statistical_model_output,
    create_check_outdated_statistical_model
)


class FrontendConfigTestCase(TestCase):

    def test_ready(self):
        create_clear_uploaded_boundary_files()
        create_clear_expired_map_session()
        create_clear_old_statistical_model_output()
        create_check_outdated_statistical_model()
