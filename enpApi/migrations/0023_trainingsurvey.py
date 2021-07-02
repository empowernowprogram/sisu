# Generated by Django 2.0.5 on 2021-07-02 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('enpApi', '0022_auto_20210606_1116'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_experience', models.IntegerField()),
                ('overall_experience_feedback', models.TextField(blank=True, max_length=3000, null=True)),
                ('selected_features', models.CharField(max_length=255)),
                ('comparison_rating', models.CharField(max_length=255)),
                ('general_feedback', models.TextField(blank=True, max_length=3000, null=True)),
                ('email', models.CharField(max_length=255)),
                ('has_completed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]