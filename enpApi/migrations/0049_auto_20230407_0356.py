# Generated by Django 2.0.5 on 2023-04-07 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enpApi', '0048_auto_20230407_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usagereport',
            name='device_model',
            field=models.CharField(max_length=50),
        ),
    ]