# Generated by Django 4.1.10 on 2023-10-26 02:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("species", "0009_taxon_graph_icon"),
        ("property", "0007_property_short_code"),
        (
            "population_data",
            "0015_alter_annualpopulation_population_estimate_certainty",
        ),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="annualpopulationperactivity",
            name="unique_population_count_per_activity",
        ),
        migrations.AddField(
            model_name="annualpopulation",
            name="area_available_to_species",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="annualpopulation",
            name="property",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="property.property",
            ),
        ),
        migrations.AddField(
            model_name="annualpopulation",
            name="taxon",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="species.taxon",
            ),
        ),
        migrations.AddField(
            model_name="annualpopulation",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="annualpopulationperactivity",
            name="annual_population",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="population_data.annualpopulation",
            ),
        ),
        migrations.AddConstraint(
            model_name="annualpopulation",
            constraint=models.UniqueConstraint(
                fields=("year", "taxon", "property"), name="unique_population_count"
            ),
        ),
        migrations.AddConstraint(
            model_name="annualpopulationperactivity",
            constraint=models.UniqueConstraint(
                fields=("year", "annual_population", "activity_type"),
                name="unique_population_count_per_activity",
            ),
        ),
    ]