# Generated by Django 5.0.7 on 2024-09-01 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0150_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='d15907', max_length=6),
        ),
    ]
