import factory
from species.models import TaxonRank, Taxon, ManagementStatus, OwnedSpecies
from species.models import Taxon
from django.contrib.auth.models import User

class TaxonRankFactory(factory.django.DjangoModelFactory):
    """taxon rank factory"""
    class Meta:
        model = TaxonRank

    name = factory.Sequence(lambda n: 'taxon_rank_%d' % n)


class ManagementStatusFactory(factory.django.DjangoModelFactory):
    """Management status factory."""
    class Meta:
        model = ManagementStatus

    name = factory.Sequence(lambda n: 'management status_%d' % n)



class OwnedSpeciesFactory(factory.django.DjangoModelFactory):
    """Owned species factory."""
    class Meta:
        model = OwnedSpecies
    
    management_status = factory.SubFactory(ManagementStatusFactory)
    nature_of_population = factory.SubFactory('population_data.factories.NatureOfPopulationFactory')
    count_method = factory.SubFactory('population_data.factories.CountMethodFactory')
    property = factory.SubFactory('property.factories.PropertyFactory')
