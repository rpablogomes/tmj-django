from rest_framework import serializers
from .models import Tarefa

class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefa
        fields = ['id', 'title', 'description', 'completed', 'user', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']