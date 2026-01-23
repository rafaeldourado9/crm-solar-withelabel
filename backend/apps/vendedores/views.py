from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vendedor, VendaVendedor
from .serializers import VendedorSerializer, VendaVendedorSerializer

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    
    @action(detail=True, methods=['get'])
    def historico_vendas(self, request, pk=None):
        vendedor = self.get_object()
        vendas = vendedor.vendas.all()
        serializer = VendaVendedorSerializer(vendas, many=True)
        return Response(serializer.data)
