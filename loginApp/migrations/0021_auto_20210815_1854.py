# Generated by Django 3.2.6 on 2021-08-15 16:54

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('loginApp', '0020_auto_20210815_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apimodel',
            name='crd',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='apimodel',
            name='valid_to',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 15, 16, 56, 53, 643389, tzinfo=utc)),
        ),
    ]
