# Generated by Django 5.0.7 on 2024-08-26 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_remove_cart_coupon_cart_coupons'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cart',
            name='grand_total',
            field=models.IntegerField(default=0),
        ),
    ]