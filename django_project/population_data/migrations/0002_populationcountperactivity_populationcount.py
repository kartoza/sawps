# Generated by Django 4.1.7 on 2023-06-10 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("activity", "0001_initial"),
        ("species", "0001_species_models"),
        ("population_data", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PopulationCountPerActivity",
            fields=[
                ("year", models.DateField(primary_key=True, serialize=False)),
                ("total", models.IntegerField()),
                ("adult_male", models.IntegerField(blank=True, null=True)),
                ("adult_female", models.IntegerField(blank=True, null=True)),
                ("juvenile_male", models.IntegerField(blank=True, null=True)),
                ("juvenile_female", models.IntegerField(blank=True, null=True)),
                ("founder_population", models.BooleanField(blank=True, null=True)),
                (
                    "reintroduction_source",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("permit_number", models.IntegerField(blank=True, null=True)),
                ("activity_type", models.ManyToManyField(to="activity.activitytype")),
                (
                    "month",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="population_data.month",
                    ),
                ),
                ("owned", models.ManyToManyField(to="species.ownedspecies")),
            ],
            options={
                "verbose_name": "Population count per activities",
                "db_table": "population_count_per_activity",
            },
        ),
        migrations.CreateModel(
            name="PopulationCount",
            fields=[
                ("year", models.DateField(primary_key=True, serialize=False)),
                ("total", models.IntegerField()),
                ("adult_male", models.IntegerField(blank=True, null=True)),
                ("adult_female", models.IntegerField(blank=True, null=True)),
                ("juvenile_male", models.IntegerField(blank=True, null=True)),
                ("juvenile_female", models.IntegerField(blank=True, null=True)),
                ("sub_adult_total", models.IntegerField(blank=True, null=True)),
                ("sub_adult_male", models.IntegerField(blank=True, null=True)),
                ("sub_adult_female", models.IntegerField(blank=True, null=True)),
                ("juvenile_total", models.IntegerField(blank=True, null=True)),
                ("pride", models.IntegerField(blank=True, null=True)),
                (
                    "month",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="population_data.month",
                    ),
                ),
                ("owned", models.ManyToManyField(to="species.ownedspecies")),
            ],
            options={
                "verbose_name": "Population counts",
                "db_table": "population_count",
            },
        ),
    ]
