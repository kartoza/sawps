# Generated by Django 4.1.10 on 2023-10-17 12:42

from django.db import migrations, models
from frontend.utils.organisation import get_abbreviation


def create_short_code(apps, schema_editor):
    Organisation = apps.get_model('stakeholder', 'Organisation')

    for idx, organisation_obj in enumerate(Organisation.objects.all().order_by('id')):
        province = get_abbreviation(organisation_obj.province.name) if organisation_obj.province else ''
        organisation = get_abbreviation(organisation_obj.name)
        digit = 1000 + idx + 1
        organisation_obj.short_code = f"{province}{organisation}{digit}"
        organisation_obj.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("stakeholder", "0014_alter_organisationinvites_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="organisation",
            name="short_code",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.RunPython(create_short_code, reverse_func)
    ]
