from django.db import models


class SurveyMethod(models.Model):
    """survey method model"""

    name = models.CharField(max_length=255, unique=True)
    sort_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Survey method'
        verbose_name_plural = 'Survey methods'
        db_table = 'survey_method'



class BasisOfRecord(models.Model):
    """basis of record model"""

    name = models.CharField(max_length=150, unique=True)
    sort_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Basis of record'
        verbose_name_plural = 'Basis of records'
        db_table = 'basis_of_record'