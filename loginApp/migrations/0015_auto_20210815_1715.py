# Generated by Django 3.2.6 on 2021-08-15 15:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginApp', '0014_alter_apimodel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apimodel',
            name='crd',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 15, 17, 15, 13, 65216)),
        ),
        migrations.AlterField(
            model_name='apimodel',
            name='valid_to',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 15, 17, 15, 28, 65216)),
        ),
    ]
