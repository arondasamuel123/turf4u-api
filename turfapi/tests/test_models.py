from django.test import TestCase
import datetime

from turfapi.models import User, Organization, Turf,\
    Timeslots, Booking


def sample_user(email='test@gmail.com', password='testpass'):
    """Create sample user"""
    return User.objects.create_user(email, password)


class UserModelTests(TestCase):
    """
    Tests for creating a user with email as the username
    """
    def test_create_user_with_email_successful(self):
        """ Test creating a new user with email and password"""
        email = 'test@gmail.com'
        password = 'testpass'

        user = User.objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_invalid_email(self):
        """Test creating with no email should raise an error"""
        with self.assertRaises(ValueError):
            User.objects.create_user(None, 'test123')

    def tearDown(self):
        User.objects.all().delete()


class OrganizationModelTestCase(TestCase):
    """
    Test creating Organization str representation
    """

    def test_create_organization(self):
        organization = Organization.objects.create(
            organization_name='GreenSports',
            organization_email='greensports@test.com',
            contact_number="+254712345678",
            user=sample_user()
        )
        self.assertEqual(organization.organization_name, 'GreenSports')
        self.assertEqual(organization.user.email, 'test@gmail.com')
        self.assertTrue(str(organization), organization.organization_name)


class TurfModelTestCase(TestCase):
    """
    Test for creating Turf str representation
    """
    def setUp(self):
        self.test_organization = Organization.objects.create(
            organization_name='Test Organization',
            organization_email='organization@gmail.com',
            organization_location='Test Location',
            contact_number='+254712345678',
            user=sample_user()

        )

    def test_create_turf(self):
        turf = Turf.objects.create(
            turf_name="GreenSports Turf",
            no_of_pitches=2,
            image_url="https://upload-turf-image.com/turf.png",
            org=self.test_organization
        )

        self.assertEqual(turf.turf_name, 'GreenSports Turf')
        self.assertTrue(str(turf), turf.turf_name)
        self.assertEqual(turf.org.organization_name, 'Test Organization')

    def tearDown(self):
        self.test_organization.delete()
        Turf.objects.all().delete()


class TimeslotsModelTestCase(TestCase):
    """
    Test for creating Timeslots str
    representation
    """
    def setUp(self):
        self.test_org = Organization.objects.create(
            organization_name='Manarat School',
            organization_email='manarat@gmail.com',
            organization_location='Kilimani',
            contact_number="+254123456789",
            user=sample_user()
        )
        self.test_turf = Turf.objects.create(
            turf_name='Manarat School',
            no_of_pitches=2,
            image_url='/images/manarat.png',
            org=self.test_org
        )

    def test_create_timeslots(self):
        timeslot = Timeslots.objects.create(
            start_time=datetime.time(8, 00),
            stop_time=datetime.time(9, 00),
            price=9000,
            turf=self.test_turf
        )
        self.assertTrue(str(timeslot), timeslot.start_time)
        self.assertEqual(timeslot.start_time, datetime.time(8, 00))

    def tearDown(self):
        self.test_org.delete()
        self.test_turf.delete()
        Timeslots.objects.all().delete()


class BookingModelTestCase(TestCase):
    """
    Test for creating Booking str
    representation
    """
    def setUp(self):
        self.org = Organization.objects.create(
            organization_name='Arena 256 Inc',
            organization_email='arena@gmail.com',
            user=sample_user(
                email='turfmanager@gmail.com',
                password='secret123'
            ),
            organization_location='Lubowa, Kampala'
        )
        self.test_turf = Turf.objects.create(
            turf_name='Arena 256',
            image_url='/uploads/image/turf.png',
            no_of_pitches=2,
            org=self.org
        )

        self.timeslot = Timeslots.objects.create(
            start_time=datetime.time(8, 00),
            stop_time=datetime.time(9, 00),
            price=5000,
            turf=self.test_turf
        )

    def test_create_booking(self):
        """
        Test creating Booking object
        """
        booking = Booking.objects.create(
            user=sample_user(
                email='turfuser@gmail.com',
                password='secret123'
            ),
            timeslot=self.timeslot,
            date_booked=datetime.date(2020, 9, 11),
            payment_method='MOBILE MONEY'
        )
        self.assertTrue(str(booking), booking.date_booked)
        self.assertEqual(booking.date_booked, datetime.date(2020, 9, 11))

    def tearDown(self):
        self.test_turf.delete()
        self.org.delete()
        self.timeslot.delete()
        Booking.objects.all().delete()
