# Generated by Django 5.0.7 on 2024-09-04 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0164_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='5079b6', max_length=6),
        ),
    ]
