from rest_framework import serializers
from .models import Vendedor, VendaVendedor

class VendedorSerializer(serializers.ModelSerializer):
    total_vendas = serializers.SerializerMethodField()
    total_clientes = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Vendedor
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
    
    def get_total_vendas(self, obj):
        return obj.vendas.filter(pago=True).count()
    
    def get_total_clientes(self, obj):
        return obj.clientes.count()
    
    def get_username(self, obj):
        return obj.user.username if obj.user else None

class VendaVendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendaVendedor
        fields = '__all__'
