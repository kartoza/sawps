# Generated by Django 4.1.10 on 2023-08-07 09:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("occurrence", "0004_merge_20230706_1128"),
    ]

    operations = [
        migrations.AlterField(
            model_name="surveymethod",
            name="sort_id",
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
