from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tags
from receipe.serializers import TagSerializer

TAGS_URL = reverse('receipe:tags-list')


class PublicTagsApiTest(TestCase):
    """ test the publicly available tags API """
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """  test that login is required for retrieving tags """
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """ test the authorized user tags API """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'milan@gmail.com',
            'test@123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        Tags.objects.create(user=self.user, name="Vegan")
        Tags.objects.create(user=self.user, name="Dessert")

        res = self.client.get(TAGS_URL)

        tags = Tags.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tag_limited_to_user(self):
        """ test that tags return are for authenticated user """
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'test@1234'
        )
        Tags.objects.create(user=user2, name='Fruity')
        tag = Tags.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # import ipdb;ipdb.set_trace()
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successfull(self):
        """ test creating a new tag """
        payload = {
            'name': 'test tag'
        }
        self.client.post(TAGS_URL, payload)

        exists = Tags.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """" creating a new tag with invalid payload """
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
