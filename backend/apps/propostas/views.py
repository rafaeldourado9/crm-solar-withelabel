from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date
from .models import Proposta
from .serializers import PropostaSerializer

class PropostaViewSet(viewsets.ModelViewSet):
    queryset = Proposta.objects.all()
    serializer_class = PropostaSerializer
    
    def create(self, request, *args, **kwargs):
        orcamento_id = request.data.get('orcamento')
        
        # Buscar orçamento para copiar margens
        from apps.orcamentos.models import Orcamento
        orcamento = Orcamento.objects.get(id=orcamento_id)
        
        # Adicionar margens do orçamento aos dados da proposta
        data = request.data.copy()
        data['margem_lucro_percentual'] = getattr(orcamento, 'margem_lucro_percentual', None)
        data['comissao_percentual'] = getattr(orcamento, 'comissao_percentual', None)
        data['imposto_percentual'] = getattr(orcamento, 'imposto_percentual', None)
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def aceitar(self, request, pk=None):
        proposta = self.get_object()
        proposta.status = 'aceita'
        proposta.data_aceite = date.today()
        proposta.save()
        
        proposta.orcamento.cliente.status = 'proposta'
        proposta.orcamento.cliente.cpf_cnpj = proposta.cpf_cnpj
        proposta.orcamento.cliente.endereco = proposta.endereco_completo
        proposta.orcamento.cliente.bairro = proposta.bairro
        proposta.orcamento.cliente.cep = proposta.cep
        proposta.orcamento.cliente.save()
        
        return Response({'status': 'aceita'})
    
    @action(detail=True, methods=['post'])
    def converter_contrato(self, request, pk=None):
        proposta = self.get_object()
        
        if proposta.status != 'aceita':
            return Response({'error': 'Proposta não aceita'}, status=status.HTTP_400_BAD_REQUEST)
        
        if proposta.convertido_contrato:
            return Response({'error': 'Já convertido'}, status=status.HTTP_400_BAD_REQUEST)
        
        from apps.contratos.models import Contrato
        
        ultimo = Contrato.objects.order_by('-id').first()
        numero = f"CONT-{(ultimo.id + 1) if ultimo else 1}"
        
        contrato = Contrato.objects.create(
            numero=numero,
            proposta=proposta,
            valor_total=proposta.orcamento.valor_total,
            forma_pagamento=request.data.get('forma_pagamento', 'vista'),
            numero_parcelas=request.data.get('numero_parcelas', 1),
            valor_parcela=request.data.get('valor_parcela', proposta.orcamento.valor_total),
        )
        
        proposta.convertido_contrato = True
        proposta.save()
        
        proposta.orcamento.cliente.status = 'contrato'
        proposta.orcamento.cliente.save()
        
        return Response({'contrato_id': contrato.id, 'numero': contrato.numero})
