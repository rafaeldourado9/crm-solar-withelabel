from rest_framework import serializers
from .models import Vendedor, VendaVendedor

class VendedorSerializer(serializers.ModelSerializer):
    total_vendas = serializers.SerializerMethodField()
    
    class Meta:
        model = Vendedor
        fields = '__all__'
    
    def get_total_vendas(self, obj):
        return obj.vendas.filter(pago=True).count()

class VendaVendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendaVendedor
        fields = '__all__'
