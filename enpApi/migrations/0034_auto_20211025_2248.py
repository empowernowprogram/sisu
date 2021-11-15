# Generated by Django 2.0.5 on 2021-10-25 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enpApi', '0033_merge_20211020_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='employer',
            name='logo',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='employer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='enpApi.Employer'),
        ),
    ]