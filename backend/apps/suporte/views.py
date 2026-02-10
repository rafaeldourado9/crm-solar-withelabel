from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AgenteIA, ConversaIA
from .serializers import AgenteIASerializer, ConversaIASerializer, ChatRequestSerializer
from .gemini_service import GeminiIAService


class AgenteIAViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar configurações do agente IA"""
    serializer_class = AgenteIASerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AgenteIA.objects.filter(vendedor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(vendedor=self.request.user)

    @action(detail=False, methods=['get'])
    def meu_agente(self, request):
        """Retorna ou cria o agente do vendedor logado"""
        agente, created = AgenteIA.objects.get_or_create(
            vendedor=request.user,
            defaults={'nome_agente': 'Solar Bot'}
        )
        return Response(AgenteIASerializer(agente).data)

    @action(detail=False, methods=['post'])
    def renomear(self, request):
        """Renomeia o agente do vendedor"""
        nome = request.data.get('nome_agente')
        if not nome:
            return Response({'error': 'Nome do agente é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        agente, _ = AgenteIA.objects.get_or_create(vendedor=request.user)
        agente.nome_agente = nome
        agente.save()
        
        return Response({
            'success': True,
            'mensagem': f'Agente renomeado para "{nome}" com sucesso!',
            'agente': AgenteIASerializer(agente).data
        })


class ConversaIAViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar conversas com o agente IA"""
    serializer_class = ConversaIASerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ConversaIA.objects.filter(vendedor=self.request.user)

    @action(detail=False, methods=['post'])
    def chat(self, request):
        """Endpoint principal para conversar com o agente IA"""
        try:
            serializer = ChatRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            mensagem = serializer.validated_data['mensagem']
            
            # Limpar histórico se passar de 50 mensagens
            total_conversas = ConversaIA.objects.filter(vendedor=request.user).count()
            if total_conversas >= 50:
                conversas_antigas = ConversaIA.objects.filter(
                    vendedor=request.user
                ).order_by('-criado_em')[40:]
                ConversaIA.objects.filter(
                    id__in=[c.id for c in conversas_antigas]
                ).delete()
            
            # Processar mensagem com o serviço de IA
            resultado = GeminiIAService.processar_mensagem(mensagem, request.user)
            
            # Salvar conversa no histórico
            conversa = ConversaIA.objects.create(
                vendedor=request.user,
                mensagem=mensagem,
                resposta=resultado['resposta'],
                tipo_acao=resultado['tipo_acao'],
                metadata=resultado['metadata']
            )
            
            return Response({
                'id': conversa.id,
                'mensagem': mensagem,
                'resposta': resultado['resposta'],
                'tipo_acao': resultado['tipo_acao'],
                'metadata': resultado['metadata'],
                'criado_em': conversa.criado_em
            })
        except Exception as e:
            import traceback
            print(f"ERRO CHAT: {e}")
            print(traceback.format_exc())
            return Response({
                'resposta': '❌ Erro ao processar mensagem. Tente novamente.',
                'tipo_acao': 'erro',
                'metadata': {'error': str(e)}
            }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def historico(self, request):
        """Retorna histórico de conversas"""
        limite = int(request.query_params.get('limite', 50))
        conversas = self.get_queryset()[:limite]
        return Response(ConversaIASerializer(conversas, many=True).data)

    @action(detail=False, methods=['delete'])
    def limpar_historico(self, request):
        """Limpa todo o histórico de conversas"""
        total = self.get_queryset().delete()[0]
        return Response({
            'success': True,
            'mensagem': f'{total} conversa(s) deletada(s) com sucesso!'
        })
