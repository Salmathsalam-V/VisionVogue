# Generated by Django 5.0.7 on 2024-09-01 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0030_remove_imagegallery_image2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='lens_color',
        ),
    ]
