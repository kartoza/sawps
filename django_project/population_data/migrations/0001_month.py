# Generated by Django 4.1.7 on 2023-06-04 07:45

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Month',
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
                ('sorid', models.IntegerField(unique=True)),
            ],
            options={
                'verbose_name': 'month',
                'verbose_name_plural': 'months',
                'db_table': 'month',
            },
        ),
    ]