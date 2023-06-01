from django.db import models


class LoginStatus(models.Model):
    """user login status model"""

    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Login status"
        verbose_name_plural = "Login status"
