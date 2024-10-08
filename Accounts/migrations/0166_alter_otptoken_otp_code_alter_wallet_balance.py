# Generated by Django 5.0.7 on 2024-09-05 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0165_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='177f9f', max_length=6),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=1000.0, max_digits=10),
        ),
    ]
