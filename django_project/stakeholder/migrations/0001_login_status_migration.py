# Generated by Django 4.1.7 on 2023-06-01 12:00

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [('stakeholder', '0001_initial')]

    operations = [
        migrations.CreateModel(
            name='LoginStatus',
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
                ('name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Login status',
                'verbose_name_plural': 'Login status',
            },
        ),
    ]
