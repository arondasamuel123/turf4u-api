from django.test import TestCase
# from django.contrib.auth import get_user_model
from turfapi.models import User
# from unittest.mock import patch


# def sample_user(email='test@gmail.com', password='testpass'):
#     """Create sample user"""
#     return get_user_model().objects.create_user(email, password)


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
