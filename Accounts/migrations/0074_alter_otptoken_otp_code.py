# Generated by Django 5.0.7 on 2024-08-23 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0073_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='e1d32e', max_length=6),
        ),
    ]
