# Generated by Django 3.1 on 2024-08-02 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0013_auto_20240802_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='43c41e', max_length=6),
        ),
    ]