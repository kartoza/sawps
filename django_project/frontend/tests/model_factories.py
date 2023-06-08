"""Model factories for frontend."""
import factory

from frontend.models.context_layer import ContextLayer
from frontend.models.parcels import (
    Erf,
    FarmPortion,
    Holding,
    ParentFarm
)


class ContextLayerF(factory.django.DjangoModelFactory):
    """Factory for ContextLayer Model."""
    class Meta:
        """Meta class Factory for ContextLayer Model."""
        model = ContextLayer

    name = factory.Sequence(
        lambda n: f'layer-{n}'
    )


class ErfF(factory.django.DjangoModelFactory):
    """Factory for Erf Model."""
    class Meta:
        """Meta class Factory for Erf Model."""
        model = Erf

    cname = factory.Sequence(
        lambda n: f'erf-{n}'
    )


class FarmPortionF(factory.django.DjangoModelFactory):
    """Factory for FarmPortion Model."""
    class Meta:
        """Meta class Factory for FarmPortion Model."""
        model = FarmPortion

    cname = factory.Sequence(
        lambda n: f'farm-portion-{n}'
    )


class HoldingF(factory.django.DjangoModelFactory):
    """Factory for Holding Model."""
    class Meta:
        """Meta class Factory for Holding Model."""
        model = Holding

    cname = factory.Sequence(
        lambda n: f'holding-{n}'
    )


class ParentFarmF(factory.django.DjangoModelFactory):
    """Factory for ParentFarm Model."""
    class Meta:
        """Meta class Factory for ParentFarm Model."""
        model = ParentFarm

    cname = factory.Sequence(
        lambda n: f'parent-farm-{n}'
    )
