from rest_framework import serializers
from .models import Proposta

class PropostaSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='orcamento.cliente.nome', read_only=True)
    
    class Meta:
        model = Proposta
        fields = '__all__'
