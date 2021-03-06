from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email="milan@gmail.com", password='test@123'):
    """ create a sample user """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """ test createing a new user with email is successfull """
        email = "test@gmail.com"
        password = 'test@123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test the email for new user is normalized """
        email = "test@Gmail.com"
        user = get_user_model().objects.create_user(email, 'test@123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ test creating user with no email raises error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test@123')

    def test_create_new_super_user(self):
        """ test creating a new superuser """
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test@123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """ test the tag string representation """
        tag = models.Tags.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)
