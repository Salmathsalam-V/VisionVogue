# Generated by Django 5.0.7 on 2024-08-10 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0002_order_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tax',
        ),
    ]
