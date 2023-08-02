import factory
from django.contrib.auth.models import User
from population_data.factories import (
    AnnualPopulationF,
    AnnualPopulationPerActivityFactory,
)
from species.models import (
    OwnedSpecies,
    Taxon,
    TaxonRank,
    TaxonSurveyMethod,
)


class TaxonRankFactory(factory.django.DjangoModelFactory):
    """taxon rank factory"""
    class Meta:
        model = TaxonRank

    name = factory.Sequence(lambda n: 'taxon_rank_%d' % n)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'password')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class TaxonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Taxon

    scientific_name = factory.Sequence(lambda n: f"Scientific Name {n}")
    common_name_varbatim = factory.Sequence(lambda n: f"Common Name {n}")
    colour_variant = factory.Faker('boolean')
    infraspecific_epithet = factory.Sequence(
        lambda n: f"Infraspecific Epithet {n}"
    )
    taxon_rank = factory.SubFactory('species.factories.TaxonRankFactory')
    parent = None
    show_on_front_page = factory.Faker('boolean')
    is_selected = factory.Faker('boolean')
    icon = factory.django.ImageField(filename='icon.jpg', color='blue')



class OwnedSpeciesFactory(factory.django.DjangoModelFactory):
    """Owned species factory."""
    class Meta:
        model = OwnedSpecies

    taxon = factory.SubFactory(TaxonFactory)
    user = factory.SubFactory(UserFactory)
    property = factory.SubFactory('property.factories.PropertyFactory')

    @factory.post_generation
    def create_annual_population(self, create, extracted, **kwargs):
        if not create:
            return

        AnnualPopulationF.create(
            year=factory.Faker('year'),
            owned_species=self,
            total=100,
            adult_male=50,
            adult_female=50,
            juvenile_male=30,
            juvenile_female=30,
            sub_adult_total=20,
            sub_adult_male=10,
            sub_adult_female=10,
            juvenile_total=40,
        )

    @factory.post_generation
    def create_annual_population_per_activity(self, create, *args):
        if not create:
            return

        AnnualPopulationPerActivityFactory.create(
            year=factory.Faker('year'),
            owned_species=self,
            total=100,
            adult_male=50,
            adult_female=50,
            juvenile_male=30,
            juvenile_female=30,
        )


class TaxonSurveyMethodF(factory.django.DjangoModelFactory):
    """Taxon Survey Method factory."""
    class Meta:
        model = TaxonSurveyMethod


class TaxonF(factory.django.DjangoModelFactory):
    """Taxon model factory."""
    class Meta:
        model = Taxon

    scientific_name = factory.Sequence(lambda n: 'scientific_%d' % n)
    common_name_varbatim = factory.Sequence(lambda n: 'common_%d' % n)
    colour_variant = False
    taxon_rank = factory.SubFactory(
        'species.factories.TaxonRankFactory'
    )
