from django.db import models


class OrganismQuantityType(models.Model):
    """organism quantity type model"""
    name = models.CharField(max_length=255, unique=True)
    sort_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "organism_quantity_type"

  
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

        