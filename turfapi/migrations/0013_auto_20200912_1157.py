# Generated by Django 3.1.1 on 2020-09-12 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turfapi', '0012_auto_20200911_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='organization_email',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]
