# Generated by Django 4.0.4 on 2022-05-11 16:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 11, 21, 37, 50, 380474)),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 11, 21, 37, 50, 380474)),
        ),
    ]
