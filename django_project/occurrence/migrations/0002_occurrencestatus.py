# Generated by Django 4.1.7 on 2023-06-03 12:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('occurrence', '0001_survey_method_migrations'),
    ]

    operations = [
        migrations.CreateModel(
            name='OccurrenceStatus',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Occurrence status',
                'verbose_name_plural': 'Occurrence statuses',
                'db_table': 'occurrence_status',
            },
        ),
    ]
