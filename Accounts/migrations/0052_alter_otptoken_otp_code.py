# Generated by Django 5.0.7 on 2024-08-12 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0051_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='b769db', max_length=6),
        ),
    ]
