# Generated by Django 3.1.1 on 2021-03-23 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginApp', '0007_auto_20210317_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('measure', models.CharField(max_length=200)),
                ('trans_number', models.IntegerField()),
                ('is_default', models.BooleanField()),
            ],
        ),
    ]