# Generated by Django 2.0.5 on 2020-12-12 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enpApi', '0013_player_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='registration_type',
            field=models.CharField(default='', max_length=16),
        ),
    ]