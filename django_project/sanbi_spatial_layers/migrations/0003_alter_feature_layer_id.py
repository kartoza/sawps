# Generated by Django 4.1.7 on 2023-05-24 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('sanbi_spatial_layers', '0002_alter_feature_layer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='layer_id',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='features',
                to='sanbi_spatial_layers.vectorlayer',
            ),
        ),
    ]
