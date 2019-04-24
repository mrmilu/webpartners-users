from django.test import override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from test_plus.test import TestCase

from ..settings import DEFAULTS


@override_settings(WEBPARTNERS_USERS=DEFAULTS)
class TestUserAPIV1(APITestCase, TestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.password = 'password'
        self.user = self.make_user(username='test', password=self.password)

    def get_auth_client(self):
        auth_client = self.client_class()
        auth_client.credentials(HTTP_AUTHORIZATION='jwt ' + self.get_jwt_token())
        return auth_client

    def get_auth_info(self):
        return {
            'email': self.email,
            'password': self.password
        }

    def get_jwt_token(self):
        url = reverse('users:jwt_auth')
        response = self.client.post(url, self.get_auth_info())
        return response.data['token']

    def test_create(self):
        url = reverse('users:api-v1:user-list')
        user_data = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'test2@example.com',
            'password': 'password',
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # @TODO - Check new login

        # Email duplicated
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detail(self):
        # Anonymous request
        url = reverse('users:api-v1:user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated requests
        auth_client = self.get_auth_client()
        response = auth_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_user = self.make_user(username='test2')
        url = reverse('users:api-v1:user-detail', kwargs={'pk': new_user.pk})
        response = auth_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        # Anonymous request
        data = {
            'first_name': 'Jorge',
            'last_name': 'Lorenzo',
        }

        url = reverse('users:api-v1:user-detail', kwargs={'pk': self.user.pk})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated request
        auth_client = self.get_auth_client()

        response = auth_client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = auth_client.get(url, data)
        self.assertEqual(response.data['first_name'], 'Jorge')
        self.assertEqual(response.data['last_name'], 'Lorenzo')

    def test_update_email(self):
        auth_client = self.get_auth_client()
        url = reverse('users:api-v1:user-detail', kwargs={'pk': self.user.pk})
        response = auth_client.patch(url, {'email': 'info@domain.com'})

        url = reverse('users:api-v1:user-detail', kwargs={'pk': self.user.pk})
        response = auth_client.get(url)

        self.assertEqual(response.data['email'], 'test@example.com')

    def test_delete(self):
        # Anonymous request
        url = reverse('users:api-v1:user-detail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated request
        auth_client = self.get_auth_client()
        response = auth_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(WEBPARTNERS_USERS={'PASSWORD_VALIDATION': {'MIN_LENGTH': 8}})
    def test_password_length(self):
        url = reverse('users:api-v1:user-list')
        user_data = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'test2@example.com',
            'password': '1234',
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_data['password'] = '12345678'
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @override_settings(WEBPARTNERS_USERS={'PASSWORD_VALIDATION': {'NUMERIC_DISALLOWED': True}})
    def test_password_character(self):
        url = reverse('users:api-v1:user-list')
        user_data = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'test2@example.com',
            'password': '12345678',
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_data['password'] = '123456a'
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @override_settings(WEBPARTNERS_USERS={'PASSWORD_VALIDATION': {'AT_LEAST_ONE_NUMBER': True}})
    def test_password_at_least_one_number(self):
        url = reverse('users:api-v1:user-list')
        user_data = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'test2@example.com',
            'password': 'abcde',
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_data['password'] = 'abcde1'
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_change_password(self):
        auth_client = self.get_auth_client()
        url = reverse('users:api-v1:user-change-password', kwargs={'pk': self.user.pk})
        data = {
            'old_password': 'password',
            'password': 'new_password',
        }
        response = auth_client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(WEBPARTNERS_USERS={'PASSWORD_VALIDATION': {'MIN_LENGTH': 8}})
    def test_change_password_min_length(self):
        auth_client = self.get_auth_client()
        url = reverse('users:api-v1:user-change-password', kwargs={'pk': self.user.pk})
        data = {
            'old_password': 'password',
            'password': '123456',
        }
        response = auth_client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'old_password': 'password',
            'password': '12345678',
        }
        response = auth_client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(WEBPARTNERS_USERS={'PASSWORD_VALIDATION': {'NUMERIC_DISALLOWED': True}})
    def test_change_password_numeric_disallowed(self):
        auth_client = self.get_auth_client()
        url = reverse('users:api-v1:user-change-password', kwargs={'pk': self.user.pk})
        data = {
            'old_password': 'password',
            'password': '123456',
        }
        response = auth_client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'old_password': 'password',
            'password': 'abcde',
        }
        response = auth_client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(WEBPARTNERS_USERS={'PASSWORD_VALIDATION': {'AT_LEAST_ONE_NUMBER': True}})
    def test_change_password_at_least_one_number(self):
        auth_client = self.get_auth_client()
        url = reverse('users:api-v1:user-change-password', kwargs={'pk': self.user.pk})
        data = {
            'old_password': 'password',
            'password': 'abcde',
        }
        response = auth_client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'old_password': 'password',
            'password': 'abcde1',
        }
        response = auth_client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_required_fields(self):
        auth_client = self.get_auth_client()
        url = reverse('users:api-v1:user-change-password', kwargs={'pk': self.user.pk})
        data = {
            'password': 'abcde',
        }
        response = auth_client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
