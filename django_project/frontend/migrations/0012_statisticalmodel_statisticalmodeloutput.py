# Generated by Django 4.1.10 on 2023-08-02 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("species", "0006_taxon_icon"),
        ("frontend", "0011_merge_20230710_0834"),
    ]

    operations = [
        migrations.CreateModel(
            name="StatisticalModel",
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
                ("name", models.CharField(max_length=256)),
                ("code", models.TextField()),
                (
                    "taxon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="species.taxon",
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StatisticalModelOutput",
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
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("national_trend", "National Trend"),
                            ("population_per_province", "Population Per Province"),
                            ("province_trend", "Province Trend"),
                            ("property_trend", "Property Trend"),
                            ("population_per_property", "Population Per Property"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="frontend.statisticalmodel",
                    ),
                ),
            ],
        ),
    ]
