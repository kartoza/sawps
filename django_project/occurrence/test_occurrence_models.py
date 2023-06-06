from django.test import TestCase
from occurrence.models import SurveyMethod, BasisOfRecord, SamplingSizeUnit
from occurrence.factories import SurveyMethodFactory, BasisOfRecordFactory, SamplingSizeUnitFactory
from django.db.utils import IntegrityError


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


class BasisOfRecordTestCase(TestCase):
    """basis of record testcase"""

    @classmethod
    def setUpTestData(self):
        """setup test data for basis of record test case"""
        self.basis_of_record = BasisOfRecordFactory()

    def test_create_basis_of_record(self):
        """test create basis of record"""
        self.assertTrue(isinstance(self.basis_of_record, BasisOfRecord))
        self.assertEqual(BasisOfRecord.objects.count(), 1)
        self.assertEqual(self.basis_of_record.name, 'basis of record 0')

    def test_update_basis_of_record(self):
        """test update basis of record"""
        self.basis_of_record.name = 'basis of record 1'
        self.basis_of_record.save()
        self.assertEqual(
            BasisOfRecord.objects.get(id=1).name, 'basis of record 1'
        )

    def test_basis_of_record_unique_name_constraint(self):
        """test basis of record unique name constraint"""
        with self.assertRaises(Exception) as raised:
            BasisOfRecordFactory(name='basis of record 1')
            self.assertEqual(IntegrityError, raised.exception)

    def test_basis_of_record_unique_sort_id_constraint(self):
        """test basis of record unique sort id constraint"""
        with self.assertRaises(Exception) as raised:
            BasisOfRecordFactory(sort_id=0)
            self.assertEqual(IntegrityError, raised.exception)

    def test_delete_basis_of_record(self):
        """test delete basis of record"""
        self.basis_of_record.delete()
        self.assertEqual(BasisOfRecord.objects.count(), 0)

        
class SamplingSizeUnitTestCase(TestCase):
    """sampling size unit testcase"""

    @classmethod
    def setUpTestData(cls):
        """setup test data"""
        cls.sampling_size_unit = SamplingSizeUnitFactory(unit='cm')

    def test_create_sampling_size_unit(self):
        """test create sampling size unit"""
        self.assertTrue(isinstance(self.sampling_size_unit, SamplingSizeUnit))
        self.assertEqual(SamplingSizeUnit.objects.count(), 1)
        self.assertEqual(self.sampling_size_unit.unit, 'cm')

    def test_update_sampling_size_unit(self):
        """test update sampling size unit"""
        self.sampling_size_unit.unit = 'mm'
        self.sampling_size_unit.save()
        self.assertEqual(SamplingSizeUnit.objects.get(id=1).unit, 'mm')

    def test_sampling_size_unit_unique_unit_constraint(self):
        """testing unique values for the unti"""
        with self.assertRaises(Exception) as raised:
            SamplingSizeUnitFactory(unit='mm')
            self.assertEqual(raised.exception, IntegrityError)

    def test_delete_sampling_size_unit(self):
        """test delete sampling size unit"""
        self.sampling_size_unit.delete()
        self.assertEqual(SamplingSizeUnit.objects.count(), 0)
