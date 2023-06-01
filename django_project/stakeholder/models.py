from django.db import models

class UserTitle(models.Model):
    """user title model"""

    name = models.CharField(unique=True, max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'