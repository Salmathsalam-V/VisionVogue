# Generated by Django 5.0.7 on 2024-08-25 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0094_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='ef94e6', max_length=6),
        ),
    ]
