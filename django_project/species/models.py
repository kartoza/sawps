from django.db import models


class TaxonRank(models.Model):
    """taxon rank model"""

    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Taxon Rank'
        verbose_name_plural = 'Taxon Ranks'
        db_table = 'taxon_rank'
