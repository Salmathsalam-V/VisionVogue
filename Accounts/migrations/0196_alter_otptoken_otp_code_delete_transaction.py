# Generated by Django 5.0.7 on 2024-09-19 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0195_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='c50728', max_length=6),
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
