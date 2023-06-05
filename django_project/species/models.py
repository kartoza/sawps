from django.db import models

class ManagementStatus(models.Model):
    """ management status model """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Management Status"
        verbose_name_plural = "Management Status"
        db_table = 'management_status'