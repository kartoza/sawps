# Generated by Django 4.1.13 on 2023-12-11 10:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("stakeholder", "0017_organisationinvites_user_organisationinvites_uuid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="organisation",
            name="data_use_permission",
        ),
    ]
