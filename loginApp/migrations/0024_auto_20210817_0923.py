# Generated by Django 3.2.6 on 2021-08-17 07:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('loginApp', '0023_alter_apimodel_valid_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='apimodel',
            name='rfid_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='apimodel',
            name='crd',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='apimodel',
            name='valid_to',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 7, 24, 52, 419063, tzinfo=utc)),
        ),
    ]
