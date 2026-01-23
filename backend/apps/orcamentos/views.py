from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.base import ContentFile
from .models import Orcamento
from .serializers import OrcamentoSerializer, OrcamentoCreateSerializer
from .services import SolarCalculator
from .pdf_service import PDFOrcamentoService
from apps.clientes.models import Cliente
from apps.premissas.models import Premissa
from decimal import Decimal

class CalcularDimensionamentoView(APIView):
    """
    Endpoint para calcular dimensionamento sem salvar
    """
    def post(self, request):
        consumo_kwh = request.data.get('consumo_kwh')
        painel_id = request.data.get('painel_id')
        parcelas = request.data.get('parcelas')
        
        if not consumo_kwh or not painel_id:
            return Response(
                {'error': 'consumo_kwh e painel_id são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calculator = SolarCalculator()
            resultado = calculator.calcular_completo(
                float(consumo_kwh),
                int(painel_id),
                int(parcelas) if parcelas else None,
                hsp=request.data.get('hsp'),
                perda=request.data.get('perda'),
                margem_lucro=request.data.get('margem_lucro')
            )
            return Response(resultado)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrcamentoViewSet(viewsets.ModelViewSet):
    queryset = Orcamento.objects.all()
    serializer_class = OrcamentoSerializer
    
    def create(self, request):
        serializer = OrcamentoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        cliente, _ = Cliente.objects.get_or_create(
            nome=data['nome_cliente'],
            cidade=data['cidade'],
            defaults={'telefone': data.get('telefone', '')}
        )
        
        calculator = SolarCalculator()
        resultado = calculator.calcular_completo(
            float(data['consumo_medio_kwh']),
            data.get('painel_id'),
            data.get('parcelas')
        )
        
        ultimo = Orcamento.objects.order_by('-id').first()
        numero = f"{(ultimo.id + 1) if ultimo else 1}-{cliente.id}"
        
        orcamento = Orcamento.objects.create(
            numero=numero,
            cliente=cliente,
            vendedor_id=data.get('vendedor_id'),
            consumo_medio_kwh=data['consumo_medio_kwh'],
            geracao_requerida_kwh=resultado['geracao_estimada_kwh'],
            potencia_instalada_kwp=resultado['potencia_total_kwp'],
            potencia_placas_w=resultado['painel']['potencia'],
            quantidade_placas=resultado['quantidade_paineis'],
            modelo_placa=resultado['painel']['modelo'],
            modelo_inversor=resultado['inversor']['modelo'] if resultado['inversor'] else '',
            quantidade_inversores=1,
            valor_total=Decimal(resultado['valor_final']),
            validade_dias=resultado['premissas']['validade_proposta_dias']
        )
        
        return Response(OrcamentoSerializer(orcamento).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def gerar_pdf(self, request, pk=None):
        orcamento = self.get_object()
        pdf_buffer = PDFOrcamentoService.gerar_pdf_orcamento(orcamento)
        
        filename = f"orcamento_{orcamento.numero}.pdf"
        orcamento.pdf_gerado.save(filename, ContentFile(pdf_buffer.read()), save=True)
        
        return Response({'pdf_url': orcamento.pdf_gerado.url})
    
    @action(detail=True, methods=['post'])
    def converter_proposta(self, request, pk=None):
        orcamento = self.get_object()
        
        if orcamento.convertido_proposta:
            return Response({'error': 'Orçamento já convertido'}, status=status.HTTP_400_BAD_REQUEST)
        
        from apps.propostas.models import Proposta
        
        ultimo = Proposta.objects.order_by('-id').first()
        numero = f"PROP-{(ultimo.id + 1) if ultimo else 1}"
        
        proposta = Proposta.objects.create(
            numero=numero,
            orcamento=orcamento,
            cpf_cnpj=request.data.get('cpf_cnpj', ''),
            endereco_completo=request.data.get('endereco_completo', ''),
            bairro=request.data.get('bairro', ''),
            cep=request.data.get('cep', ''),
        )
        
        orcamento.convertido_proposta = True
        orcamento.save()
        
        orcamento.cliente.status = 'proposta'
        orcamento.cliente.save()
        
        return Response({'proposta_id': proposta.id, 'numero': proposta.numero})
