# Generated by Django 4.1.10 on 2023-10-20 01:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("frontend", "0026_mapsession"),
    ]

    operations = [
        migrations.AddField(
            model_name="mapsession",
            name="species",
            field=models.CharField(blank=True, default="", max_length=255, null=True),
        )
    ]
