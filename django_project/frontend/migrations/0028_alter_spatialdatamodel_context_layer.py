# Generated by Django 4.1.10 on 2023-11-15 00:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("frontend", "0027_mapsession"),
    ]

    operations = [
        migrations.AlterField(
            model_name="spatialdatamodel",
            name="context_layer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="frontend.contextlayer",
            ),
        ),
    ]
