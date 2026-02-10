import os
import google.generativeai as genai
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class GeminiIAService:
    SYSTEM_PROMPT = """Você é um assistente de vendas de energia solar. Fale como uma pessoa REAL.

ESTILO DE ESCRITA:
- Escreva como se estivesse conversando no WhatsApp
- Use gírias brasileiras naturalmente (mano, cara, véi, bora, tá ligado)
- NÃO use listas com hífens ou bullets
- NÃO use emojis (ou use MUITO raramente)
- Escreva parágrafos curtos e diretos
- Seja irônico e sarcástico quando apropriado
- Faça piadas naturais no meio da conversa

PERSONALIDADE:
- Vendedor experiente e descontraído
- Zoador mas profissional
- Direto ao ponto
- Empático mas sem papinho

EXEMPLOS:
❌ ERRADO: "Olá! Posso ajudar com: • Orçamentos • Propostas"
✅ CERTO: "e ai mano, beleza? bora vender energia solar ou vai ficar ai parado?"

❌ ERRADO: "Você tem 3 propostas vencendo."
✅ CERTO: "cara tu tem 3 propostas quase virando pó, liga pra galera agora senão vai perder essa grana"

REGRAS:
- Só fale de energia solar e vendas
- Se perguntarem outra coisa, manda um "mano isso aqui é pra energia solar, não sei de futebol não" """

    @staticmethod
    def processar_mensagem(mensagem: str, user) -> dict:
        from apps.vendedores.models import Vendedor
        from apps.suporte.models import ConversaIA
        
        try:
            vendedor = Vendedor.objects.get(user=user)
        except Vendedor.DoesNotExist:
            vendedor = None
        
        contexto = GeminiIAService._coletar_contexto(vendedor)
        
        # Buscar últimas 50 conversas para contexto
        historico = ConversaIA.objects.filter(vendedor=user).order_by('-criado_em')[:50]
        contexto_conversa = "\n".join([f"User: {c.mensagem}\nBot: {c.resposta}" for c in reversed(historico)])
        
        try:
            if GEMINI_API_KEY:
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"""{GeminiIAService.SYSTEM_PROMPT}

Dados do vendedor:
{contexto}

Histórico recente:
{contexto_conversa}

Usuário agora: {mensagem}

Responda de forma natural, considerando o histórico da conversa."""
                response = model.generate_content(prompt)
                resposta = response.text
            else:
                resposta = GeminiIAService._resposta_fallback(mensagem, vendedor, historico)
            
            return {
                'resposta': resposta,
                'tipo_acao': GeminiIAService._detectar_tipo_acao(mensagem),
                'metadata': {}
            }
        except Exception as e:
            print(f"Erro: {e}")
            return {
                'resposta': GeminiIAService._resposta_fallback(mensagem, vendedor, historico),
                'tipo_acao': 'erro',
                'metadata': {}
            }

    @staticmethod
    def _coletar_contexto(vendedor) -> str:
        if not vendedor:
            return "Usuário: Administrador"
        
        from apps.orcamentos.models import Orcamento
        from apps.propostas.models import Proposta
        from apps.premissas.models import Premissa
        
        hoje = datetime.now()
        inicio_mes = hoje.replace(day=1)
        
        orcamentos = Orcamento.objects.filter(vendedor=vendedor, data_criacao__gte=inicio_mes.date())
        total = orcamentos.count()
        valor = orcamentos.aggregate(total=Sum('valor_final'))['total'] or Decimal('0')
        
        propostas = Proposta.objects.filter(orcamento__vendedor=vendedor, data_criacao__gte=inicio_mes.date())
        aceitas = propostas.filter(status='aceita').count()
        
        premissa = Premissa.get_ativa()
        
        return f"Orçamentos: {total} | Valor: R${valor:,.2f} | Aceitas: {aceitas} | HSP: {premissa.hsp}h"

    @staticmethod
    def _detectar_tipo_acao(msg: str) -> str:
        m = msg.lower()
        if 'proposta' in m or 'vencer' in m: return 'alerta_propostas'
        if 'cliente' in m or 'retorno' in m: return 'clientes_sem_retorno'
        if 'relatorio' in m or 'relatório' in m: return 'relatorio'
        if 'piada' in m: return 'piada'
        return 'conversa'

    @staticmethod
    def _resposta_fallback(msg: str, vendedor, historico=None) -> str:
        from apps.orcamentos.models import Orcamento
        from apps.propostas.models import Proposta
        from apps.premissas.models import Premissa
        
        m = msg.lower()
        
        # Verificar contexto da última mensagem
        ultima_msg = ""
        ultima_resposta = ""
        if historico and len(historico) > 0:
            ultima_msg = historico[0].mensagem.lower()
            ultima_resposta = historico[0].resposta.lower()
        
        # Responder baseado no contexto
        if 'piada' in ultima_msg and any(w in m for w in ['horrivel', 'ruim', 'pessima', 'kkk', 'haha']):
            return "haha eu sei que minhas piadas sao ruins cara\n\nmas pelo menos tu riu ne\n\nbora falar de coisa seria agora, que que tu precisa? propostas vencendo? clientes sem retorno?"
        
        if 'piada' in ultima_resposta and any(w in m for w in ['bora', 'vamo', 'sim', 'beleza']):
            return "booora mano, entao me fala\n\nque que tu precisa? posso te mostrar as propostas que tao vencendo, os clientes que tu esqueceu de ligar, ou um relatorio pra ver se ta vendendo bem\n\ntambem posso tirar duvidas tecnicas se precisar"
        
        if any(w in m for w in ['oi', 'olá', 'hey', 'ola', 'gatao', 'gatão', 'eai', 'e ai']):
            if not vendedor:
                return "e ai chefe, beleza? sou o assistente solar aqui\n\nposso te ajudar com umas paradas tecnicas tipo hsp, perdas, dimensionamento essas coisas\n\ntambem sei umas piadas ruins se quiser rir um pouco\n\nmanda ai o que precisa"
            ctx = GeminiIAService._coletar_contexto(vendedor)
            return f"fala mano, bora vender energia?\n\n{ctx}\n\nque que tu precisa? posso te mostrar as propostas que tao vencendo, os clientes que tu esqueceu de ligar, ou um relatorio pra ver se ta vendendo bem ou mal\n\nmanda ai"
        
        if 'proposta' in m or 'vencer' in m:
            if not vendedor:
                return "essa funcao é so pra vendedor mano, tu é admin, fica de boa ai"
            
            hoje = datetime.now().date()
            limite = hoje + timedelta(days=7)
            props = Proposta.objects.filter(
                orcamento__vendedor=vendedor,
                status='pendente',
                validade__lte=limite,
                validade__gte=hoje
            ).select_related('orcamento__cliente')
            
            if not props:
                return "booora mano, nenhuma proposta vencendo\n\nta em dia hein, assim que é bom\n\ncontinua assim que as vendas vem"
            
            resp = f"cara tu tem {props.count()} proposta{'s' if props.count() > 1 else ''} quase virando po\n\nbora ligar pra galera agora:\n\n"
            for p in props:
                dias = (p.validade - hoje).days
                urgencia = "URGENTE" if dias <= 2 else "atencao"
                resp += f"{urgencia} - {p.numero}\n"
                resp += f"cliente: {p.orcamento.cliente.nome}\n"
                resp += f"grana: R${p.orcamento.valor_final:,.2f}\n"
                resp += f"vence em {dias} dia{'s' if dias != 1 else ''} {'HOJE' if dias == 0 else ''}\n\n"
            
            resp += "liga pra eles agora vei, nao deixa essa grana escapar"
            return resp
        
        if 'cliente' in m or 'retorno' in m:
            if not vendedor:
                return "essa é so pra vendedor chefe, relaxa ai"
            
            data_limite = datetime.now().date() - timedelta(days=15)
            orcs = Orcamento.objects.filter(
                vendedor=vendedor,
                data_criacao__lte=data_limite,
                proposta__isnull=True
            ).select_related('cliente')[:10]
            
            if not orcs:
                return "arrasou mano, todos os clientes tao sendo acompanhados\n\nfollow-up em dia é o segredo pra vender bem\n\ncontinua assim"
            
            resp = f"cara tu tem {orcs.count()} cliente{'s' if orcs.count() > 1 else ''} esperando ha mais de 15 dias\n\nbora dar uma ligadinha:\n\n"
            for o in orcs:
                dias = (datetime.now().date() - o.data_criacao).days
                resp += f"{o.cliente.nome}\n"
                resp += f"orcamento {o.numero} - R${o.valor_final:,.2f}\n"
                resp += f"abandonado ha {dias} dias\n\n"
            
            resp += "uma ligadinha amigavel pode reativar essas vendas mano, nao deixa a grana fugir"
            return resp
        
        if 'piada' in m:
            import random
            piadas = [
                "por que o painel solar foi ao psicologo? tava se sentindo descarregado haha\n\nessa foi pessima ne? mas tu riu",
                "qual o super heroi favorito dos instaladores? o flash de luz solar\n\nadmite que foi engracado",
                "o que o sol disse pro painel? voce me deixa radiante\n\neu sei, sou um genio da comedia",
                "por que o inversor nao conta piadas? porque ele so converte, nao inventa\n\nessa foi boa demais",
                "energia solar é tipo cafe, quanto mais sol mais energia pra trabalhar\n\ne pra vender tambem ne"
            ]
            return f"{random.choice(piadas)}\n\nbora vender energia solar agora?"
        
        if 'hsp' in m or 'perda' in m or 'dimensionamento' in m:
            premissa = Premissa.get_ativa()
            return f"""suporte tecnico solar

dimensionamento basico:
Potencia em kWp = Consumo dividido por 30 vezes HSP vezes 1 menos a Perda

hsp atual ta em {premissa.hsp} horas por dia
perda do sistema ta em {premissa.perda_sistema} porcento

usa a calculadora do sistema que é mais facil mano, é tipo uma calculadora cientifica mas pra energia solar"""
        
        # Resposta genérica com contexto
        if historico and len(historico) > 0:
            return """ta ligado mano, me fala melhor o que tu precisa

posso te ajudar com:

propostas que tao vencendo
clientes sem retorno
relatorios de vendas
duvidas tecnicas

manda ai que eu te ajudo"""
        
        # Primeira interação
        if not vendedor:
            return """assistente solar aqui

posso te ajudar com duvidas tecnicas tipo hsp perdas dimensionamento essas paradas

tambem sei umas formulas e calculos

e umas piadas ruins se quiser

so respondo sobre energia solar ta, se perguntar de futebol vou te ignorar"""
        
        return """assistente solar aqui mano

posso te ajudar com propostas que tao vencendo antes que vire po

clientes sem retorno que tu esqueceu de ligar

relatorios pra ver se ta vendendo bem ou mal

duvidas tecnicas

e umas piadas ruins porque vender tambem é se divertir

so respondo sobre energia solar ta, nada de assunto aleatorio"""
