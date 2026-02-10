from rest_framework import viewsets, filters, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cliente
from .serializers import ClienteSerializer

class ClientePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ClientePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'cidade', 'vendedor', 'estado']
    search_fields = ['nome', 'cpf_cnpj', 'telefone', 'email', 'cidade']
    ordering_fields = ['created_at', 'nome', 'cidade']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Cliente.objects.all()
        if hasattr(user, 'vendedor'):
            return Cliente.objects.filter(vendedor=user.vendedor)
        return Cliente.objects.filter(criado_por=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        vendedor = None
        
        if hasattr(user, 'vendedor'):
            vendedor = user.vendedor
            cpf_cnpj = serializer.validated_data.get('cpf_cnpj')
            
            if cpf_cnpj:
                cliente_existente = Cliente.objects.filter(cpf_cnpj=cpf_cnpj).exclude(vendedor=vendedor).first()
                if cliente_existente:
                    raise serializers.ValidationError({
                        'cpf_cnpj': f'Cliente já atendido por {cliente_existente.vendedor.nome}'
                    })
        
        serializer.save(criado_por=user, vendedor=vendedor)
