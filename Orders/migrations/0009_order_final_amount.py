# Generated by Django 5.0.7 on 2024-08-26 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0008_order_discount_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='final_amount',
            field=models.FloatField(blank=True, default=0),
        ),
    ]