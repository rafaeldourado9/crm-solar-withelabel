from django.db import models
from apps.propostas.models import Proposta

class Contrato(models.Model):
    FORMA_PAGAMENTO_CHOICES = [
        ('vista', 'À Vista'),
        ('cartao', 'Cartão de Crédito'),
        ('financiamento', 'Financiamento Bancário'),
    ]
    
    numero = models.CharField(max_length=20, unique=True)
    proposta = models.OneToOneField(Proposta, on_delete=models.CASCADE, related_name='contrato')
    
    # Dados de pagamento
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total_extenso = models.CharField(max_length=500, blank=True, default='')
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    descricao_pagamento = models.TextField(blank=True, default='', help_text="Descrição detalhada da forma de pagamento")
    numero_parcelas = models.IntegerField(default=1)
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_parcela_extenso = models.CharField(max_length=500, blank=True, default='')
    
    # Datas importantes
    data_assinatura = models.DateField()
    data_inicio_obra = models.DateField(null=True, blank=True)
    data_conclusao = models.DateField(null=True, blank=True)
    prazo_execucao_dias = models.IntegerField(default=45)
    
    # Garantias
    garantia_instalacao_meses = models.IntegerField(default=12)
    
    # Arquivos
    pdf_contrato = models.FileField(upload_to='contratos/', null=True, blank=True)
    
    # Dados da empresa (CONTRATADA)
    empresa_razao_social = models.CharField(max_length=255, default='MAB ENERGIA SOLAR')
    empresa_cnpj = models.CharField(max_length=18, default='38.068.450/0001-99')
    empresa_endereco = models.CharField(max_length=500, default='Rua Maria Rosa, nº S/N, bairro Parque Ipanema')
    empresa_cidade = models.CharField(max_length=100, default='Itaporã')
    empresa_estado = models.CharField(max_length=2, default='MS')
    empresa_cep = models.CharField(max_length=9, default='79890-270')
    empresa_representante_nome = models.CharField(max_length=255, default='Mateus Leonço Concato')
    empresa_representante_cpf = models.CharField(max_length=14, default='051.536.511-42')
    empresa_representante_rg = models.CharField(max_length=20, default='001939969')
    
    # Dados bancários
    banco_nome = models.CharField(max_length=100, default='Banco Cooperativo Sicredi S.A.')
    banco_agencia = models.CharField(max_length=10, default='0903')
    banco_conta = models.CharField(max_length=20, default='50661-1')
    banco_titular = models.CharField(max_length=255, default='38.068.450 Mateus Leonco Concato')
    
    # Foro
    foro_comarca = models.CharField(max_length=100, default='Itaporã/MS')
    
    # Status
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'contratos'
        ordering = ['-data_assinatura']
    
    def __str__(self):
        return f"Contrato {self.numero} - {self.proposta.orcamento.cliente.nome}"
