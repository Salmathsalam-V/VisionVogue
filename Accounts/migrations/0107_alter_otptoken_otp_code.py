# Generated by Django 5.0.7 on 2024-08-26 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0106_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='5d665e', max_length=6),
        ),
    ]