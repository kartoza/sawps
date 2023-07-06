# Generated by Django 4.1.7 on 2023-06-29 00:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("property", "0002_alter_parcel_parcel_type_alter_parcel_property"),
    ]

    operations = [
        migrations.AddField(
            model_name="parcel",
            name="farm_name",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="parcel",
            name="farm_number",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="parcel",
            name="sub_division_number",
            field=models.IntegerField(default=0),
        ),
    ]
