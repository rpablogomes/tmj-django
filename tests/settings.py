from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse

class GlobalTestSetup(APITestCase):
    def setUp(self):
        self.username = 'usuarioTesteNome'
        self.password = 'usuarioTesteSenha'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        url_token = reverse('token_obtain_pair')
        response = self.client.post(url_token, {'username': self.username, 'password': self.password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')