# Generated by Django 4.1.10 on 2023-09-02 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("stakeholder", "0011_userprofile_allowing_sanbi_to_expose_data_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="current_organisation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="stakeholder.organisation",
            ),
        ),
    ]
