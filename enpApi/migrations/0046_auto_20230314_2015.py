# Generated by Django 2.0.5 on 2023-03-14 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enpApi', '0045_playstate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playstate',
            old_name='currrent_scene',
            new_name='current_scene',
        ),
    ]