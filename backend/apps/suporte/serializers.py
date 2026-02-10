from rest_framework import serializers
from .models import AgenteIA, ConversaIA


class AgenteIASerializer(serializers.ModelSerializer):
    vendedor_nome = serializers.CharField(source='vendedor.username', read_only=True)

    class Meta:
        model = AgenteIA
        fields = ['id', 'vendedor', 'vendedor_nome', 'nome_agente', 'criado_em', 'atualizado_em']
        read_only_fields = ['vendedor', 'criado_em', 'atualizado_em']


class ConversaIASerializer(serializers.ModelSerializer):
    vendedor_nome = serializers.CharField(source='vendedor.username', read_only=True)

    class Meta:
        model = ConversaIA
        fields = ['id', 'vendedor', 'vendedor_nome', 'mensagem', 'resposta', 'tipo_acao', 'metadata', 'criado_em']
        read_only_fields = ['vendedor', 'resposta', 'tipo_acao', 'metadata', 'criado_em']


class ChatRequestSerializer(serializers.Serializer):
    mensagem = serializers.CharField(required=True)
