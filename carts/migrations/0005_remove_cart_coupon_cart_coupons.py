# Generated by Django 5.0.7 on 2024-08-24 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_coupon_cart_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='coupon',
        ),
        migrations.AddField(
            model_name='cart',
            name='coupons',
            field=models.ManyToManyField(blank=True, to='carts.coupon'),
        ),
    ]
