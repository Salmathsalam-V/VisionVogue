# Generated by Django 3.1 on 2024-08-01 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_product_image3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='photos/products'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='photos/products'),
        ),
    ]
