# Generated by Django 3.1 on 2024-08-01 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0008_auto_20240801_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='358107', max_length=6),
        ),
    ]