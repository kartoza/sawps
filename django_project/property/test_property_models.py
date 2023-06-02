from django.test import TestCase
import property.models as PropertryModels
import property.factories as PropertyFactories
from django.db.utils import IntegrityError


class ProvinceTestCase(TestCase):
    """province test case"""

    @classmethod
    def setUpTestData(cls):
        cls.province = PropertyFactories.ProvinceFactory()

    def test_create_province(self):
        'test create a province'
        self.assertTrue(isinstance(self.province, PropertryModels.Province))
        self.assertEqual(PropertryModels.Province.objects.count(), 1)
        self.assertEqual(self.province.name, 'Province 0')

    def test_update_province(self):
        'test update a province'
        self.province.name = 'Province 1'
        self.province.save()
        self.assertEqual(
            PropertryModels.Province.objects.get(id=1).name, 'Province 1'
        )

    def test_unique_province_name_constraint(self):
        'test unique province name constraint'
        with self.assertRaises(Exception) as raised:
            PropertyFactories.ProvinceFactory(name='Province 0')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_province(self):
        'test delete a province'
        self.province.delete()
        self.assertEqual(PropertryModels.Province.objects.count(), 0)
