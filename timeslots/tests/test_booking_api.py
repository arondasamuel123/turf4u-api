from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import datetime

from turfapi.models import Timeslots, \
    Organization, Turf, User, Booking


def sample_user(email='test@gmail.com', password='secret@123'):
    return User.objects.create_user(email, password)


def sample_org(**params):
    return Organization.objects.create(**params)


def sample_turf(**params):
    return Turf.objects.create(**params)


def book_turf(ts_id):
    return reverse('make-booking', args=[ts_id])


def rud_bookings(ts_id):
    return reverse('read-update-delete-bookings', args=[ts_id])


GET_BOOKINGS_URL = reverse('list-user-bookings')


class PublicAPITestCase(TestCase):
    """
    Test Public available endpoint
    """
    def setUp(self):
        self.client = APIClient()

        self.org = sample_org(
            organization_name='Arena 256 Inc',
            organization_email='arena@gmail.com',
            organization_location='FreedomCity, Entebbe Road',
            user=sample_user()
        )

        self.turf = sample_turf(
            turf_name="Arena KLA Turf",
            turf_image="/upload/images/turf.png",
            no_of_pitches=2,
            org=self.org
        )
        self.ts = Timeslots.objects.create(
            start_time=datetime.time(8, 00),
            stop_time=datetime.time(9, 00),
            price=5000,
            turf=self.turf
        )

    def test_login_required(self):
        """
        Test to unauthorized access
        to enpoint
        """
        url = book_turf(self.ts.id)
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        self.org.delete()
        self.turf.delete()
        self.ts.delete()


class PrivateAPITestCase(TestCase):
    """
    Test to check endpoints only accessible
    to authenticated users
    """
    def setUp(self):
        self.user = sample_user(
            email="turfuser@gmail.com",
            password="secret123"
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.org = sample_org(
            organization_name='The Hub',
            organization_email='thehub@gmail.com',
            organization_location='Lubowa, Off Entebbe Road',
            contact_number='+256712345678',
            user=sample_user()
        )
        self.turf = sample_turf(
            turf_name='The Hub Turf',
            no_of_pitches=2,
            turf_image="/upload/images/turf.jpg",
            org=self.org
        )
        self.ts = Timeslots.objects.create(
            start_time=datetime.time(8, 00),
            stop_time=datetime.time(9, 00),
            price=7000,
            turf=self.turf
        )

    def test_make_booking(self):
        """
        Test making a booking based on a timeslot
        """
        payload = {
            "user": self.user,
            "timeslot": self.ts,
            "date_booked": "2020-09-20"
        }

        url = book_turf(self.ts.id)
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_make_invalid_booking(self):
        """
        Making invalid booking
        """
        payload = {
            "user": self.user,
            "timeslot": self.ts,
            "date_booked": "2020-09-11"
        }
        payload_two = {
            "timeslot": payload['timeslot'],
            "date_booked": payload['date_booked']
        }
        url = book_turf(self.ts.id)
        self.client.post(url, payload)
        res_two = self.client.post(url, payload_two)
        self.assertEqual(res_two.status_code, status.HTTP_400_BAD_REQUEST)

    def test_method_not_allowed(self):
        """
        Test that only the POST method is allowed
        for this endpoint
        """
        url = book_turf(self.ts.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_booking(self):
        """
        Test to check payment status of booking
        before allowing a user to book again
        """
        Booking.objects.create(
            timeslot=self.ts,
            user=self.user,
            date_booked="2020-09-22",
            payment_status='not_paid'
        )
        payload = {
            "user": self.user,
            "timeslot": self.ts,
            "date_booked": "2020-09-27"
        }

        url = book_turf(self.ts.id)
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_bookings_by_user(self):
        """
        Get bookings made by authenticated user
        """
        Booking.objects.create(
            timeslot=self.ts,
            user=self.user,
            date_booked="2020-09-29",
            payment_status='complete'
        )
        Booking.objects.create(
            timeslot=self.ts,
            user=self.user,
            date_booked="2020-10-05"
        )
        res = self.client.get(GET_BOOKINGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.user.delete()
        self.org.delete()
        self.turf.delete()
        self.ts.delete()
        Timeslots.objects.all().delete()


class IsManagerPermissionTestCase(TestCase):
    """
    Test requests that should be carried out by a
    turf manager
    """
    def setUp(self):
        self.user = User.objects.create_user(
            email="turfmanager@gmail.com",
            password="manager@!23",
            is_manager=True
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.org = sample_org(
            organization_name='The Hub',
            organization_email='thehub@gmail.com',
            organization_location='Lubowa, Off Entebbe Road',
            contact_number='+256712345678',
            user=sample_user()
        )
        self.turf = sample_turf(
            turf_name='The Hub Turf',
            no_of_pitches=2,
            turf_image="/upload/images/turf.jpg",
            org=self.org
        )
        self.ts = Timeslots.objects.create(
            start_time=datetime.time(8, 00),
            stop_time=datetime.time(9, 00),
            price=7000,
            turf=self.turf
        )

    def test_retrieve_booking_by_timeslot(self):
        """
        Test to get all bookings for a week for
        a specific timeslot
        """
        self.ts_two = Timeslots.objects.create(
            start_time="2:00",
            stop_time="3:00",
            turf=self.turf,
            price=10000
        )
        Booking.objects.create(
            timeslot=self.ts,
            user=self.user,
            date_booked="2020-09-15"
        )
        Booking.objects.create(
            timeslot=self.ts_two,
            user=self.user,
            date_booked="2020-09-20"
        )
        url = rud_bookings(self.ts.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_update_booking_by_id(self):
        """
        Test to update booking by ID
        """
        self.booking = Booking.objects.create(
            timeslot=self.ts,
            date_booked="2020-09-17",
            user=self.user
        )
        payload = {
            "payment_status": 'complete'
        }
        url = rud_bookings(self.booking.id)
        res = self.client.patch(url, payload)
        self.booking.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.booking.payment_status, payload['payment_status'])

    def test_delete_booking_by_id(self):
        """
        Test to delete a booking by ID
        """
        self.booking_one = Booking.objects.create(
            timeslot=self.ts,
            date_booked="2020-09-25",
            user=self.user
        )
        url = rud_bookings(self.booking_one.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = Booking.objects.filter(
            id=self.booking_one.id
        ).exists()
        self.assertFalse(exists)

    def tearDown(self):
        self.user.delete()
        self.turf.delete()
        self.ts.delete()
        self.org.delete()
        Booking.objects.all().delete()
