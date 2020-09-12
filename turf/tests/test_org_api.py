from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

from turfapi.models import Organization, User


ORG_URL = reverse('org-create')


def get_org(org_id):
    return reverse('org-retrieve-update', args=[org_id])


def get_org_by_user(user_id):
    return reverse('user-get-org', args=[user_id])


class PublicAPITestCase(TestCase):
    """
    Test access to api publicly
    """
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """
        Test that login is required
        """

        res = self.client.post(ORG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAPITestCase(TestCase):
    """
    Test for access API as an authenticated user
    """
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@gmail.com',
            password='test123',
            is_manager=True
        )
        self.org = Organization.objects.create(
            organization_name='Test Organization',
            organization_email='testorg@gmail.com',
            organization_location='Test Location',
            contact_number='+254791019910',
            user=self.user
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_org(self):
        """
        Test for creating an organization
        """
        self.payload = {
            "organization_name": "TurfEntertainment",
            "organization_email": "ent@turfent.com",
            "organization_location": "Lubowa,Kampala",
            "contact_number": "+256772471503",
            "user": self.user.id
        }
        res = self.client.post(ORG_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_check_invalid_email(self):
        """
        Check to see if user has entered invalid email
        """
        payload = {
            "organization_name": "Astro Turf Ltd",
            "organization_email": "astro#gmail.com",
            "organization_location": "Kololo",
            "contact_number": "+25673423456"
        }
        res = self.client.post(ORG_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_org(self):
        """
        Creating invalid organization
        """
        self.payload = {
            "organization_name": "TurfGalore",
            "organization_email": "galore@gmail.com",
            "organization_location": "Kololo",
            "contact_number": "",
            "user": self.user.id
        }
        res = self.client.post(ORG_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_org(self):
        """
        Test for updating organization
        """
        organization = self.org
        payload = {
            "organization_email": "new@gmail.com",
        }
        url = get_org(self.org.id)

        res = self.client.patch(url, payload)
        organization.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.org.organization_email, payload['organization_email'])

    def test_retrieve_orgs_limited_to_user(self):
        """
        Test for retrieving organizations limited to an authenticated user
        """
        self. user_two = User.objects.create_user(
            email='arenaone@gmail.com',
            password='arena123',
            is_manager=True
        )
        Organization.objects.create(
            organization_name="Arena One",
            organization_email="arenaone@gmail.com",
            organization_location="Valley Arcade,Kilimani",
            contact_number="+2547684854",
            user=self.user_two
        )
        url = get_org_by_user(self.user.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_no_duplicate_entries(self):
        """
        Test no duplicate entries are created
        """
        payload = {
            "organization_name": "Second Organizaton",
            "organization_email": "second@gmail.com",
            "organization_location": "Second Location",
            "contact_number": "+256123456789",
            "user": self.user.id
        }
        payload_two = {
            "organization_name": payload['organization_name'],
            "organization_email": payload['organization_email'],
            "organization_location": payload['organization_location'],
            "contact_number": payload['contact_number'],
            "user": payload['user']
        }
        res_one = self.client.post(ORG_URL, payload)
        res_two = self.client.post(ORG_URL, payload_two)

        self.assertEqual(res_one.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_two.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        self.user.delete()
        self.org.delete()
        Organization.objects.all().delete()


class IsManagerPermissionTestCase(TestCase):
    """
    Test Case to check if IsManager Permission is working
    """
    def setUp(self):
        self.client = APIClient()
        self.turf_user = User.objects.create(
            email="turfuser@gmail.com",
            password="secret123",
            is_manager=False
        )
        self.client.force_authenticate(self.turf_user)

    def test_prevent_create_org_by_non_manager(self):
        """
        Test that a turf user can't create an organization
        """

        payload = {
            "organization_name": "Arena Kampala",
            "organization_email": "arenakla@gmail.com",
            "organization_location": "FreedomCity,Entebbe Road",
            "contact_number": "+256123456789",
            "user": self.turf_user.id
        }
        res = self.client.post(ORG_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        self.turf_user.delete()
