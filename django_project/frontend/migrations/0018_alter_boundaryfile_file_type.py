# Generated by Django 4.1.10 on 2023-09-14 02:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("frontend", "0017_boundarysearchrequest_used_parcels_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="boundaryfile",
            name="file_type",
            field=models.CharField(
                choices=[
                    ("GEOJSON", "GEOJSON"),
                    ("SHAPEFILE", "SHAPEFILE"),
                    ("GEOPACKAGE", "GEOPACKAGE"),
                    ("KML", "KML"),
                ],
                max_length=100,
            ),
        ),
    ]
