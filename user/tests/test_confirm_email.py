from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from turfapi.models import User

REGISTER_URL = reverse('user:register-user')


def safe_url(token):
    return f"{reverse('user:activate')}?token={token}"


class AccountActivationTestCase(APITestCase):
    """
    Test case class to check the validity of a
    token
    """
    def setUp(self):

        self.payload = {
            "email": "testuser@gmail.com",
            "name": "Test User",
            "password": "secret@!23"
        }

    def test_account_activation(self):
        """
        Test a user account has been activated with
        a valid token
        """
        res = self.client.post(REGISTER_URL, self.payload)

        if res.status_code == 201:
            user = User.objects.filter(
                email=self.payload['email']
            ).first()
            token = user.generate_confirmation_token()

            url = safe_url(token)
            res = self.client.post(url)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            user.refresh_from_db()
            self.assertTrue(user.is_active)

    def test_no_token_provided(self):
        """
        Test account activation when no token is provided
        """
        self.client.post(REGISTER_URL, self.payload)
        User.objects.filter(email=self.payload['email'])
        token = ''
        url = safe_url(token)
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsigned_token_provided(self):
        """
        Test account activation when unsigned token
        is provided
        """
        self.client.post(REGISTER_URL, self.payload)
        user = User.objects.filter(email=self.payload['email']).first()
        token = user.generate_confirmation_token()

        url = safe_url(token + 'modified')
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_already_activated(self):
        """
        Test to check that a user has already been activated
        """
        self.client.post(REGISTER_URL, self.payload)
        user = User.objects.filter(email=self.payload['email']).first()
        user.is_active = True
        user.save()
        token = user.generate_confirmation_token()

        url = safe_url(token)
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
