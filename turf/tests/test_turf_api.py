from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from turfapi.models import User, Organization,\
    Turf
from turf.serializers import TurfSerializer


TURF_URL = reverse('turf-list')


def get_turf_by_org(org_id):
    return reverse('turf-get-org', args=[org_id])


def get_turf_by_id(turf_id):
    return reverse('update-image-url', args=[turf_id])


def create_turf_by_org(org_id):
    return reverse('turf-create', args=[org_id])


class PublicAPITestCase(TestCase):
    """
    Test Case for accessing the api publicly
    """
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(TURF_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAPITestCase(TestCase):
    """
    Test case for accessing the API with credentials
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

    def test_retrieve_turfs(self):
        """
        Test to retrieve all turfs
        """
        Turf.objects.create(
            turf_name="Test Turf",
            no_of_pitches=2,
            image_url="uploads/images/turf.jpg",
            org=self.org
        )
        Turf.objects.create(
            turf_name="The Hub Turf",
            no_of_pitches=3,
            image_url="https://upload-turf-image.com/hub.png",
            org=self.org
        )
        res = self.client.get(TURF_URL)
        turfs = Turf.objects.all()
        serializer = TurfSerializer(turfs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_turf(self):
        """
        Test case for creating a turf
        """
        self.payload = {
            "turf_name": "Greensports Turf",
            "no_of_pitches": 2,
            "org": self.org.id
        }
        url = create_turf_by_org(self.org.id)

        res = self.client.post(url, self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_invalid_turf(self):
        """
        Test case for creating an invalid turf
        """
        self.payload = {
            "turf_name": "",
            "no_of_pitches": 2,
            "org": self.org.id
        }
        url = create_turf_by_org(self.org.id)
        res = self.client.post(url, self.payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_turf_limited_to_org(self):
        """
        Retrieve turfs belonging to an organization
        """
        self.org_one = Organization.objects.create(
            organization_name="Turf FC",
            organization_email="turffc@gmail.com",
            organization_location="FC Location",
            contact_number="+256712345678",
            user=self.user
        )
        url = get_turf_by_org(self.org.id)

        Turf.objects.create(
            turf_name="Test turf",
            no_of_pitches=2,
            image_url="/uploads/images/test.jpg",
            org=self.org
        )
        Turf.objects.create(
            turf_name="Turf Stadium",
            no_of_pitches=3,
            image_url="/uploads/images/stadium.jpg",
            org=self.org_one
        )
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_no_duplicate_entries(self):
        """
        Test that no duplicate entries are created
        """
        payload = {
            "turf_name": "The hub Turf",
            "no_of_pitches": 2,
            "org": self.org.id,
            "turf_created": timezone.now()
        }
        payload_two = {
            "turf_name": payload['turf_name'],
            "no_of_pitches": payload['no_of_pitches'],
            "org": payload['org'],
            "turf_created": payload['turf_created']
        }
        url = create_turf_by_org(self.org.id)

        res_one = self.client.post(url, payload)
        res_two = self.client.post(url, payload_two)
        self.assertEqual(res_one.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_two.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_image_url(self):
        """
        Test that a valid image_url has been inserted
        for a specific turf
        """
        self.test_turf = Turf.objects.create(
            turf_name="Test turf",
            no_of_pitches=2,
            org=self.org
        )
        payload = {
            "image_url": "http://res.upload.com/gdgfdsg.png"
        }
        url = get_turf_by_id(self.test_turf.id)
        res = self.client.patch(url, payload)
        self.test_turf.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.test_turf.image_url, payload['image_url'])
        self.test_turf.delete()

    def test_invalid_url(self):
        """
        Test to check if an invalid url has been entered
        """
        self.test_turf = Turf.objects.create(
            turf_name="Test turf",
            no_of_pitches=2,
            org=self.org
        )

        payload = {
            "image_url": "fsadgdagasf.com"
        }
        url = get_turf_by_id(self.test_turf.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.test_turf.delete()

    def tearDown(self):
        self.org.delete()
        self.user.delete()
        Turf.objects.all().delete()
        Organization.objects.all().delete()


class IsManagerPermissionTestCase(TestCase):
    def setUp(self):
        self.turf_user = User.objects.create(
            email="turfuser@gmail.com",
            password="turfuser@abc",
            is_manager=False
        )
        self.org = Organization.objects.create(
            organization_name='Test Organization',
            organization_email='testorg@gmail.com',
            organization_location='Test Location',
            contact_number='+254791019910',
            user=self.turf_user
        )
        self.client = APIClient()
        self.client.force_authenticate(self.turf_user)

    def test_prevent_user_from_creating_turf(self):
        """
        Test that only a manager can create a turf
        """
        payload = {
            "turf_name": "Arena Kampala",
            "no_of_pitches": 3,
            "org": self.org.id,

        }
        url = create_turf_by_org(self.org.id)
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        self.turf_user.delete()
        self.org.delete()
