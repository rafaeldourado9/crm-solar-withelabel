from rest_framework import serializers
from .models import Equipamento, Painel, Inversor

class EquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = '__all__'

class PainelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Painel
        fields = '__all__'

class InversorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inversor
        fields = '__all__'
