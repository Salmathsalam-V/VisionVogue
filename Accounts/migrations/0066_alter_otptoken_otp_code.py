# Generated by Django 5.0.7 on 2024-08-18 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0065_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='422137', max_length=6),
        ),
    ]
