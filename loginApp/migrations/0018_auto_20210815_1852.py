# Generated by Django 3.2.6 on 2021-08-15 16:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('loginApp', '0017_auto_20210815_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apimodel',
            name='crd',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 15, 16, 52, 46, 403158, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='apimodel',
            name='valid_to',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 15, 16, 54, 46, 403158, tzinfo=utc)),
        ),
    ]
