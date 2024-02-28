# Generated by Django 4.1.13 on 2024-02-06 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("property", "0015_property_boundary_source"),
        ("frontend", "0032_boundarysearchrequest_errors_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="boundarysearchrequest",
            name="property_size_ha",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="boundarysearchrequest",
            name="province",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="property.province",
            ),
        ),
    ]
