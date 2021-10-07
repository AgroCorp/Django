# Generated by Django 3.1.1 on 2021-03-10 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginApp', '0002_auto_20210310_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=200),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='storage_id',
            field=models.IntegerField(default=-1),
        ),
    ]