# Generated by Django 3.1.1 on 2020-09-14 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turfapi', '0015_auto_20200914_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turf',
            name='image_url',
            field=models.URLField(max_length=255, null=True),
        ),
    ]
