from django.test import override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from test_plus.test import TestCase

from ..settings import DEFAULTS


@override_settings(WEBPARTNERS_USERS=DEFAULTS)
class TestUserJWT(APITestCase, TestCase):

    def setUp(self):
        self.email = 'test@example.com'
        self.password = 'password'
        self.user = self.make_user(username='test', password=self.password)

    def get_auth_info(self):
        return {
            'email': self.email,
            'password': self.password
        }

    def test_auth(self):
        url = reverse('users:jwt_auth')
        response = self.client.post(url, self.get_auth_info())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_jwt_token(self):
        url = reverse('users:jwt_auth')
        response = self.client.post(url, self.get_auth_info())
        return response.data['token']

    def test_verify(self):
        url = reverse('users:jwt_verify')
        response = self.client.post(url, {'token': self.get_jwt_token()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh(self):
        url = reverse('users:jwt_refresh')
        response = self.client.post(url, {'token': self.get_jwt_token()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
