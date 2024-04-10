"""Class for managing spreadsheet.
"""
from django.db import models

FILE_STORAGE = 'spreadsheet'


class Spreadsheet(models.Model):
    """Spreadsheet template.
    """

    name = models.CharField(
        max_length=200,
        default='',
        blank=True
    )

    spreadsheet_file = models.FileField(
        upload_to=FILE_STORAGE,
        max_length=512,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Spreadsheet"
