# Generated by Django 5.0.7 on 2024-08-31 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0141_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='f7c32a', max_length=6),
        ),
    ]