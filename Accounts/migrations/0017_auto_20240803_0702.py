# Generated by Django 3.1 on 2024-08-03 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0016_auto_20240802_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='ca0cec', max_length=6),
        ),
    ]