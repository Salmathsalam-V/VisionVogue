# Generated by Django 5.0.7 on 2024-09-06 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0167_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='77c577', max_length=6),
        ),
    ]
