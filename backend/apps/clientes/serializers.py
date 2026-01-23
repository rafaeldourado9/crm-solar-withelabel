from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    criado_por_nome = serializers.CharField(source='criado_por.username', read_only=True)
    
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ['criado_por']
