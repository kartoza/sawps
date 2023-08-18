# Generated by Django 4.1.10 on 2023-08-18 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("property", "0005_remove_property_area_available_property_open"),
        ("stakeholder", "0010_alter_userroletype_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="organisation",
            name="national",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="organisation",
            name="province",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="property.province",
            ),
        ),
    ]
