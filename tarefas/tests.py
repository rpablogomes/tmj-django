from rest_framework import status
from .models import Tarefa
from tests.settings import GlobalTestSetup

class TarefaAPITestCase(GlobalTestSetup):

    def setUp(self):
        """
        Configura os dados necessários para os testes.
        Isso inclui chamar o setUp da classe base para lidar com a autenticação.
        """
        
        super().setUp()

        self.tarefa_1 = Tarefa.objects.create(
            user=self.user,
            title="Tarefa de Teste 1",
            description="Descrição da Tarefa 1",
            completed=False
        )

    def test_listar_tarefas(self):
        """Testa a listagem de todas as tarefas do usuário autenticado."""
        response = self.client.get('/api/tarefas')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Tarefa de Teste 1')

    def test_criar_tarefa(self):
        """Testa a criação de uma nova tarefa."""
        data = {
            'title': 'Nova Tarefa',
            'description': 'Descrição da nova tarefa',
            'completed': True
        }
        response = self.client.post('/api/tarefas', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tarefa.objects.count(), 2)
        self.assertEqual(response.data['title'], 'Nova Tarefa')

    def test_verificar_tarefa(self):
        """Testa a recuperação de uma tarefa específica."""
        response = self.client.get(f'/api/tarefas/{self.tarefa_1.pk}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Tarefa de Teste 1')
    
    def test_atualizar_tarefa(self):
        """Testa a atualização completa de uma tarefa (PUT)."""
        data = {
            'title': 'Tarefa Atualizada',
            'description': 'Descrição atualizada',
            'completed': True,
        }
        response = self.client.put(f'/api/tarefas/{self.tarefa_1.pk}', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tarefa_1.refresh_from_db()
        self.assertEqual(self.tarefa_1.title, 'Tarefa Atualizada')

    def test_atualização_parcial_tarefa(self):
        """Testa a atualização parcial de uma tarefa (PATCH)."""
        data = {'completed': True}
        response = self.client.patch(f'/api/tarefas/{self.tarefa_1.pk}', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tarefa_1.refresh_from_db()
        self.assertTrue(self.tarefa_1.completed)

    def test_deletar_tarefa(self):
        """Testa a exclusão de uma tarefa."""
        response = self.client.delete(f'/api/tarefas/{self.tarefa_1.pk}')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tarefa.objects.count(), 0)


    def test_listar_tarefas_concluidas(self):
        """
        Testa a listagem de tarefas filtrando apenas por 'completed=true'.
        """
        Tarefa.objects.create(
            user=self.user,
            title="Tarefa Concluída",
            description="Esta tarefa está completa.",
            completed=True
        )
        response = self.client.get('/api/tarefas?completed=true')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Tarefa Concluída')

    def test_listar_tarefas_nao_concluidas(self):
        """
        Testa a listagem de tarefas filtrando apenas por 'completed=false'.
        """
        Tarefa.objects.create(
            user=self.user,
            title="Tarefa Concluída",
            description="Esta tarefa está completa.",
            completed=True
        )
        response = self.client.get('/api/tarefas?completed=false')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Tarefa de Teste 1')