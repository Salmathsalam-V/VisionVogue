# Generated by Django 5.0.7 on 2024-09-01 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0157_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='40f24c', max_length=6),
        ),
    ]