# Generated by Django 5.0.7 on 2024-08-31 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0025_rename_discount_amount_product_offer_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='offer_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]