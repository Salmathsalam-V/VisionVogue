# Generated by Django 3.1 on 2024-08-01 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_auto_20240801_0741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='b3dc4e', max_length=6),
        ),
    ]
