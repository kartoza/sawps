import factory
from species.models import TaxonRank


class TaxonRankFactory(factory.django.DjangoModelFactory):
    """taxon rank factory"""

    class Meta:
        model = TaxonRank

    name = factory.Sequence(lambda n: 'taxon_rank_%d' % n)