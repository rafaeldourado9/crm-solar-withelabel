import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum, Count, Q
from apps.orcamentos.models import Orcamento
from apps.propostas.models import Proposta
from apps.clientes.models import Cliente
from apps.premissas.models import Premissa


class AgenteIAService:
    """Serviço de IA para suporte ao vendedor - focado em energia solar"""
    
    PIADAS_SOLARES = [
        "☀️ Por que o painel solar foi ao psicólogo? Porque estava se sentindo meio 'descarregado'!",
        "⚡ Qual é o super-herói favorito dos instaladores solares? O Flash... de luz solar!",
        "🌞 O que o Sol disse para o painel fotovoltaico? 'Você me deixa radiante!'",
        "💡 Por que o inversor não conta piadas? Porque ele só converte, não inventa!",
        "🔋 Energia solar é tipo café: quanto mais sol, mais energia pra trabalhar!",
    ]
    
    SAUDACOES = [
        "Olá! Sou seu assistente solar! ☀️",
        "E aí, parceiro(a) solar! Como posso iluminar seu dia? 💡",
        "Fala, campeão(ã) das vendas! Bora gerar energia (e vendas)? ⚡",
        "Opa! Seu agente solar está online e carregado! 🔋",
    ]

    @staticmethod
    def processar_mensagem(mensagem: str, vendedor) -> dict:
        """Processa mensagem e retorna resposta com ação"""
        msg_lower = mensagem.lower()
        
        # Detectar intenção
        if any(word in msg_lower for word in ['orcamento', 'orçamento', 'criar', 'gerar', 'calcular']):
            return AgenteIAService._handle_orcamento(mensagem, vendedor)
        
        elif any(word in msg_lower for word in ['proposta', 'vencer', 'expirar', 'prazo']):
            return AgenteIAService._handle_propostas_vencendo(vendedor)
        
        elif any(word in msg_lower for word in ['cliente', 'retorno', 'sem resposta', 'follow', 'followup']):
            return AgenteIAService._handle_clientes_sem_retorno(vendedor)
        
        elif any(word in msg_lower for word in ['relatorio', 'relatório', 'dashboard', 'vendas', 'desempenho']):
            return AgenteIAService._handle_relatorio(vendedor)
        
        elif any(word in msg_lower for word in ['engenharia', 'técnico', 'tecnico', 'dimensionamento', 'hsp', 'perda']):
            return AgenteIAService._handle_duvida_engenharia(mensagem)
        
        elif any(word in msg_lower for word in ['piada', 'engraçado', 'humor', 'alegre']):
            return AgenteIAService._handle_piada()
        
        elif any(word in msg_lower for word in ['oi', 'olá', 'ola', 'hey', 'bom dia', 'boa tarde', 'boa noite']):
            return AgenteIAService._handle_saudacao(vendedor)
        
        else:
            return AgenteIAService._handle_ajuda_geral()

    @staticmethod
    def _handle_saudacao(vendedor) -> dict:
        """Saudação personalizada"""
        saudacao = random.choice(AgenteIAService.SAUDACOES)
        
        # Buscar estatísticas rápidas
        orcamentos_mes = Orcamento.objects.filter(
            vendedor=vendedor,
            criado_em__month=datetime.now().month
        ).count()
        
        resposta = f"{saudacao}\n\n"
        resposta += f"📊 Você já criou {orcamentos_mes} orçamentos este mês!\n\n"
        resposta += "Como posso ajudar hoje?\n"
        resposta += "• Gerar orçamentos\n"
        resposta += "• Ver propostas vencendo\n"
        resposta += "• Clientes sem retorno\n"
        resposta += "• Relatórios de vendas\n"
        resposta += "• Dúvidas técnicas"
        
        return {
            'resposta': resposta,
            'tipo_acao': 'saudacao',
            'metadata': {'orcamentos_mes': orcamentos_mes}
        }

    @staticmethod
    def _handle_orcamento(mensagem: str, vendedor) -> dict:
        """Auxilia na criação de orçamentos"""
        resposta = "💼 **Geração de Orçamentos**\n\n"
        resposta += "Para criar um orçamento, preciso de algumas informações:\n\n"
        resposta += "1️⃣ **Cliente**: Qual cliente? (nome ou ID)\n"
        resposta += "2️⃣ **Consumo**: Qual o consumo mensal em kWh?\n"
        resposta += "3️⃣ **Tipo**: Residencial, comercial ou rural?\n\n"
        resposta += "💡 **Dica**: Use a calculadora no sistema para dimensionamento automático!\n\n"
        
        # Mostrar últimos orçamentos como referência
        ultimos = Orcamento.objects.filter(vendedor=vendedor).order_by('-criado_em')[:3]
        if ultimos:
            resposta += "📋 **Seus últimos orçamentos:**\n"
            for orc in ultimos:
                resposta += f"• {orc.numero} - {orc.cliente.nome} - R$ {orc.valor_final:,.2f}\n"
        
        return {
            'resposta': resposta,
            'tipo_acao': 'orcamento',
            'metadata': {'ultimos_orcamentos': [o.id for o in ultimos]}
        }

    @staticmethod
    def _handle_propostas_vencendo(vendedor) -> dict:
        """Alerta sobre propostas próximas do vencimento"""
        hoje = datetime.now().date()
        limite = hoje + timedelta(days=7)
        
        propostas = Proposta.objects.filter(
            orcamento__vendedor=vendedor,
            status='pendente',
            validade__lte=limite,
            validade__gte=hoje
        ).select_related('orcamento', 'orcamento__cliente')
        
        if not propostas:
            resposta = "✅ **Ótimas notícias!**\n\n"
            resposta += "Você não tem propostas vencendo nos próximos 7 dias! 🎉\n\n"
            resposta += "Continue assim, campeão(ã)! ⚡"
        else:
            resposta = f"⚠️ **ALERTA: {propostas.count()} proposta(s) vencendo!**\n\n"
            for prop in propostas:
                dias = (prop.validade - hoje).days
                urgencia = "🔴 URGENTE" if dias <= 2 else "🟡 ATENÇÃO"
                resposta += f"{urgencia} - {prop.numero}\n"
                resposta += f"   Cliente: {prop.orcamento.cliente.nome}\n"
                resposta += f"   Valor: R$ {prop.orcamento.valor_final:,.2f}\n"
                resposta += f"   Vence em: {dias} dia(s)\n\n"
            
            resposta += "💡 **Ação recomendada**: Entre em contato AGORA!"
        
        return {
            'resposta': resposta,
            'tipo_acao': 'alerta_propostas',
            'metadata': {
                'total': propostas.count(),
                'propostas': [{'id': p.id, 'numero': p.numero, 'dias': (p.validade - hoje).days} for p in propostas]
            }
        }

    @staticmethod
    def _handle_clientes_sem_retorno(vendedor) -> dict:
        """Identifica clientes sem retorno/venda"""
        dias_sem_contato = 15
        data_limite = datetime.now() - timedelta(days=dias_sem_contato)
        
        # Clientes com orçamentos mas sem proposta aceita
        orcamentos_sem_retorno = Orcamento.objects.filter(
            vendedor=vendedor,
            criado_em__lte=data_limite,
            proposta__isnull=True
        ).select_related('cliente').order_by('-criado_em')[:10]
        
        if not orcamentos_sem_retorno:
            resposta = "✅ **Parabéns!**\n\n"
            resposta += "Todos os seus clientes recentes estão sendo acompanhados! 👏\n\n"
            resposta += "Continue com esse follow-up impecável! 🚀"
        else:
            resposta = f"📞 **{orcamentos_sem_retorno.count()} cliente(s) precisam de follow-up!**\n\n"
            resposta += f"Orçamentos criados há mais de {dias_sem_contato} dias sem retorno:\n\n"
            
            for orc in orcamentos_sem_retorno:
                dias = (datetime.now().date() - orc.criado_em.date()).days
                resposta += f"• **{orc.cliente.nome}**\n"
                resposta += f"  Orçamento: {orc.numero} - R$ {orc.valor_final:,.2f}\n"
                resposta += f"  Há {dias} dias - Tel: {orc.cliente.telefone or 'N/A'}\n\n"
            
            resposta += "💡 **Dica**: Uma ligação amigável pode reativar essas oportunidades!"
        
        return {
            'resposta': resposta,
            'tipo_acao': 'clientes_sem_retorno',
            'metadata': {
                'total': orcamentos_sem_retorno.count(),
                'clientes': [{'id': o.cliente.id, 'nome': o.cliente.nome, 'orcamento_id': o.id} for o in orcamentos_sem_retorno]
            }
        }

    @staticmethod
    def _handle_relatorio(vendedor) -> dict:
        """Gera relatório de desempenho"""
        hoje = datetime.now()
        inicio_mes = hoje.replace(day=1)
        
        # Estatísticas do mês
        orcamentos_mes = Orcamento.objects.filter(vendedor=vendedor, criado_em__gte=inicio_mes)
        total_orcamentos = orcamentos_mes.count()
        valor_total = orcamentos_mes.aggregate(total=Sum('valor_final'))['total'] or Decimal('0')
        
        propostas_mes = Proposta.objects.filter(orcamento__vendedor=vendedor, criado_em__gte=inicio_mes)
        propostas_aceitas = propostas_mes.filter(status='aceita').count()
        
        taxa_conversao = (propostas_aceitas / total_orcamentos * 100) if total_orcamentos > 0 else 0
        
        resposta = f"📊 **RELATÓRIO DE DESEMPENHO - {hoje.strftime('%B/%Y').upper()}**\n\n"
        resposta += f"🎯 **Orçamentos Criados**: {total_orcamentos}\n"
        resposta += f"💰 **Valor Total**: R$ {valor_total:,.2f}\n"
        resposta += f"✅ **Propostas Aceitas**: {propostas_aceitas}\n"
        resposta += f"📈 **Taxa de Conversão**: {taxa_conversao:.1f}%\n\n"
        
        if taxa_conversao >= 30:
            resposta += "🏆 **EXCELENTE!** Você está arrasando! Continue assim! 🚀"
        elif taxa_conversao >= 15:
            resposta += "👍 **BOM TRABALHO!** Está no caminho certo! 💪"
        else:
            resposta += "💡 **DICA**: Foque no follow-up para aumentar conversões! 📞"
        
        return {
            'resposta': resposta,
            'tipo_acao': 'relatorio',
            'metadata': {
                'total_orcamentos': total_orcamentos,
                'valor_total': float(valor_total),
                'propostas_aceitas': propostas_aceitas,
                'taxa_conversao': float(taxa_conversao)
            }
        }

    @staticmethod
    def _handle_duvida_engenharia(mensagem: str) -> dict:
        """Responde dúvidas técnicas sobre energia solar"""
        msg_lower = mensagem.lower()
        premissa = Premissa.get_ativa()
        
        resposta = "🔧 **SUPORTE TÉCNICO SOLAR**\n\n"
        
        if 'hsp' in msg_lower:
            resposta += f"☀️ **HSP (Horas de Sol Pleno)**\n"
            resposta += f"Valor atual: {premissa.hsp} horas/dia\n\n"
            resposta += "HSP representa a quantidade de horas de sol com irradiação de 1000W/m².\n"
            resposta += "Varia por região e época do ano.\n\n"
        
        if 'perda' in msg_lower or 'eficiência' in msg_lower or 'eficiencia' in msg_lower:
            resposta += f"⚡ **Perdas do Sistema**\n"
            resposta += f"Perda configurada: {premissa.perda_sistema}%\n\n"
            resposta += "Perdas incluem:\n"
            resposta += "• Sujeira nos painéis\n"
            resposta += "• Temperatura elevada\n"
            resposta += "• Perdas nos cabos\n"
            resposta += "• Eficiência do inversor\n\n"
        
        if 'dimensionamento' in msg_lower or 'calcular' in msg_lower:
            resposta += "📐 **Fórmula de Dimensionamento**\n\n"
            resposta += "```\n"
            resposta += "Potência (kWp) = Consumo Mensal (kWh) / (30 × HSP × (1 - Perda))\n"
            resposta += "Painéis = Potência Total / Potência do Painel\n"
            resposta += "Geração = Potência × HSP × 30 × (1 - Perda)\n"
            resposta += "```\n\n"
        
        if not any(word in msg_lower for word in ['hsp', 'perda', 'dimensionamento', 'calcular', 'eficiência', 'eficiencia']):
            resposta += "Posso ajudar com:\n"
            resposta += "• HSP e irradiação solar\n"
            resposta += "• Perdas e eficiência\n"
            resposta += "• Dimensionamento de sistemas\n"
            resposta += "• Cálculos de geração\n\n"
        
        resposta += "💡 Use a calculadora do sistema para dimensionamento automático!"
        
        return {
            'resposta': resposta,
            'tipo_acao': 'duvida_engenharia',
            'metadata': {'hsp': float(premissa.hsp), 'perda': float(premissa.perda_sistema)}
        }

    @staticmethod
    def _handle_piada() -> dict:
        """Conta uma piada sobre energia solar"""
        piada = random.choice(AgenteIAService.PIADAS_SOLARES)
        
        resposta = f"😄 **HORA DA DESCONTRAÇÃO!**\n\n{piada}\n\n"
        resposta += "Haha! Bora voltar a vender energia solar? ⚡"
        
        return {
            'resposta': resposta,
            'tipo_acao': 'piada',
            'metadata': {}
        }

    @staticmethod
    def _handle_ajuda_geral() -> dict:
        """Ajuda geral sobre o que o agente pode fazer"""
        resposta = "🤖 **CENTRAL DE AJUDA - AGENTE SOLAR**\n\n"
        resposta += "Sou seu assistente especializado em energia solar! Posso ajudar com:\n\n"
        resposta += "💼 **Vendas & Orçamentos**\n"
        resposta += "• Criar e calcular orçamentos\n"
        resposta += "• Alertas de propostas vencendo\n"
        resposta += "• Identificar clientes sem retorno\n\n"
        resposta += "📊 **Relatórios & Análises**\n"
        resposta += "• Desempenho de vendas\n"
        resposta += "• Estatísticas do mês\n"
        resposta += "• Taxa de conversão\n\n"
        resposta += "🔧 **Suporte Técnico**\n"
        resposta += "• Dúvidas de engenharia solar\n"
        resposta += "• Dimensionamento de sistemas\n"
        resposta += "• Cálculos e fórmulas\n\n"
        resposta += "😄 **Entretenimento**\n"
        resposta += "• Piadas solares (porque vender também é se divertir!)\n\n"
        resposta += "⚠️ **IMPORTANTE**: Só respondo sobre energia solar e vendas. Nada de assuntos aleatórios! 😉"
        
        return {
            'resposta': resposta,
            'tipo_acao': 'ajuda',
            'metadata': {}
        }
