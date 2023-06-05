from django.test import TestCase
from occurrence.models import OrganismQuantityType, SurveyMethod
from occurrence.factories import OrganismQuantityTypeFactory, SurveyMethodFactory
from django.db.utils import IntegrityError


class OrganismQuantityTypeTestCase(TestCase):
    """organism quantity type test case"""

    @classmethod
    def setUpTestData(cls):
        """set up test data"""
        cls.quantityType = OrganismQuantityTypeFactory()

    def test_create_quantity_type(self):
        """test create organism quantity type"""
        self.assertTrue(isinstance(self.quantityType, OrganismQuantityType))
        self.assertEqual(OrganismQuantityType.objects.count(), 1)
        self.assertEqual(self.quantityType.name, "organism_quantity_type_0")

    def test_update_quantity_type(self):
        """test update quantity type"""
        self.quantityType.name = "organism_quantity_type_1"
        self.quantityType.save()
        self.assertEqual(
            OrganismQuantityType.objects.get(id=1).name,
            "organism_quantity_type_1",
        )

    def test_quantity_type_unique_name(self):
        """test unique names of quantity types"""
        with self.assertRaises(Exception) as raised:
            OrganismQuantityTypeFactory(name="organism_quantity_type_1")
            self.assertEqual(raised.exception, IntegrityError)

    def test_quantity_type_unique_sort_id(self):
        """test unique sort ids of quantity types"""
        with self.assertRaises(Exception) as raised:
            OrganismQuantityTypeFactory(sort_id=0)
            self.assertEqual(raised.exception, IntegrityError)

    def test_delete_quantity_type(self):
        """test delete quantity type"""
        self.quantityType.delete()
        self.assertEqual(OrganismQuantityType.objects.count(), 0)


class SurveyMethodTestCase(TestCase):
    """survey method test case"""

    @classmethod
    def setUpTestData(cls):
        """setup test data"""
        cls.survey_method = SurveyMethodFactory()

    def test_create_survey_method(self):
        """test create survey method"""
        self.assertTrue(
            isinstance(self.survey_method, SurveyMethod)
        )
        self.assertEqual(SurveyMethod.objects.count(), 1)
        self.assertEqual(self.survey_method.name, 'survey method 0')

    def test_update_survey_method(self):
        """test update survey method"""
        self.survey_method.name = 'survey method 1'
        self.survey_method.save()
        self.assertEqual(
            SurveyMethod.objects.get(id=1).name,
            'survey method 1',
        )

    def test_survey_method_unique_name_constraint(self):
        """test survey method unique name constraint"""
        with self.assertRaises(Exception) as raised:
            SurveyMethodFactory(name='survey method 0')
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_survey_method_unique_sort_id_constraint(self):
        """test survey method unique sort id constraint"""
        with self.assertRaises(Exception) as raised:
            SurveyMethodFactory(sort_id=0)
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_survey_method(self):
        """test delete survey method"""
        self.survey_method.delete()
        self.assertEqual(SurveyMethod.objects.count(), 0)