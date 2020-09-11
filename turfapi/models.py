import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    BaseUserManager
from django.conf import settings
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and saves new user
        """
        if not email:
            raise ValueError('Users must have email address')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_name = models.CharField(max_length=255)
    organization_email = models.CharField(max_length=255)
    organization_location = models.CharField(
        max_length=255,
        default='Default Location'
    )
    contact_number = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    org_created = models.DateTimeField(default=timezone.now)


class Turf(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    turf_name = models.CharField(max_length=255)
    no_of_pitches = models.IntegerField(default=1)
    turf_image = models.CharField(max_length=255)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    turf_created = models.DateTimeField(default=timezone.now)


class Timeslots(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    start_time = models.TimeField(default=timezone.now)
    stop_time = models.TimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Booking(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    timeslot = models.ForeignKey(
        Timeslots,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_booked = models.DateField(default=timezone.now)
