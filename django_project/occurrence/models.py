from django.contrib.gis.db import models


class SurveyMethod(models.Model):
    """Survey method model."""

    name = models.CharField(max_length=255, unique=True)
    sort_id = models.IntegerField(
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Survey method'
        verbose_name_plural = 'Survey methods'
        db_table = 'survey_method'


class SamplingSizeUnit(models.Model):
    """Sampling size unit model."""

    unit = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.unit

    class Meta:
        verbose_name = 'Sampling size unit'
        verbose_name_plural = 'Sampling size units'
        db_table = 'sampling_size_unit'
