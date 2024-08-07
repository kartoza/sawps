# Generated by Django 4.1.10 on 2023-10-29 21:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("frontend", "0026_spatialdatavaluemodel_frontend_sp_spatial_50ad24_idx"),
    ]

    operations = [
        migrations.CreateModel(
            name="MapSession",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("query_params", models.TextField(blank=True, default="", null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                (
                    "species",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                ("created_date", models.DateTimeField()),
                ("expired_date", models.DateTimeField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
