# Generated by Django 3.1.1 on 2020-09-03 08:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('turfapi', '0003_organization_turf'),
    ]

    operations = [
        migrations.AddField(
            model_name='turf',
            name='turf_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
