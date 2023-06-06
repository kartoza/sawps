import factory
from species.models import TaxonRank, Taxon


class TaxonRankFactory(factory.django.DjangoModelFactory):
    """taxon rank factory"""

    class Meta:
        model = TaxonRank

    name = factory.Sequence(lambda n: 'taxon_rank_%d' % n)
