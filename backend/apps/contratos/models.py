from django.db import models
from apps.propostas.models import Proposta

class Contrato(models.Model):
    FORMA_PAGAMENTO_CHOICES = [
        ('vista', 'À Vista'),
        ('parcelado', 'Parcelado'),
        ('financiamento', 'Financiamento'),
    ]
    
    numero = models.CharField(max_length=20, unique=True)
    proposta = models.OneToOneField(Proposta, on_delete=models.CASCADE, related_name='contrato')
    
    # Dados de pagamento
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    numero_parcelas = models.IntegerField(default=1)
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Datas importantes
    data_assinatura = models.DateField(auto_now_add=True)
    data_inicio_obra = models.DateField(null=True, blank=True)
    data_conclusao = models.DateField(null=True, blank=True)
    prazo_execucao_dias = models.IntegerField(default=45)
    
    # Controle de prazos
    dias_ate_entrega = models.IntegerField(default=0)
    dias_ate_vistoria = models.IntegerField(default=0)
    dias_ate_monitoramento = models.IntegerField(default=0)
    
    # Arquivos
    pdf_contrato = models.FileField(upload_to='contratos/', null=True, blank=True)
    
    # Garantias
    garantia_instalacao_meses = models.IntegerField(default=12)
    garantia_placas_anos = models.IntegerField(default=25)
    garantia_inversor_anos = models.IntegerField(default=10)
    
    # Status
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'contratos'
        ordering = ['-data_assinatura']
    
    def __str__(self):
        return f"Contrato {self.numero} - {self.proposta.orcamento.cliente.nome}"
