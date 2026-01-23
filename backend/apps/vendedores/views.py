from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Vendedor, VendaVendedor
from .serializers import VendedorSerializer, VendaVendedorSerializer

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Criar usuário Django para o vendedor
        email = serializer.validated_data['email']
        nome = serializer.validated_data['nome']
        senha = self.request.data.get('senha', 'senha123')  # Pega senha do request ou usa padrão
        
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=nome.split()[0],
            last_name=' '.join(nome.split()[1:]) if len(nome.split()) > 1 else '',
            is_staff=False
        )
        user.set_password(senha)
        user.save()
        
        serializer.save(user=user)
    
    @action(detail=True, methods=['post'])
    def resetar_senha(self, request, pk=None):
        vendedor = self.get_object()
        nova_senha = request.data.get('senha', 'senha123')
        if vendedor.user:
            vendedor.user.set_password(nova_senha)
            vendedor.user.save()
            return Response({'message': 'Senha resetada com sucesso'})
        return Response({'error': 'Vendedor sem usuário vinculado'}, status=400)
    
    @action(detail=True, methods=['post'])
    def bloquear(self, request, pk=None):
        vendedor = self.get_object()
        vendedor.bloqueado = not vendedor.bloqueado
        vendedor.save()
        if vendedor.user:
            vendedor.user.is_active = not vendedor.bloqueado
            vendedor.user.save()
        return Response({'bloqueado': vendedor.bloqueado})
    
    @action(detail=True, methods=['get'])
    def resumo(self, request, pk=None):
        vendedor = self.get_object()
        total_clientes = vendedor.clientes.count()
        clientes_ativos = vendedor.clientes.filter(status='contrato').count()
        total_vendas = vendedor.vendas.count()
        valor_total = sum(v.valor_venda for v in vendedor.vendas.all())
        
        return Response({
            'total_clientes': total_clientes,
            'clientes_ativos': clientes_ativos,
            'total_vendas': total_vendas,
            'valor_total': float(valor_total)
        })
    
    @action(detail=True, methods=['get'])
    def clientes(self, request, pk=None):
        vendedor = self.get_object()
        from apps.clientes.serializers import ClienteSerializer
        clientes = vendedor.clientes.all()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def historico_vendas(self, request, pk=None):
        vendedor = self.get_object()
        vendas = vendedor.vendas.all()
        serializer = VendaVendedorSerializer(vendas, many=True)
        return Response(serializer.data)
