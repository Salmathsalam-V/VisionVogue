# Generated by Django 5.0.7 on 2024-08-24 11:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0012_categoryoffer_productoffer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoffer',
            name='discount_percentage',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='productoffer',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='discount', to='Store.product'),
        ),
    ]
