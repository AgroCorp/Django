# Generated by Django 3.2.6 on 2021-08-15 16:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('loginApp', '0018_auto_20210815_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apimodel',
            name='crd',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 15, 16, 53, 30, 76122, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='apimodel',
            name='valid_to',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 15, 16, 55, 30, 76122, tzinfo=utc)),
        ),
    ]
