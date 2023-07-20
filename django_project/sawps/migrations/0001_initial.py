# Generated by Django 4.1.10 on 2023-07-20 09:35

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UploadSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "token",
                    models.UUIDField(default=uuid.uuid4, editable=False, null=True),
                ),
                ("uploaded_at", models.DateTimeField(default=datetime.datetime.now)),
                ("processed", models.BooleanField(default=False)),
                ("canceled", models.BooleanField(default=False)),
                ("error_notes", models.TextField(blank=True, null=True)),
                ("success_notes", models.TextField(blank=True, null=True)),
                ("progress", models.CharField(blank=True, default="", max_length=200)),
                (
                    "process_file",
                    models.FileField(max_length=512, null=True, upload_to="species"),
                ),
                (
                    "success_file",
                    models.FileField(
                        blank=True, max_length=512, null=True, upload_to="species"
                    ),
                ),
                (
                    "error_file",
                    models.FileField(
                        blank=True, max_length=512, null=True, upload_to="species"
                    ),
                ),
                (
                    "updated_file",
                    models.FileField(
                        blank=True, max_length=512, null=True, upload_to="species"
                    ),
                ),
                (
                    "uploader",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="upload_session_uploader",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Upload Session",
                "verbose_name_plural": "Upload Sessions",
            },
        ),
    ]
