# Generated by Django 3.1.1 on 2020-09-10 05:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('turfapi', '0007_remove_user_is_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turf',
            name='turf_location',
        ),
        migrations.AddField(
            model_name='organization',
            name='organization_location',
            field=models.CharField(default='Default Location', max_length=255),
        ),
        migrations.AddField(
            model_name='turf',
            name='no_of_pitches',
            field=models.IntegerField(default=1),
        ),
        migrations.CreateModel(
            name='Timeslots',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timeslot', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('turf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turfapi.turf')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_booked', models.DateField(default=django.utils.timezone.now)),
                ('timeslot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turfapi.timeslots')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
