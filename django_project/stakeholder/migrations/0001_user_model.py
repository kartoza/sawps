# Generated by Django 4.1.7 on 2023-05-30 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    replaces = [
        ('stakeholder', '0001_initial'),
        ('stakeholder', '0002_organization_organizationuser_and_more'),
    ]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('regulatory_permit', '0001_initial'),
    ]

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
        migrations.CreateModel(
            name='UserRoleType',
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
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'User role',
                'verbose_name_plural': 'User roles',
            },
        ),
        migrations.CreateModel(
            name='UserTitle',
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
                ('name', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'verbose_name': 'title',
                'verbose_name_plural': 'titles',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
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
                ('cell_number', models.IntegerField()),
                (
                    'title_id',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to='stakeholder.usertitle',
                    ),
                ),
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'user_role_type_id',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to='stakeholder.userroletype',
                    ),
                ),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='UserLogin',
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
                (
                    'datetime',
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ('ip_address', models.CharField(max_length=15)),
                (
                    'login_status_id',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to='stakeholder.loginstatus',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='stakeholder.userprofile',
                    ),
                ),
            ],
            options={
                'verbose_name': 'User login',
                'verbose_name_plural': 'Users login',
            },
        ),
        migrations.CreateModel(
            name='Organization',
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
                ('name', models.CharField(max_length=250, unique=True)),
                (
                    'data_use_permission',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to='regulatory_permit.datausepermission',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.CreateModel(
            name='OrganizationUser',
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
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='stakeholder.organization',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'verbose_name': 'Organization user',
                'verbose_name_plural': 'Organization users',
            },
        ),
        migrations.CreateModel(
            name='OrganizationRepresentatives',
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
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='stakeholder.organization',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'verbose_name': 'Organization representative',
                'verbose_name_plural': 'Organization representatives',
            },
        ),
    ]
