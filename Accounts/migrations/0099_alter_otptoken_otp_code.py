# Generated by Django 5.0.7 on 2024-08-25 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0098_alter_otptoken_otp_code_referral'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='c90f9e', max_length=6),
        ),
    ]
