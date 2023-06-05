# Generated by Django 4.1.7 on 2023-06-01 07:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'title',
                    models.CharField(
                        default='', help_text='Reminder title', max_length=200
                    ),
                ),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                (
                    'text',
                    models.TextField(blank=True, help_text='Reminder text', null=True),
                ),
                (
                    'status',
                    models.CharField(
                        blank=True,
                        choices=[('active', 'Active'), ('draft', 'Draft')],
                        max_length=50,
                        null=True,
                    ),
                ),
            ],
        ),
    ]
