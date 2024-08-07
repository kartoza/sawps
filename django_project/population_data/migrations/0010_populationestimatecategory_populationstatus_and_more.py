# Generated by Django 4.1.10 on 2023-08-01 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("species", "0007_remove_ownedspecies_management_status_and_more"),
        (
            "population_data",
            "0009_remove_annualpopulation_unique_population_count_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="PopulationEstimateCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(default="", help_text="Name", unique=True)),
            ],
            options={
                "verbose_name": "Population Estimate Category",
                "verbose_name_plural": "Population Estimate Categories",
                "db_table": "population_estimate_category",
            },
        ),
        migrations.CreateModel(
            name="PopulationStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(default="", help_text="Name", unique=True)),
            ],
            options={
                "verbose_name": "Population Status",
                "verbose_name_plural": "Population Status",
                "db_table": "population_status",
            },
        ),
        migrations.DeleteModel(
            name="NatureOfPopulation",
        ),
        migrations.RemoveConstraint(
            model_name="annualpopulation",
            name="unique_population_count",
        ),
        migrations.RemoveField(
            model_name="annualpopulation",
            name="month",
        ),
        migrations.RemoveField(
            model_name="annualpopulation",
            name="pride",
        ),
        migrations.RemoveField(
            model_name="annualpopulationperactivity",
            name="month",
        ),
        migrations.DeleteModel(
            name="Month",
        ),
        migrations.AddField(
            model_name="annualpopulation",
            name="population_estimate_category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="population_data.populationestimatecategory",
            ),
        ),
        migrations.AddField(
            model_name="annualpopulation",
            name="population_status",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="population_data.populationstatus",
            ),
        ),
    ]
