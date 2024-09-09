# Generated by Django 5.0.7 on 2024-09-08 04:04

import imagekit.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0037_alter_imagegallery_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagegallery',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='photos/variation_gallery'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='images',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='photos/products'),
        ),
    ]
