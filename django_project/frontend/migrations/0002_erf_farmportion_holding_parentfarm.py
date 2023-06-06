# Generated by Django 4.1.7 on 2023-06-06 07:00

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("frontend", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            "create schema if not exists layer",
            reverse_sql="drop schema if exists layer",
            elidable=False
        ),
        migrations.CreateModel(
            name="Erf",
            fields=[
                ("fid", models.AutoField(primary_key=True, serialize=False)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.GeometryField(
                        null=True, srid=3857
                    ),
                ),
                ("tag_value", models.CharField(blank=True, max_length=40, null=True)),
                ("id", models.CharField(blank=True, max_length=60, null=True)),
            ],
            options={
                "db_table": 'layer"."erf',
            },
        ),
        migrations.CreateModel(
            name="FarmPortion",
            fields=[
                ("fid", models.AutoField(primary_key=True, serialize=False)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.GeometryField(
                        null=True, srid=3857
                    ),
                ),
                ("tag_value", models.CharField(blank=True, max_length=40, null=True)),
                ("id", models.CharField(blank=True, max_length=60, null=True)),
            ],
            options={
                "db_table": 'layer"."farm_portion',
            },
        ),
        migrations.CreateModel(
            name="Holding",
            fields=[
                ("fid", models.AutoField(primary_key=True, serialize=False)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.GeometryField(
                        null=True, srid=3857
                    ),
                ),
                ("tag_value", models.CharField(blank=True, max_length=40, null=True)),
                ("id", models.CharField(blank=True, max_length=60, null=True)),
            ],
            options={
                "db_table": 'layer"."holding',
            },
        ),
        migrations.CreateModel(
            name="ParentFarm",
            fields=[
                ("fid", models.AutoField(primary_key=True, serialize=False)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.GeometryField(
                        null=True, srid=3857
                    ),
                ),
                ("tag_value", models.CharField(blank=True, max_length=40, null=True)),
                ("id", models.CharField(blank=True, max_length=60, null=True)),
            ],
            options={
                "db_table": 'layer"."parent_farm',
            },
        ),
    ]
