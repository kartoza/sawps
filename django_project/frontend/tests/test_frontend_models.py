"""Test Frontend Models."""
from django.test import TestCase
from frontend.models import (
    ContextLayer,
    Erf,
    FarmPortion,
    Holding,
    ParentFarm,
    UploadSpeciesCSV, Layer,
    Spreadsheet,
)
from frontend.tests.model_factories import (
    ContextLayerF,
    ErfF,
    FarmPortionF,
    HoldingF,
    ParentFarmF,
    UploadSpeciesCSVF, LayerF, ContextLayerLegendF,
    SpreadsheetModelF,
)
from property.factories import PropertyFactory
from core.settings.utils import absolute_path




class TestContextLayerModels(TestCase):

    def setUp(self) -> None:
        self.layer = ContextLayerF.create(
            name='context_layer_1'
        )

    def test_create_context_layer(self):
        self.assertTrue(
            isinstance(self.layer, ContextLayer)
        )
        self.assertTrue(
            str(self.layer),
            'context_layer_1'
        )
        self.assertEqual(ContextLayer.objects.count(), 1)

    def test_create_context_layer_legend(self):
        legend = ContextLayerLegendF.create(
            name='context-layer-legend-1',
            layer=self.layer
        )
        self.assertTrue(
            str(legend),
            'context-layer-legend-1'
        )

    def test_create_layer(self):
        layer = LayerF.create(
            context_layer=self.layer,
            name='layer-1'
        )
        self.assertTrue(
            str(layer),
            'layer-1'
        )
        self.assertGreaterEqual(
            Layer.objects.filter(name='layer-1').count(), 1)

    def test_update_context_layer(self):
        self.layer.name = 'Updated Layer'
        self.layer.save()
        self.assertEqual(
            ContextLayer.objects.get(id=self.layer.id).name,
            self.layer.name
        )

    def test_delete_context_layer(self):
        self.layer.delete()
        self.assertEqual(ContextLayer.objects.count(), 0)


class TestErfModels(TestCase):

    def setUp(self) -> None:
        self.layer = ErfF.create()

    def test_create_context_layer(self):
        self.assertTrue(
            isinstance(self.layer, Erf)
        )
        self.assertEqual(Erf.objects.count(), 1)

    def test_update_context_layer(self):
        self.layer.tag_value = 'Updated Layer'
        self.layer.save()
        self.assertEqual(
            Erf.objects.get(id=self.layer.id).tag_value,
            self.layer.tag_value
        )

    def test_delete_context_layer(self):
        self.layer.delete()
        self.assertEqual(Erf.objects.count(), 0)


class TestFarmPortionModels(TestCase):

    def setUp(self) -> None:
        self.layer = FarmPortionF.create()

    def test_create_context_layer(self):
        self.assertTrue(
            isinstance(self.layer, FarmPortion)
        )
        self.assertEqual(FarmPortion.objects.count(), 1)

    def test_update_context_layer(self):
        self.layer.tag_value = 'Updated Layer'
        self.layer.save()
        self.assertEqual(
            FarmPortion.objects.get(id=self.layer.id).tag_value,
            self.layer.tag_value
        )

    def test_delete_context_layer(self):
        self.layer.delete()
        self.assertEqual(FarmPortion.objects.count(), 0)


class TestHoldingModels(TestCase):

    def setUp(self) -> None:
        self.layer = HoldingF.create()

    def test_create_context_layer(self):
        self.assertTrue(
            isinstance(self.layer, Holding)
        )
        self.assertEqual(Holding.objects.count(), 1)

    def test_update_context_layer(self):
        self.layer.tag_value = 'Updated Layer'
        self.layer.save()
        self.assertEqual(
            Holding.objects.get(id=self.layer.id).tag_value,
            self.layer.tag_value
        )

    def test_delete_context_layer(self):
        self.layer.delete()
        self.assertEqual(Holding.objects.count(), 0)


class TestParentFarmModels(TestCase):

    def setUp(self) -> None:
        self.layer = ParentFarmF.create()

    def test_create_context_layer(self):
        self.assertTrue(
            isinstance(self.layer, ParentFarm)
        )
        self.assertEqual(ParentFarm.objects.count(), 1)

    def test_update_context_layer(self):
        self.layer.tag_value = 'Updated Layer'
        self.layer.save()
        self.assertEqual(
            ParentFarm.objects.get(id=self.layer.id).tag_value,
            self.layer.tag_value
        )

    def test_delete_context_layer(self):
        self.layer.delete()
        self.assertEqual(ParentFarm.objects.count(), 0)


class TestUploadSpeciesCSV(TestCase):
    """Test upload species csv model."""

    def setUp(self) -> None:
        self.property = PropertyFactory()

    def test_create_new_upload_species_csv(self):
        """Test creating new upload species csv."""
        upload_species_csv = UploadSpeciesCSVF.create(
            id=1,
            success_notes='success_message',
            property=self.property
        )
        self.assertEqual(UploadSpeciesCSV.objects.count(), 1)
        self.assertEqual(
            upload_species_csv.success_notes,
            'success_message'
        )

    def test_update_upload_species_csv(self):
        """Test updating a upload species csv."""
        UploadSpeciesCSVF.create(
            id=1,
            success_notes='success_message',
            property=self.property
        )
        upload_species_csv = UploadSpeciesCSV.objects.get(
            id=1
        )
        upload_species_csv.success_notes = 'success message'
        upload_species_csv.save()
        self.assertEqual(upload_species_csv.success_notes, 'success message')

    def test_delete_upload_species_csv(self):
        """Test deleting upload species csv."""
        upload_species_csv = UploadSpeciesCSVF.create(
            id=1,
            success_notes='success_message',
            property=self.property
        )
        upload_species_csv.delete()
        self.assertEqual(UploadSpeciesCSV.objects.count(), 0)


class TestSpreadsheet(TestCase):
    """Test spreadsheet model."""

    def test_create_new_spreadsheet(self):
        """Test creating new spreadsheet."""
        spreadsheet_path = absolute_path(
            'frontend', 'tests',
            'csv', 'excel_error_property.xlsx')
        SpreadsheetModelF.create(
            id=1,
            name='template',
            spreadsheet_file=spreadsheet_path
        )
        self.assertEqual(Spreadsheet.objects.count(), 1)
        spreadsheet = Spreadsheet.objects.get(
            id=1
        )
        self.assertEqual(
            spreadsheet.name,
            'template'
        )
        self.assertEqual(
            spreadsheet.spreadsheet_file.url,
            'spreadsheet/excel_error_property.xlsx'
        )

    def test_update_spreadsheet(self):
        """Test updating a upload species csv."""
        SpreadsheetModelF.create(
            id=1,
            name='template',
        )
        spreadsheet = Spreadsheet.objects.get(
            id=1
        )
        spreadsheet.name = 'template_1'
        spreadsheet.save()
        self.assertEqual(spreadsheet.name, 'template_1')

    def test_delete_spreadsheet(self):
        """Test deleting upload species csv."""
        spreadsheet = SpreadsheetModelF.create(
            id=1,
            name='template',
        )
        spreadsheet.delete()
        self.assertEqual(Spreadsheet.objects.count(), 0)
