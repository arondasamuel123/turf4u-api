from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import json
from uuid import UUID
import datetime

from turfapi.models import Turf, Organization, User,\
    Timeslots


def create_ts(turf_id):
    return reverse('create-timeslots', args=[turf_id])


def get_timeslot(ts_id):
    return reverse('update-timeslot', args=[ts_id])


def get_timeslots_by_turf(turf_id):
    return reverse('get-timeslots-turf', args=[turf_id])


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class PublicAPITestCase(TestCase):
    """
    Test unauthorized access to API
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='testuser@gmail.com',
            password='secret123'
        )
        self.org = Organization.objects.create(
            organization_name='Test Organization',
            organization_email='testorg@gmail.com',
            organization_location='Valley Arcade, Kilimani',
            user=self.user
        )
        self.turf = Turf.objects.create(
            turf_name="Arena One",
            no_of_pitches=2,
            turf_image='/image/turf.png',
            org=self.org
        )

    def test_login_required(self):
        """
        Test to check login is required to access this endpoint
        """
        url = create_ts(self.turf.id)
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAPITestCase(TestCase):
    """
    Test API endpoint for authenticated users
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='testuser@gmail.com',
            password='secret123'
        )
        self.org = Organization.objects.create(
            organization_name='Test Organization',
            organization_email='testorg@gmail.com',
            organization_location='Valley Arcade, Kilimani',
            user=self.user
        )
        self.turf = Turf.objects.create(
            turf_name="Arena One",
            no_of_pitches=2,
            turf_image='/image/turf.png',
            org=self.org
        )
        self.client.force_authenticate(self.user)

    def test_create_timeslots(self):
        """
        Test for creating timeslots
        """
        payload = [
            {
                "start_time": "8:30",
                "stop_time": "9:30",
                "price": 5000,
                "turf": self.turf.id
            },
            {
                "start_time": "10:30",
                "stop_time": "11:30",
                "price": 5000,
                "turf": self.turf.id
            },
            {
                "start_time": "12:30",
                "stop_time": "1:30",
                "price": 5000,
                "turf": self.turf.id
            },
        ]

        url = create_ts(self.turf.id)
        res = self.client.post(url, data=json.dumps(
            payload, cls=UUIDEncoder
        ), content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(res.data), 3)

    def test_create_invalid_timeslots(self):
        """
        Test creating invalid timeslot
        """
        payload = [
            {
                "start_time": "",
                "stop_time": "10:00",
                "price": 5000,
                "turf": self.turf.id
            }
        ]
        url = create_ts(self.turf.id)
        res = self.client.post(url, data=json.dumps(
            payload, cls=UUIDEncoder
        ), content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_timeslot(self):
        """
        Update single timeslots
        """
        self.ts = Timeslots.objects.create(
            start_time=datetime.time(8, 00),
            stop_time=datetime.time(9, 00),
            price=4000,
            turf=self.turf
        )
        timeslot = self.ts
        payload = {
            "start_time": datetime.time(10, 30),
            "price": 6000
        }
        url = get_timeslot(self.ts.id)
        res = self.client.patch(url, payload)
        timeslot.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(timeslot.price, payload['price'])
        self.assertEqual(timeslot.start_time, payload['start_time'])

    def test_method_not_allowed(self):
        """
        Test the GET method is not allowed
        for this endpoint
        """
        url = create_ts(self.turf.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_timeslots_by_turf(self):
        """
        Retrieve timeslots associated with a turf
        """
        self.turf_two = Turf.objects.create(
            turf_name="Arena 256",
            no_of_pitches=3,
            turf_image='/upload/img/turf.jpg',
            org=self.org
        )
        Timeslots.objects.create(
            start_time=datetime.time(4, 00),
            stop_time=datetime.time(5, 00),
            price=6000,
            turf=self.turf
        )
        Timeslots.objects.create(
            start_time=datetime.time(6, 00),
            stop_time=datetime.time(7, 00),
            price=6000,
            turf=self.turf
        )

        Timeslots.objects.create(
            start_time=datetime.time(8, 00),
            stop_time=datetime.time(9, 00),
            price=5000,
            turf=self.turf_two
        )

        url = get_timeslots_by_turf(self.turf.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
