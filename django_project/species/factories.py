import factory
from species.models import TaxonRank, Taxon, ManagementStatus


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
