from django.test import TestCase
# from django.contrib.auth import get_user_model
from turfapi.models import User, Organization, Turf
# from unittest.mock import patch


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
            contact_number='+254712345678',
            user=sample_user()

        )

    def test_create_turf(self):
        turf = Turf.objects.create(
            turf_name="GreenSports Turf",
            turf_location="Valley Arcade",
            turf_image="/upload/images/greensports.jpg",
            org=self.test_organization
        )

        self.assertEqual(turf.turf_name, 'GreenSports Turf')
        self.assertTrue(str(turf), turf.turf_name)
        self.assertEqual(turf.org.organization_name, 'Test Organization')
