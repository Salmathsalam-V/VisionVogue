# Generated by Django 3.1 on 2024-08-02 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0010_auto_20240801_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='a430bb', max_length=6),
        ),
    ]
