from rest_framework import status
from django.contrib.auth.models import User
from tests.settings import GlobalTestSetup

class UserRegistrationTest(GlobalTestSetup):
    """
    Testes para o endpoint de registro de usuário e autenticação.
    """

    def test_registrar_usuario(self):
        """
        Testa se um novo usuário pode ser registrado com sucesso.
        """
        user_data = {
            'username': 'usuarioRegistro',
            'password': 'senhaRegistro'
        }
        
        response = self.client.post('/api/register/' , user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertTrue(User.objects.filter(username='usuarioRegistro').exists())

    def test_registrar_usuario_ja_existente(self):
        """
        Testa se a criação de usuário falha se o nome de usuário já existir.
        """
        user_data = {
            'username': self.username,
            'password': 'password456'
        }
        
        response = self.client.post('/api/register/', user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_obter_token_com_credenciais_invalidas(self):
        """
        Testa se a obtenção do token JWT falha com credenciais inválidas.
        """
        invalid_data = {
            'username': self.username,
            'password': 'senha_errada'
        }
        
        response = self.client.post('/api/token/', invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

    def test_refresh_token(self):
        """
        Testa a atualização de um token de acesso usando o token de refresh.
        """
        
        token_response = self.client.post(
            '/api/token/',
            {'username': self.username, 'password': self.password},
            format='json'
        )
        refresh_token = token_response.data['refresh']
        
        refresh_response = self.client.post(
            '/api/token/refresh/', 
            { 'refresh': refresh_token }, 
            format='json')

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

    def test_blacklist_token(self):
        """
        Testa a invalidação de um token de refresh.
        """

        token_response = self.client.post(
            '/api/token/',
            {'username': self.username, 'password': self.password},
            format='json'
        )
        refresh_token = token_response.data['refresh']

        blacklist_response = self.client.post(
            '/api/token/blacklist/', 
            {'refresh': refresh_token}, 
            format='json')

        self.assertEqual(blacklist_response.status_code, status.HTTP_200_OK)