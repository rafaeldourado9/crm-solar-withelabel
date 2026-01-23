from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.ia_service import IAService
from apps.orcamentos.models import Orcamento
from apps.clientes.models import Cliente

ia_service = IAService()

class AnalisarConsumoView(APIView):
    def post(self, request):
        historico = request.data.get('historico_consumo', [])
        resultado = ia_service.analisar_consumo(historico)
        return Response(resultado)

class OtimizarPropostaView(APIView):
    def post(self, request, orcamento_id):
        orcamento = Orcamento.objects.get(id=orcamento_id)
        dados = {
            'consumo': float(orcamento.consumo_medio_kwh),
            'valor_total': float(orcamento.valor_total),
            'equipamentos': {
                'placas': orcamento.quantidade_placas,
                'modelo_placa': orcamento.modelo_placa,
                'inversor': orcamento.modelo_inversor
            }
        }
        resultado = ia_service.otimizar_proposta(dados)
        return Response(resultado)

class ChatbotView(APIView):
    def post(self, request):
        mensagem = request.data.get('mensagem')
        cliente_id = request.data.get('cliente_id')
        
        contexto = None
        if cliente_id:
            cliente = Cliente.objects.get(id=cliente_id)
            contexto = f"Nome: {cliente.nome}, Status: {cliente.status}, Cidade: {cliente.cidade}"
        
        resposta = ia_service.chatbot_atendimento(mensagem, contexto)
        return Response({'resposta': resposta})

class AnalisarViabilidadeView(APIView):
    def post(self, request):
        dados = request.data
        resultado = ia_service.analisar_viabilidade(dados)
        return Response(resultado)

class GerarEmailFollowupView(APIView):
    def post(self, request, cliente_id):
        cliente = Cliente.objects.get(id=cliente_id)
        dias = request.data.get('dias_sem_resposta', 7)
        
        email = ia_service.gerar_email_followup(
            cliente.nome,
            cliente.status,
            dias
        )
        return Response({'email': email})

class ExtrairContaLuzView(APIView):
    def post(self, request):
        imagem_base64 = request.data.get('imagem_base64')
        dados = ia_service.extrair_dados_conta_luz(imagem_base64)
        return Response(dados)

class PreverEconomiaView(APIView):
    def post(self, request):
        consumo = request.data.get('consumo')
        tarifa = request.data.get('tarifa', 0.95)
        anos = request.data.get('anos', 25)
        
        previsao = ia_service.prever_economia(consumo, tarifa, anos)
        return Response(previsao)
