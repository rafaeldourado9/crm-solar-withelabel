from rest_framework import serializers
from .models import Orcamento

class OrcamentoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    vendedor_nome = serializers.CharField(source='vendedor.nome', read_only=True, allow_null=True)
    
    class Meta:
        model = Orcamento
        fields = '__all__'
        read_only_fields = ['numero', 'data_criacao']

class OrcamentoCreateSerializer(serializers.Serializer):
    nome_kit = serializers.CharField()
    cliente_id = serializers.IntegerField()
    vendedor_id = serializers.IntegerField(required=False, allow_null=True)
    
    valor_kit = serializers.DecimalField(max_digits=10, decimal_places=2)
    marca_painel = serializers.CharField()
    potencia_painel = serializers.IntegerField()
    quantidade_paineis = serializers.IntegerField()
    marca_inversor = serializers.CharField()
    potencia_inversor = serializers.IntegerField()
    quantidade_inversores = serializers.IntegerField(default=1)
    
    tipo_estrutura = serializers.ChoiceField(choices=[
        'ceramico', 'fibromadeira', 'fibrometal', 'zinco', 'solo', 'laje'
    ])
    valor_estrutura = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_material_eletrico = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    itens_adicionais = serializers.ListField(child=serializers.DictField(), default=list)
    forma_pagamento = serializers.CharField(default='avista')
