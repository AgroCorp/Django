# Generated by Django 3.2.6 on 2021-08-17 07:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('loginApp', '0022_alter_apimodel_valid_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apimodel',
            name='valid_to',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 7, 11, 52, 927345, tzinfo=utc)),
        ),
    ]
