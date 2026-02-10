from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Orcamento
from .serializers import OrcamentoSerializer, OrcamentoCreateSerializer
from apps.premissas.models import Premissa
from apps.equipamentos.models import Inversor
from apps.clientes.models import Cliente
from decimal import Decimal, ROUND_UP, ROUND_HALF_UP
from .services.deslocamento_service import DeslocamentoService

class OrcamentoPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

class ValidarDimensionamentoView(APIView):
    def post(self, request):
        potencia_painel = request.data.get('potencia_painel')
        quantidade_paineis = request.data.get('quantidade_paineis')
        inversor_id = request.data.get('inversor_id')
        quantidade_inversores = request.data.get('quantidade_inversores', 1)
        
        if not all([potencia_painel, quantidade_paineis, inversor_id]):
            return Response({'error': 'Dados incompletos'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            inversor = Inversor.objects.get(id=inversor_id)
            
            # Potência total dos painéis em Watts
            potencia_paineis_w = int(potencia_painel) * int(quantidade_paineis)
            
            # Potência máxima suportada pelos inversores (considerando overload)
            # Overload é a porcentagem ADICIONAL que o inversor aguenta
            # Ex: 5000W com overload 0.70 = 5000 * (1 + 0.70) = 8500W
            potencia_max_inversores = inversor.potencia_w * int(quantidade_inversores) * (1 + float(inversor.overload))
            
            valido = potencia_paineis_w <= potencia_max_inversores
            
            return Response({
                'valido': valido,
                'potencia_paineis_w': potencia_paineis_w,
                'potencia_paineis_kwp': round(potencia_paineis_w / 1000, 2),
                'potencia_max_inversores_w': round(potencia_max_inversores, 2),
                'overload_inversor': float(inversor.overload),
                'mensagem': 'Dimensionamento válido' if valido else f'Potência dos painéis ({potencia_paineis_w}W) excede capacidade dos inversores ({round(potencia_max_inversores, 2)}W). Adicione mais inversores ou escolha um inversor maior.'
            })
        except Inversor.DoesNotExist:
            return Response({'error': 'Inversor não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CalcularDeslocamentoView(APIView):
    def post(self, request):
        return Response({
            'error': 'Funcionalidade de deslocamento requer instalação do módulo requests',
            'distancia_km': 0,
            'valor_total': 0,
            'cobrar': False
        }, status=status.HTTP_501_NOT_IMPLEMENTED)

class CalcularMaterialEletricoView(APIView):
    def post(self, request):
        potencia_kwp = request.data.get('potencia_kwp')
        if not potencia_kwp:
            return Response({'error': 'potencia_kwp obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        premissa = Premissa.get_ativa()
        faixas = premissa.material_eletrico_faixas
        
        potencia = float(potencia_kwp)
        valor = 0
        
        for faixa in sorted([int(k) for k in faixas.keys()]):
            if potencia <= faixa:
                valor = faixas[str(faixa)]
                break
        
        if valor == 0 and faixas:
            valor = faixas[str(max([int(k) for k in faixas.keys()]))]
        
        return Response({'valor_material_eletrico': valor})

class OrcamentoViewSet(viewsets.ModelViewSet):
    queryset = Orcamento.objects.all()
    serializer_class = OrcamentoSerializer
    pagination_class = OrcamentoPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vendedor', 'cliente', 'forma_pagamento']
    search_fields = ['numero', 'nome_kit', 'cliente__nome', 'cliente__cidade', 'vendedor__nome']
    ordering_fields = ['data_criacao', 'valor_final', 'numero']
    ordering = ['-data_criacao']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Orcamento.objects.all()
        if hasattr(user, 'vendedor'):
            return Orcamento.objects.filter(vendedor=user.vendedor)
        return Orcamento.objects.filter(cliente__criado_por=user)
    
    def create(self, request):
        serializer = OrcamentoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        premissa = Premissa.get_ativa()
        
        # Buscar cliente para calcular deslocamento
        cliente = Cliente.objects.get(id=data['cliente_id'])
        
        # Atribuir vendedor do cliente ao orçamento
        vendedor_id = data.get('vendedor_id') or (cliente.vendedor.id if cliente.vendedor else None)
        
        # Calcular deslocamento
        deslocamento = DeslocamentoService.calcular_custo_deslocamento(
            cliente.cidade,
            premissa
        )
        
        valor_deslocamento = Decimal(str(deslocamento.get('custo_combustivel', 0)))
        
        # Calcular totais
        valor_kit = Decimal(str(data['valor_kit']))
        valor_projeto = premissa.valor_projeto
        valor_montagem = premissa.montagem_por_painel * data['quantidade_paineis']
        valor_estrutura = Decimal(str(data.get('valor_estrutura', 0)))
        valor_material_eletrico = Decimal(str(data['valor_material_eletrico']))
        
        # Somar itens adicionais
        valor_adicionais = sum(
            Decimal(str(item.get('valor_total', 0))) 
            for item in data.get('itens_adicionais', [])
        )
        
        # Subtotal (custo)
        subtotal = (
            valor_kit + valor_projeto + valor_montagem + 
            valor_estrutura + valor_material_eletrico + valor_adicionais + valor_deslocamento
        )
        
        # Cálculo reverso: Valor Final = Custo / (1 - % total)
        percentual_total = (
            premissa.comissao_percentual + 
            premissa.imposto_percentual + 
            premissa.margem_lucro_percentual
        ) / Decimal('100')
        
        valor_base = subtotal / (Decimal('1') - percentual_total)
        valor_base_arredondado = (valor_base / 100).quantize(Decimal('1'), rounding=ROUND_UP) * 100
        
        # Adicionar margem de desconto
        margem_desconto = valor_base_arredondado * (premissa.margem_desconto_avista_percentual / 100)
        valor_com_margem = valor_base_arredondado + margem_desconto
        
        # Arredondar valor final
        valor_final = (valor_com_margem / 100).quantize(Decimal('1'), rounding=ROUND_UP) * 100
        
        # Aplicar taxa de juros se parcelado
        forma_pagamento = data.get('forma_pagamento', 'avista')
        taxa_juros = Decimal('0')
        valor_parcela = None
        valor_final_com_juros = valor_final
        
        if forma_pagamento != 'avista':
            taxas = premissa.taxas_maquininha
            taxa_juros = Decimal(str(taxas.get(forma_pagamento, 0)))
            valor_final_com_juros = valor_final * (1 + taxa_juros / 100)
            valor_final_com_juros = valor_final_com_juros.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            valor_parcela = (valor_final_com_juros / int(forma_pagamento)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Gerar número
        ultimo = Orcamento.objects.order_by('-id').first()
        numero = f"ORC-{(ultimo.id + 1) if ultimo else 1:04d}"
        
        # Criar orçamento
        orcamento = Orcamento.objects.create(
            numero=numero,
            nome_kit=data['nome_kit'],
            cliente_id=data['cliente_id'],
            vendedor_id=vendedor_id,
            valor_kit=valor_kit,
            marca_painel=data['marca_painel'],
            potencia_painel=data['potencia_painel'],
            quantidade_paineis=data['quantidade_paineis'],
            marca_inversor=data['marca_inversor'],
            potencia_inversor=data['potencia_inversor'],
            quantidade_inversores=data['quantidade_inversores'],
            tipo_estrutura=data['tipo_estrutura'],
            valor_estrutura=valor_estrutura,
            valor_material_eletrico=valor_material_eletrico,
            itens_adicionais=data.get('itens_adicionais', []),
            valor_total=subtotal,
            forma_pagamento=forma_pagamento,
            taxa_juros=taxa_juros,
            valor_final=valor_final_com_juros if forma_pagamento != 'avista' else valor_final,
            valor_parcela=valor_parcela
        )
        
        return Response(OrcamentoSerializer(orcamento).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'], url_path='gerar-pdf-dimensionamento')
    def gerar_pdf_dimensionamento(self, request, pk=None):
        from django.http import HttpResponse
        from .services.template_processor import TemplateProcessorService
        from apps.templates.models import Template
        import tempfile
        import os
        import subprocess
        
        orcamento = self.get_object()
        premissa = Premissa.get_ativa()
        cliente = orcamento.cliente
        
        try:
            template = Template.objects.filter(tipo='orcamento', ativo=True).first()
            
            if not template:
                return Response({'error': 'Nenhum template de orçamento ativo encontrado'}, status=404)
            
            # Processar template DOCX
            buffer_docx = TemplateProcessorService.processar_template(
                template.arquivo.path,
                orcamento,
                premissa,
                cliente
            )
            
            # Criar arquivo temporário DOCX
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_docx:
                tmp_docx.write(buffer_docx.getvalue())
                tmp_docx_path = tmp_docx.name
            
            # Converter para PDF usando LibreOffice
            tmp_dir = os.path.dirname(tmp_docx_path)
            try:
                subprocess.run([
                    'libreoffice',
                    '--headless',
                    '--convert-to', 'pdf',
                    '--outdir', tmp_dir,
                    tmp_docx_path
                ], check=True, capture_output=True, timeout=30)
                
                # Caminho do PDF gerado
                pdf_path = tmp_docx_path.replace('.docx', '.pdf')
                
                # Ler PDF
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_content = pdf_file.read()
                
                # Limpar arquivos temporários
                os.unlink(tmp_docx_path)
                os.unlink(pdf_path)
                
                # Retornar PDF
                response = HttpResponse(pdf_content, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="Orcamento_{orcamento.numero}.pdf"'
                return response
                
            except Exception as e:
                # Se falhar, retornar DOCX
                os.unlink(tmp_docx_path)
                response = HttpResponse(
                    buffer_docx.getvalue(),
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
                response['Content-Disposition'] = f'attachment; filename="Orcamento_{orcamento.numero}.docx"'
                return response
            
        except Exception as e:
            import traceback
            return Response({'error': str(e), 'traceback': traceback.format_exc()}, status=500)
    
    @action(detail=True, methods=['post'])
    def converter_proposta(self, request, pk=None):
        from apps.propostas.models import Proposta
        from apps.contratos.models import Contrato
        from apps.contratos.utils import numero_por_extenso
        from datetime import date
        
        orcamento = self.get_object()
        cliente = orcamento.cliente
        
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
                'campos_faltantes': campos_faltantes,
                'mensagem': f'Complete os seguintes dados do cliente: {", ".join(campos_faltantes)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar se já existe proposta
        if hasattr(orcamento, 'proposta'):
            return Response({
                'error': 'Orçamento já possui proposta',
                'proposta_id': orcamento.proposta.id
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Criar proposta
            ultimo_prop = Proposta.objects.order_by('-id').first()
            numero_prop = f"PROP-{date.today().year}-{(ultimo_prop.id + 1) if ultimo_prop else 1:04d}"
            
            proposta = Proposta.objects.create(
                numero=numero_prop,
                orcamento=orcamento,
                cpf_cnpj=cliente.cpf_cnpj,
                endereco_completo=cliente.endereco,
                bairro=cliente.bairro,
                cep=cliente.cep,
                status='aceita',
                data_aceite=date.today()
            )
            
            # Criar contrato automaticamente
            ultimo_cont = Contrato.objects.order_by('-id').first()
            numero_cont = f"CONT-{date.today().year}-{(ultimo_cont.id + 1) if ultimo_cont else 1:04d}"
            
            # Determinar forma de pagamento e parcelas
            forma_pagamento = 'vista'
            num_parcelas = 1
            valor_parcela = orcamento.valor_final
            
            if orcamento.forma_pagamento != 'avista':
                num_parcelas = int(orcamento.forma_pagamento)
                valor_parcela = orcamento.valor_parcela or (orcamento.valor_final / num_parcelas)
                forma_pagamento = 'cartao' if num_parcelas <= 18 else 'financiamento'
            
            descricao_pagamento = f"Pagamento em {num_parcelas}x de R$ {valor_parcela:.2f}" if num_parcelas > 1 else f"Pagamento à vista de R$ {orcamento.valor_final:.2f}"
            
            contrato = Contrato.objects.create(
                numero=numero_cont,
                proposta=proposta,
                valor_total=orcamento.valor_final,
                valor_total_extenso=numero_por_extenso(float(orcamento.valor_final)),
                forma_pagamento=forma_pagamento,
                descricao_pagamento=descricao_pagamento,
                numero_parcelas=num_parcelas,
                valor_parcela=valor_parcela,
                valor_parcela_extenso=numero_por_extenso(float(valor_parcela)),
                data_assinatura=date.today()
            )
            
            return Response({
                'success': True,
                'proposta_id': proposta.id,
                'proposta_numero': proposta.numero,
                'contrato_id': contrato.id,
                'contrato_numero': contrato.numero,
                'mensagem': 'Proposta e contrato criados com sucesso!'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def detalhamento(self, request, pk=None):
        orcamento = self.get_object()
        premissa = Premissa.get_ativa()
        cliente = orcamento.cliente
        
        # Calcular deslocamento
        deslocamento = DeslocamentoService.calcular_custo_deslocamento(
            cliente.cidade,
            premissa
        )
        
        itens = [
            {
                'categoria': 'Kit',
                'item': 'Valor do Kit',
                'quantidade': 1,
                'valor_unitario': float(orcamento.valor_kit),
                'valor_total': float(orcamento.valor_kit)
            },
            {
                'categoria': 'Kit',
                'item': f'{orcamento.marca_painel} - Painel {orcamento.potencia_painel}W',
                'quantidade': orcamento.quantidade_paineis,
                'valor_unitario': 0,
                'valor_total': 0
            },
            {
                'categoria': 'Kit',
                'item': f'{orcamento.marca_inversor} - Inversor {orcamento.potencia_inversor}W ({int(orcamento.potencia_inversor/1000)} kWp)',
                'quantidade': orcamento.quantidade_inversores,
                'valor_unitario': 0,
                'valor_total': 0
            },
            {
                'categoria': 'Serviços',
                'item': 'Projeto',
                'quantidade': 1,
                'valor_unitario': float(premissa.valor_projeto),
                'valor_total': float(premissa.valor_projeto)
            },
            {
                'categoria': 'Serviços',
                'item': 'Montagem Painel',
                'quantidade': orcamento.quantidade_paineis,
                'valor_unitario': float(premissa.montagem_por_painel),
                'valor_total': float(premissa.montagem_por_painel * orcamento.quantidade_paineis)
            },
            {
                'categoria': 'Custos',
                'item': 'Materiais Elétricos',
                'quantidade': 1,
                'valor_unitario': float(orcamento.valor_material_eletrico),
                'valor_total': float(orcamento.valor_material_eletrico)
            },
            {
                'categoria': 'Custos',
                'item': f'Estrutura - {orcamento.get_tipo_estrutura_display()}',
                'quantidade': 1,
                'valor_unitario': float(orcamento.valor_estrutura),
                'valor_total': float(orcamento.valor_estrutura)
            },
        ]
        
        # Adicionar deslocamento se houver
        if deslocamento.get('cobrar', False):
            itens.append({
                'categoria': 'Custos',
                'item': f'Deslocamento - {cliente.cidade} ({deslocamento.get("distancia_total_km", 0):.0f} km)',
                'quantidade': 1,
                'valor_unitario': float(deslocamento.get('custo_combustivel', 0)),
                'valor_total': float(deslocamento.get('custo_combustivel', 0))
            })
        
        # Adicionar apenas itens adicionais que não sejam duplicados
        itens_base = ['Materiais Elétricos', 'Estrutura']
        for item_adicional in orcamento.itens_adicionais:
            # Verificar se não é um item base
            if not any(base in item_adicional.get('item', '') for base in itens_base):
                itens.append(item_adicional)
        
        return Response({
            'orcamento': OrcamentoSerializer(orcamento).data,
            'itens': itens,
            'deslocamento': deslocamento,
            'valor_total': float(orcamento.valor_total),
            'valor_final': float(orcamento.valor_final)
        })
