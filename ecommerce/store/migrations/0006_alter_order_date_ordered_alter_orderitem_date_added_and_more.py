# Generated by Django 4.0.4 on 2022-05-12 15:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_product_description_product_feature1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 12, 21, 15, 20, 381498)),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 12, 21, 15, 20, 381498)),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]