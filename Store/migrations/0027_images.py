# Generated by Django 5.0.7 on 2024-08-31 12:40

import django.db.models.deletion
import imagekit.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0026_alter_product_offer_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image2', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='photos/products')),
                ('image3', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='photos/products')),
                ('image4', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='photos/products')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prod_images', to='Store.product')),
            ],
        ),
    ]
