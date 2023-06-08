from django.test import TestCase
from occurrence.models import (
    OrganismQuantityType,
    SurveyMethod,
    OccurrenceStatus,
    BasisOfRecord,
    SamplingSizeUnit,
)
from occurrence.factories import (
    OrganismQuantityTypeFactory,
    SurveyMethodFactory,
)
from occurrence.factories import (
    OccurrenceStatusFactory,
    BasisOfRecordFactory,
    SamplingSizeUnitFactory,
)
from django.db.utils import IntegrityError


class OrganismQuantityTypeTestCase(TestCase):
    """Organism quantity type test case."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.quantityType = OrganismQuantityTypeFactory()

    def test_create_quantity_type(self):
        """Test create organism quantity type."""
        self.assertTrue(isinstance(self.quantityType, OrganismQuantityType))
        self.assertEqual(OrganismQuantityType.objects.count(), 1)
        self.assertEqual(self.quantityType.name, 'organism_quantity_type_0')

    def test_update_quantity_type(self):
        """Test update quantity type."""
        self.quantityType.name = 'organism_quantity_type_1'
        self.quantityType.save()
        self.assertEqual(
            OrganismQuantityType.objects.get(id=1).name,
            'organism_quantity_type_1',
        )

    def test_quantity_type_unique_name(self):
        """Test unique names of quantity types."""
        with self.assertRaises(Exception) as raised:
            OrganismQuantityTypeFactory(name='organism_quantity_type_1')
            self.assertEqual(raised.exception, IntegrityError)

    def test_quantity_type_unique_sort_id(self):
        """Test unique sort ids of quantity types."""
        with self.assertRaises(Exception) as raised:
            OrganismQuantityTypeFactory(sort_id=0)
            self.assertEqual(raised.exception, IntegrityError)

    def test_delete_quantity_type(self):
        """Test delete quantity type."""
        self.quantityType.delete()
        self.assertEqual(OrganismQuantityType.objects.count(), 0)


class SurveyMethodTestCase(TestCase):
    """Survey method test case."""

    @classmethod
    def setUpTestData(cls):
        """Setup test data."""
        cls.survey_method = SurveyMethodFactory()

    def test_create_survey_method(self):
        """Test create survey method."""
        self.assertTrue(isinstance(self.survey_method, SurveyMethod))
        self.assertEqual(SurveyMethod.objects.count(), 1)
        self.assertEqual(self.survey_method.name, 'survey method 0')

    def test_update_survey_method(self):
        """Test update survey method."""
        self.survey_method.name = 'survey method 1'
        self.survey_method.save()
        self.assertEqual(
            SurveyMethod.objects.get(id=1).name,
            'survey method 1',
        )

    def test_survey_method_unique_name_constraint(self):
        """Test survey method unique name constraint."""
        with self.assertRaises(Exception) as raised:
            SurveyMethodFactory(name='survey method 0')
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_survey_method_unique_sort_id_constraint(self):
        """Test survey method unique sort id constraint."""
        with self.assertRaises(Exception) as raised:
            SurveyMethodFactory(sort_id=0)
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_survey_method(self):
        """Test delete survey method."""
        self.survey_method.delete()
        self.assertEqual(SurveyMethod.objects.count(), 0)


class OccurrenceStatusTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Setup test data for occurrence status testcase."""
        cls.occurrence_status = OccurrenceStatusFactory()

    def test_create_occurrence_status(self):
        """Test create occurrence status."""
        self.assertTrue(isinstance(self.occurrence_status, OccurrenceStatus))
        self.assertEqual(OccurrenceStatus.objects.count(), 1)
        self.assertEqual(self.occurrence_status.name, 'occurrence status 0')

    def test_update_occurrence_status(self):
        """Test update occurrence status."""
        self.occurrence_status.name = 'occurrence status 1'
        self.occurrence_status.save()
        self.assertEqual(
            OccurrenceStatus.objects.get(id=1).name,
            'occurrence status 1',
        )

    def test_occurrence_status_unique_name_constraint(self):
        """Test occurrence status unique name constraint."""
        with self.assertRaises(Exception) as raised:
            OccurrenceStatusFactory(name='occurrence status 0')
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_occurrence_status(self):
        """Test delete occurrence status."""
        self.occurrence_status.delete()
        self.assertEqual(OccurrenceStatus.objects.count(), 0)


class BasisOfRecordTestCase(TestCase):
    """Basis of record testcase."""

    @classmethod
    def setUpTestData(self):
        """Setup test data for basis of record test case."""
        self.basis_of_record = BasisOfRecordFactory()

    def test_create_basis_of_record(self):
        """Test create basis of record."""
        self.assertTrue(isinstance(self.basis_of_record, BasisOfRecord))
        self.assertEqual(BasisOfRecord.objects.count(), 1)
        self.assertEqual(self.basis_of_record.name, 'basis of record 0')

    def test_update_basis_of_record(self):
        """Test update basis of record."""
        self.basis_of_record.name = 'basis of record 1'
        self.basis_of_record.save()
        self.assertEqual(
            BasisOfRecord.objects.get(id=1).name, 'basis of record 1'
        )

    def test_basis_of_record_unique_name_constraint(self):
        """Test basis of record unique name constraint."""
        with self.assertRaises(Exception) as raised:
            BasisOfRecordFactory(name='basis of record 1')
            self.assertEqual(IntegrityError, raised.exception)

    def test_basis_of_record_unique_sort_id_constraint(self):
        """Test basis of record unique sort id constraint."""
        with self.assertRaises(Exception) as raised:
            BasisOfRecordFactory(sort_id=0)
            self.assertEqual(IntegrityError, raised.exception)

    def test_delete_basis_of_record(self):
        """Test delete basis of record."""
        self.basis_of_record.delete()
        self.assertEqual(BasisOfRecord.objects.count(), 0)


class SamplingSizeUnitTestCase(TestCase):
    """Sampling size unit testcase."""

    @classmethod
    def setUpTestData(cls):
        """Setup test data."""
        cls.sampling_size_unit = SamplingSizeUnitFactory(unit='cm')

    def test_create_sampling_size_unit(self):
        """Test create sampling size unit."""
        self.assertTrue(isinstance(self.sampling_size_unit, SamplingSizeUnit))
        self.assertEqual(SamplingSizeUnit.objects.count(), 1)
        self.assertEqual(self.sampling_size_unit.unit, 'cm')

    def test_update_sampling_size_unit(self):
        """Test update sampling size unit."""
        self.sampling_size_unit.unit = 'mm'
        self.sampling_size_unit.save()
        self.assertEqual(SamplingSizeUnit.objects.get(id=1).unit, 'mm')

    def test_sampling_size_unit_unique_unit_constraint(self):
        """Testing unique values for the unit."""
        with self.assertRaises(Exception) as raised:
            SamplingSizeUnitFactory(unit='mm')
            self.assertEqual(raised.exception, IntegrityError)

    def test_delete_sampling_size_unit(self):
        """Test delete sampling size unit."""
        self.sampling_size_unit.delete()
        self.assertEqual(SamplingSizeUnit.objects.count(), 0)
