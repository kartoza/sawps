"""Test Frontend Models."""
from django.test import TestCase
from frontend.models import (
    ContextLayer,
    Erf,
    FarmPortion,
    Holding,
    ParentFarm
)
from frontend.tests.model_factories import (
    ContextLayerF,
    ErfF,
    FarmPortionF,
    HoldingF,
    ParentFarmF
)


class TestContextLayerModels(TestCase):

    def setUp(self) -> None:
        self.layer = ContextLayerF.create()

    def test_create_context_layer(self):
        self.assertTrue(
            isinstance(self.layer, ContextLayer)
        )
        self.assertEqual(ContextLayer.objects.count(), 1)

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
