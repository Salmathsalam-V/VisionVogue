# Generated by Django 5.0.7 on 2024-08-25 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0090_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='7ee806', max_length=6),
        ),
    ]
