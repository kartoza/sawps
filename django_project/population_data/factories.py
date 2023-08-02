# -*- coding: utf-8 -*-


"""Test factories for population data package.
"""
import factory
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationAbstract,
    AnnualPopulationPerActivity,
    Certainty,
    CountMethod,
    OpenCloseSystem,
    PopulationStatus,
    PopulationEstimateCategory
)


class CountMethodFactory(factory.django.DjangoModelFactory):
    """Count method factory."""

    class Meta:
        """meta"""

        model = CountMethod

    name = "count method-1"


class AnnualPopulationAbstractFactory(factory.django.DjangoModelFactory):
    """Population count abstract factory."""

    class Meta:
        model = AnnualPopulationAbstract
        abstract = True

    year = factory.Sequence(lambda n: f"{n}")
    owned_species = factory.SubFactory("species.factories.OwnedSpeciesFactory")
    total = factory.Faker("random_int")
    adult_male = factory.Faker("random_int")
    adult_female = factory.Faker("random_int")
    juvenile_male = factory.Faker("random_int")
    juvenile_female = factory.Faker("random_int")


class AnnualPopulationF(AnnualPopulationAbstractFactory):
    """Population count factory."""

    class Meta:
        model = AnnualPopulation

    sub_adult_total = factory.Faker("random_int")
    sub_adult_male = factory.Faker("random_int")
    sub_adult_female = factory.Faker("random_int")
    juvenile_total = factory.Faker("random_int")


class AnnualPopulationPerActivityFactory(AnnualPopulationAbstractFactory):
    """Population count per activity factory."""

    class Meta:
        model = AnnualPopulationPerActivity

    activity_type = factory.SubFactory(
        "activity.factories.ActivityTypeFactory"
    )
    founder_population = True
    reintroduction_source = factory.Sequence(
        lambda n: f"reintroduction source-{n}"
    )
    intake_permit = factory.Faker("random_int")



class CertaintyF(factory.django.DjangoModelFactory):
    """Certainty factory."""

    class Meta:
        """meta"""

        model = Certainty


class OpenCloseSystemF(factory.django.DjangoModelFactory):
    """Open Close System factory."""

    class Meta:
        """meta"""

        model = OpenCloseSystem


class PopulationStatusF(factory.django.DjangoModelFactory):
    """Population Status factory."""

    class Meta:
        """meta"""

        model = PopulationStatus



class PopulationEstimateCategoryF(factory.django.DjangoModelFactory):
    """Population Status factory."""

    class Meta:
        """meta"""

        model = PopulationEstimateCategory