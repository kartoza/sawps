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


class OccurrenceStatus(models.Model):
    """occurrence status model"""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Occurrence status'
        verbose_name_plural = 'Occurrence statuses'
        db_table = 'occurrence_status'