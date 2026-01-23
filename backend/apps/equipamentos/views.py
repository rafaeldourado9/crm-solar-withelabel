from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Equipamento, Painel, Inversor
from .serializers import EquipamentoSerializer, PainelSerializer, InversorSerializer

# Imports necessários para o ReportLab (PDF)
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class EquipamentoViewSet(viewsets.ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer
    filterset_fields = ['categoria', 'ativo']

    @action(detail=False, methods=['post'])
    def gerar_os(self, request):
        """
        Gera um PDF da Ordem de Serviço com base nos dados enviados (Cliente, Tipo, Itens).
        Não exibe custos.
        """
        # 1. Captura os dados
        dados = request.data
        cliente = dados.get('cliente', 'Não informado')
        tipo_servico = dados.get('tipo_servico', 'Serviço Geral')
        descricao = dados.get('descricao', '')
        data_execucao = dados.get('data', '')
        itens = dados.get('itens', [])

        # 2. Prepara o Buffer e o Documento
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Estilos personalizados
        titulo_style = ParagraphStyle(
            'TituloOS',
            parent=styles['Heading1'],
            fontSize=18,
            alignment=1, # Centralizado
            spaceAfter=20
        )
        campo_style = ParagraphStyle(
            'CampoOS',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=6
        )

        # 3. Cabeçalho da OS
        elements.append(Paragraph(f"ORDEM DE SERVIÇO - {tipo_servico.upper()}", titulo_style))
        elements.append(Spacer(1, 12))

        # 4. Detalhes do Cliente/Serviço
        elements.append(Paragraph(f"<b>Cliente / Local:</b> {cliente}", campo_style))
        elements.append(Paragraph(f"<b>Data Programada:</b> {data_execucao}", campo_style))
        elements.append(Spacer(1, 12))
        
        elements.append(Paragraph("<b>Descrição da Atividade:</b>", campo_style))
        elements.append(Paragraph(descricao, styles['Normal']))
        elements.append(Spacer(1, 25))

        # 5. Tabela de Equipamentos (Sem custos)
        if itens:
            elements.append(Paragraph("<b>Equipamentos e Materiais Necessários:</b>", styles['Heading3']))
            elements.append(Spacer(1, 10))

            # Cabeçalho da Tabela
            table_data = [['Tipo', 'Modelo / Fabricante', 'Qtd']]

            # Preenchimento das linhas
            for item in itens:
                # Tenta pegar modelo/fabricante ou usa o nome genérico 'item'
                modelo = item.get('modelo') or item.get('item') or ''
                fabricante = item.get('fabricante') or ''
                descricao_item = f"{modelo} {fabricante}".strip()
                
                table_data.append([
                    item.get('tipo', 'Outro'),
                    descricao_item,
                    str(item.get('quantidade', 1))
                ])

            # Criação da tabela com estilos
            t = Table(table_data, colWidths=[100, 300, 50])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')), # Azul
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (2, 0), (2, -1), 'CENTER'), # Qtd centralizada
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
            ]))
            elements.append(t)
        else:
            elements.append(Paragraph("Nenhum equipamento vinculado a esta ordem.", styles['Normal']))

        elements.append(Spacer(1, 50))

        # 6. Área de Assinaturas
        elements.append(Paragraph("_" * 50, styles['Normal']))
        elements.append(Paragraph("Técnico Responsável", styles['Normal']))
        elements.append(Spacer(1, 30))
        elements.append(Paragraph("_" * 50, styles['Normal']))
        elements.append(Paragraph("De Acordo (Cliente)", styles['Normal']))

        # 7. Gerar PDF
        doc.build(elements)
        buffer.seek(0)
        
        # Retorna o arquivo
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="OS_{cliente}.pdf"'
        return response


class PainelViewSet(viewsets.ModelViewSet):
    queryset = Painel.objects.filter(ativo=True).order_by('fabricante', 'potencia_w', 'modelo')
    serializer_class = PainelSerializer
    search_fields = ['fabricante', 'modelo', 'potencia_w']
    ordering_fields = ['fabricante', 'potencia_w', 'modelo']
    ordering = ['fabricante', 'potencia_w', 'modelo']

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        if Painel.objects.count() >= 4000:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Limite de 4000 painéis atingido')
        cache.delete_pattern('crm_solar:*paineis*')
        serializer.save()

    def perform_update(self, serializer):
        cache.delete_pattern('crm_solar:*paineis*')
        serializer.save()

    def perform_destroy(self, instance):
        cache.delete_pattern('crm_solar:*paineis*')
        instance.delete()

class InversorViewSet(viewsets.ModelViewSet):
    queryset = Inversor.objects.filter(ativo=True).order_by('fabricante', 'potencia_w', 'modelo')
    serializer_class = InversorSerializer
    search_fields = ['fabricante', 'modelo', 'potencia_w']
    ordering_fields = ['fabricante', 'potencia_w', 'modelo']
    ordering = ['fabricante', 'potencia_w', 'modelo']

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        if Inversor.objects.count() >= 4000:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Limite de 4000 inversores atingido')
        cache.delete_pattern('crm_solar:*inversores*')
        serializer.save()

    def perform_update(self, serializer):
        cache.delete_pattern('crm_solar:*inversores*')
        serializer.save()

    def perform_destroy(self, instance):
        cache.delete_pattern('crm_solar:*inversores*')
        instance.delete()
