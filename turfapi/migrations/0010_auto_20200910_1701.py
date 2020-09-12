# Generated by Django 3.1.1 on 2020-09-10 14:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('turfapi', '0009_auto_20200910_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslots',
            name='timeslot',
        ),
        migrations.AddField(
            model_name='timeslots',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='timeslots',
            name='stop_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]
