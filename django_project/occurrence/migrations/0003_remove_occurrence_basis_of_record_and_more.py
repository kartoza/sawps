# Generated by Django 4.1.7 on 2023-06-27 20:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("occurrence", "0002_alter_occurrence_basis_of_record_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="occurrence",
            name="basis_of_record",
        ),
        migrations.RemoveField(
            model_name="occurrence",
            name="occurrence_status",
        ),
        migrations.RemoveField(
            model_name="occurrence",
            name="ogranism_quantity_type",
        ),
        migrations.RemoveField(
            model_name="occurrence",
            name="organisation",
        ),
        migrations.RemoveField(
            model_name="occurrence",
            name="sampling_size_unit",
        ),
        migrations.RemoveField(
            model_name="occurrence",
            name="survey_method",
        ),
        migrations.RemoveField(
            model_name="occurrence",
            name="taxon",
        ),
        migrations.RemoveField(
            model_name="occurrence",
            name="user",
        ),
        migrations.DeleteModel(
            name="BasisOfRecord",
        ),
        migrations.DeleteModel(
            name="Occurrence",
        ),
        migrations.DeleteModel(
            name="OccurrenceStatus",
        ),
        migrations.DeleteModel(
            name="OrganismQuantityType",
        ),
    ]
