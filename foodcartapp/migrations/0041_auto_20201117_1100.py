# Generated by Django 3.0.7 on 2020-11-17 11:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0040_auto_20201116_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='call_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, verbose_name='комментарии'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('оплата картой', 'оплата картой'), ('обработанный', 'processed')], default='оплата картой', max_length=13),
        ),
        migrations.AddField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=datetime.date(2020, 11, 17), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('необработанный', 'not processed'), ('обработанный', 'processed')], default='необработанный', max_length=14),
        ),
    ]