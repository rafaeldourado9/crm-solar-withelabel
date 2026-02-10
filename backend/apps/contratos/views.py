from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFilter, CharFilter
from django.http import HttpResponse
from django.core.files.base import ContentFile
from .models import Contrato
from .serializers import ContratoSerializer
from .services.contrato_service import ContratoService
import subprocess
import tempfile
import os

class ContratoPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

class ContratoFilter(FilterSet):
    data_inicio = DateFilter(field_name='data_assinatura', lookup_expr='gte')
    data_fim = DateFilter(field_name='data_assinatura', lookup_expr='lte')
    forma_pagamento = CharFilter(field_name='forma_pagamento', lookup_expr='iexact')
    cliente = CharFilter(field_name='proposta__orcamento__cliente__nome', lookup_expr='icontains')
    
    class Meta:
        model = Contrato
        fields = ['forma_pagamento', 'data_inicio', 'data_fim', 'cliente']

class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.select_related(
        'proposta__orcamento__cliente',
        'proposta__orcamento__vendedor'
    ).all()
    serializer_class = ContratoSerializer
    pagination_class = ContratoPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ContratoFilter
    search_fields = ['numero', 'proposta__orcamento__cliente__nome']
    ordering_fields = ['data_assinatura', 'valor_total', 'numero']
    ordering = ['-data_assinatura']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        if hasattr(user, 'vendedor'):
            return queryset.filter(proposta__orcamento__vendedor=user.vendedor)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def gerar_pdf(self, request, pk=None):
        contrato = self.get_object()
        cliente = contrato.proposta.orcamento.cliente
        
        # Validar dados completos do cliente
        campos_obrigatorios = {
            'nome': cliente.nome,
            'cpf_cnpj': cliente.cpf_cnpj,
            'telefone': cliente.telefone,
            'email': cliente.email,
            'endereco': cliente.endereco,
            'bairro': cliente.bairro,
            'cidade': cliente.cidade,
            'estado': cliente.estado,
            'cep': cliente.cep
        }
        
        campos_faltantes = [campo for campo, valor in campos_obrigatorios.items() if not valor]
        
        if campos_faltantes:
            return Response({
                'error': 'Dados incompletos do cliente',
                'campos_faltantes': campos_faltantes
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            buffer_docx = ContratoService.gerar_contrato_docx(contrato)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_docx:
                tmp_docx.write(buffer_docx.getvalue())
                tmp_docx_path = tmp_docx.name
            
            tmp_dir = os.path.dirname(tmp_docx_path)
            try:
                subprocess.run([
                    'libreoffice',
                    '--headless',
                    '--convert-to', 'pdf',
                    '--outdir', tmp_dir,
                    tmp_docx_path
                ], check=True, capture_output=True, timeout=30)
                
                pdf_path = tmp_docx_path.replace('.docx', '.pdf')
                
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_content = pdf_file.read()
                
                # Salvar PDF no modelo
                contrato.pdf_contrato.save(
                    f'Contrato_{contrato.numero}.pdf',
                    ContentFile(pdf_content),
                    save=True
                )
                
                os.unlink(tmp_docx_path)
                os.unlink(pdf_path)
                
                response = HttpResponse(pdf_content, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="Contrato_{contrato.numero}.pdf"'
                return response
                
            except Exception as e:
                os.unlink(tmp_docx_path)
                response = HttpResponse(
                    buffer_docx.getvalue(),
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
                response['Content-Disposition'] = f'attachment; filename="Contrato_{contrato.numero}.docx"'
                return response
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
