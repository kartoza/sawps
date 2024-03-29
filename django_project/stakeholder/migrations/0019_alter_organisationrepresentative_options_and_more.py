# Generated by Django 4.1.13 on 2024-02-13 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stakeholder", "0018_remove_organisation_data_use_permission"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="organisationrepresentative",
            options={
                "verbose_name": "Organisation manager",
                "verbose_name_plural": "Organisation managers",
            },
        ),
        migrations.AlterModelOptions(
            name="organisationuser",
            options={
                "verbose_name": "Organisation member",
                "verbose_name_plural": "Organisation members",
            },
        ),
    ]
