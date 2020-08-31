# Generated by Django 3.1 on 2020-08-31 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turfapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role_type',
            field=models.CharField(choices=[('TURF_USER', 'TURF_USER'), ('TURF_MANAGER', 'TURF_MANAGER')], default='TURF_USER', max_length=12),
        ),
    ]