from rest_framework import serializers
from .models import Orcamento
from apps.clientes.models import Cliente

class OrcamentoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    vendedor_nome = serializers.CharField(source='vendedor.nome', read_only=True)
    
    class Meta:
        model = Orcamento
        fields = '__all__'
        read_only_fields = ['numero', 'data_criacao', 'pdf_gerado']

class OrcamentoCreateSerializer(serializers.Serializer):
    # Dados do cliente
    nome_cliente = serializers.CharField()
    cidade = serializers.CharField()
    telefone = serializers.CharField(required=False, allow_blank=True)
    
    # Dados do dimensionamento
    consumo_medio_kwh = serializers.DecimalField(max_digits=10, decimal_places=2)
    potencia_placas_w = serializers.IntegerField()
    modelo_placa = serializers.CharField()
    modelo_inversor = serializers.CharField()
    
    vendedor_id = serializers.IntegerField(required=False)
