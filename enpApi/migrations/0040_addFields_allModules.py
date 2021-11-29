# Generated by Django 2.0.5 on 2021-11-16 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enpApi', '0039_auto_20211115_2328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playsession',
            name='training_type',
        ),
        migrations.AddField(
            model_name='employer',
            name='registered_modules',
            field=models.ManyToManyField(blank=True, null=True, related_name='all_modules', to='enpApi.Modules'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='mandatory_modules',
            field=models.ManyToManyField(blank=True, null=True, related_name='mandatory_modules', to='enpApi.Modules'),
        ),
    ]
