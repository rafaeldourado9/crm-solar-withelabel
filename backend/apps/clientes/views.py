from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cliente
from .serializers import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'cidade', 'vendedor']
    search_fields = ['nome', 'cpf_cnpj', 'telefone']
    
    def get_queryset(self):
        user = self.request.user
        # Admin vê todos
        if user.is_staff or user.is_superuser:
            return Cliente.objects.all()
        # Vendedor vê apenas seus clientes
        if hasattr(user, 'vendedor'):
            return Cliente.objects.filter(vendedor=user.vendedor)
        # Outros usuários veem os que criaram
        return Cliente.objects.filter(criado_por=user)
    
    def perform_create(self, serializer):
        # Se usuário é vendedor, associa automaticamente
        vendedor = None
        if hasattr(self.request.user, 'vendedor'):
            vendedor = self.request.user.vendedor
        serializer.save(criado_por=self.request.user, vendedor=vendedor)
