from django.urls import path
from .views import TarefaViewSet

urlpatterns = [
    path('tarefas', TarefaViewSet.as_view({'get': 'list', 'post': 'create'}), name='tarefa-list'),
    path('tarefas/<int:pk>', TarefaViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='tarefa-detail'),
]