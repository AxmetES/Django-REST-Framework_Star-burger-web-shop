# Generated by Django 3.0.7 on 2020-11-01 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0037_auto_20201031_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phonenumber',
            field=models.CharField(max_length=10, verbose_name='номер телефона'),
        ),
    ]
