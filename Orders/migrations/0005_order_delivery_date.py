# Generated by Django 5.0.7 on 2024-08-18 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0004_orderproduct_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
