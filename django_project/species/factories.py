import factory
from species.models import ManagementStatus, TaxonRank


class ManagementStatusFactory(factory.django.DjangoModelFactory):
    """Management status factory."""

    class Meta:
        model = ManagementStatus

    name = factory.Sequence(lambda n: 'management status_%d' % n)


class TaxonRankFactory(factory.django.DjangoModelFactory):
    """Taxon rank factory."""

    class Meta:
        model = TaxonRank

    name = factory.Sequence(lambda n: 'taxon_rank_%d' % n)
