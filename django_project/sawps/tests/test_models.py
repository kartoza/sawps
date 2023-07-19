from django.test import TestCase
from sawps.tests.model_factories import UploadSessionF
from sawps.models import UploadSession


class TestUploadSession(TestCase):
    """Test upload session model."""


    def test_create_new_upload_session(self):
        """Test creating new upload session."""
        upload_session = UploadSessionF.create(
            id=1,
            success_notes='success_message'
        )
        self.assertEqual(UploadSession.objects.count(), 1)
        self.assertEqual(
            upload_session.success_notes,
            'success_message'
        )

    def test_update_upload_session(self):
        """Test updating a upload session."""
        UploadSessionF.create(
            id=1,
            success_notes='success_message'
        )
        upload_session = UploadSession.objects.get(
            id=1
        )
        upload_session.success_notes='success message'
        upload_session.save()
        self.assertEqual(upload_session.success_notes, 'success message')

    def test_delete_role(self):
        """Test deleting upload session."""
        upload_session = UploadSessionF.create(
            id=1,
            success_notes='success_message'
        )
        upload_session.delete()
        self.assertEqual(UploadSession.objects.count(), 0)