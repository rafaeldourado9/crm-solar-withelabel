from django.db import models
from django.contrib.auth.models import User


class AgenteIA(models.Model):
    """Configuração personalizada do agente IA por vendedor"""
    vendedor = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agente_ia')
    nome_agente = models.CharField(max_length=100, default='Solar Bot')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agentes_ia'
        verbose_name = 'Agente IA'
        verbose_name_plural = 'Agentes IA'

    def __str__(self):
        return f"{self.nome_agente} - {self.vendedor.username}"


class ConversaIA(models.Model):
    """Histórico de conversas com o agente IA"""
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversas_ia')
    mensagem = models.TextField()
    resposta = models.TextField()
    tipo_acao = models.CharField(max_length=50, null=True, blank=True)  # orcamento, relatorio, alerta, duvida
    metadata = models.JSONField(default=dict, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversas_ia'
        verbose_name = 'Conversa IA'
        verbose_name_plural = 'Conversas IA'
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.vendedor.username} - {self.criado_em.strftime('%d/%m/%Y %H:%M')}"
