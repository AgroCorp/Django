# Generated by Django 3.2.6 on 2021-08-15 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginApp', '0013_apimodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apimodel',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, unique=True),
        ),
    ]
