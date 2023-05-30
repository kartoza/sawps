from django.test import TestCase
from activity.models import ActivityType
from activity.factories import ActivtyTypeFactory


class ActivityTypeTestCase(TestCase):
    """unit tests for ActivityType model"""

    def setUp(self) -> None:
        """setup test data"""
        self.activity_type = ActivtyTypeFactory()

    def test_activity_type_create(self):
        """test activity type create"""
        self.assertEqual(self.activity_type.name, 'Activity #0')
        self.assertEqual(self.activity_type.recruitment, True)
        self.assertEqual(ActivityType.objects.count(), 1)

    def test_activity_type_update(self):
        """test activity type update"""
        self.activity_type.name = 'Activity #1'
        self.activity_type.recruitment = False
        self.activity_type.save()
        self.assertEqual(self.activity_type.name, 'Activity #1')
        self.assertEqual(self.activity_type.recruitment, False)

    def test_activity_type_delete(self):
        """test activity type delete"""
        self.activity_type.delete()
        self.assertEqual(ActivityType.objects.count(), 0)
