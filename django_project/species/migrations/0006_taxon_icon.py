# Generated by Django 4.1.10 on 2023-07-19 20:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("species", "0005_taxon_colour_taxon_front_page_order_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="taxon",
            name="icon",
            field=models.ImageField(blank=True, null=True, upload_to="taxon_icons"),
        ),
    ]
