from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.clientes.models import Cliente
from apps.orcamentos.models import Orcamento
from django.utils import timezone
from datetime import timedelta

class DashboardResumoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if user.is_staff or user.is_superuser:
            clientes = Cliente.objects.all()
            orcamentos = Orcamento.objects.all()
        else:
            clientes = Cliente.objects.filter(criado_por=user)
            orcamentos = Orcamento.objects.filter(cliente__criado_por=user)
        
        data_limite = timezone.now() - timedelta(days=30)
        novos_leads = clientes.filter(created_at__gte=data_limite, status='orcamento').count()
        orcamentos_ativos = orcamentos.filter(convertido_proposta=False).count()
        
        ultimos_clientes = clientes[:5].values('id', 'nome', 'telefone', 'status', 'created_at')
        
        return Response({
            'total_clientes': clientes.count(),
            'novos_leads': novos_leads,
            'propostas_ativas': orcamentos_ativos,
            'ultimos_clientes': list(ultimos_clientes)
        })
