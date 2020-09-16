from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


from turfapi.models import User


REGISTER_USER_URL = reverse('user:register-user')
TOKEN_URL = reverse('user:obtain-token')
PROFILE_URL = reverse('user:profile')


def sample_user(**params):
    return User.objects.create_user(**params)


class UserPublicAPITestCase(TestCase):
    """
    Test case for creating a user
    """
    def setUp(self):
        self.client = APIClient()

    def test_valid_user_created_successfully(self):
        """
        Create a valid user
        """
        payload = {
            "email": "test@gmail.com",
            "name": "Test Manager",
            "password": "test123",
            "is_manager": True
        }
        res = self.client.post(REGISTER_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        self.assertFalse(user.is_active)

    def test_create_invalid_password(self):
        """
        Check that password not less than 6 characters
        """
        payload = {
            "email": "test@gmail.com",
            "name": "Test User",
            "password": "test",
            "is_manager": False
        }
        res = self.client.post(REGISTER_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_exists(self):
        """
        Check that user exists
        """
        user = User.objects.create_user(
            email="turfuser@gmail.com",
            password="test123"
        )
        payload = {
            "email": user.email,
            "password": user.password,
            "name": "Turf User",
            "is_manager": False
        }
        res = self.client.post(REGISTER_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_manager_created(self):
        """
        Creating a turf manager
        """
        payload = {"email": "manager@gmail.com",
                   "password": "secret123",
                   "name": "Turf Manager",
                   "is_manager": True}

        res = self.client.post(REGISTER_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data.get('is_manager'), True)

    def test_turf_user_created(self):
        """
        Creating a turf user
        """
        payload = {"email": "pitchuser@gmail.com",
                   "password": "testsecret",
                   "name": "Pitch User"}

        res = self.client.post(REGISTER_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data.get('is_manager'), False)

    def test_retrieve_user_unauthorized(self):
        """
        Retrieve user unauthorized test case
        """
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class ObtainTokenTestCase(TestCase):
    """
    Obtaining a token using publicly available api
    """
    def setUp(self):
        self.client = APIClient()

    def test_obtain_token(self):
        """
        Test to check user gets a token after logging in
        """
        payload = {"email": "turfuser@gmail.com", "password": "testabc"}
        sample_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_obtain_token_unsuccessfully(self):
        """
        Obtaining token with invalid credentials
        """
        sample_user(email="turfuser@gmail.com", password="correctpass")
        payload = {"email": "turfuser@gmail.com", "password": "wrongpass"}

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_token_no_user(self):
        """
        Obtaining a token without a created user
        """
        payload = {"email": "testuser@test.com", "password": "notcreated"}
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_token_missing_input(self):
        """
        Obtaining a token with a missing input
        """
        payload = {"email": '', "password": 'testabc'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserAPITestCase(TestCase):
    """
    Test profile endpoints with authenticated user
    """
    def setUp(self):
        self.client = APIClient()
        self.user = sample_user(
            email="turfuser@gmail.com",
            password="secretabc",
            name="Turf user"
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_successfully(self):
        """
        Retrieve authenticated user successfully
        """

        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name,
            'is_manager': False
        })

    def test_update_user_details(self):
        """
        Test user can update user details
        """
        payload = {"password": "newpass"}
        res = self.client.patch(PROFILE_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(payload['password']))

    def test_post_not_allowed(self):
        """
        Test post not allowed on profile url
        """
        res = self.client.post(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
