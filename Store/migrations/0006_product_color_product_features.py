# Generated by Django 5.0.7 on 2024-08-03 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0005_auto_20240801_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(default='Brown', max_length=20),
        ),
        migrations.AddField(
            model_name='product',
            name='features',
            field=models.CharField(default='polerized', max_length=20),
        ),
    ]
