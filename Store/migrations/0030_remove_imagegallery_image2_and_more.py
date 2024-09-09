# Generated by Django 5.0.7 on 2024-09-01 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0029_variation_images_alter_imagegallery_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagegallery',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='imagegallery',
            name='image3',
        ),
        migrations.RemoveField(
            model_name='imagegallery',
            name='image4',
        ),
        migrations.RemoveField(
            model_name='imagegallery',
            name='product',
        ),
        migrations.AddField(
            model_name='imagegallery',
            name='images',
            field=models.ImageField(default='Null', upload_to='photos/variation_gallery'),
        ),
        migrations.AddField(
            model_name='imagegallery',
            name='variation',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='Store.variation'),
        ),
    ]
