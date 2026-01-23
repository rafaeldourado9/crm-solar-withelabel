from rest_framework import serializers
from .models import Contrato

class ContratoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='proposta.orcamento.cliente.nome', read_only=True)
    
    class Meta:
        model = Contrato
        fields = '__all__'
