from django.db import models
from apps.clientes.models import Cliente
from apps.vendedores.models import Vendedor

class Orcamento(models.Model):
    TIPO_ESTRUTURA_CHOICES = [
        ('ceramico', 'Cerâmico/Colonial'),
        ('fibromadeira', 'Fibromadeira'),
        ('fibrometal', 'Fibrometal'),
        ('zinco', 'Zinco'),
        ('solo', 'Solo'),
        ('laje', 'Laje'),
    ]
    
    numero = models.CharField(max_length=20, unique=True)
    nome_kit = models.CharField(max_length=255)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='orcamentos')
    vendedor = models.ForeignKey(Vendedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='orcamentos')
    
    # Kit
    valor_kit = models.DecimalField(max_digits=10, decimal_places=2)
    marca_painel = models.CharField(max_length=100)
    potencia_painel = models.IntegerField()
    quantidade_paineis = models.IntegerField()
    marca_inversor = models.CharField(max_length=100)
    potencia_inversor = models.IntegerField()
    quantidade_inversores = models.IntegerField(default=1)
    
    # Estrutura e custos
    tipo_estrutura = models.CharField(max_length=20, choices=TIPO_ESTRUTURA_CHOICES)
    valor_estrutura = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_material_eletrico = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Itens adicionais (JSON)
    itens_adicionais = models.JSONField(default=list, help_text="[{categoria, item, qtd, valor_unit, valor_total}]")
    
    # Totais
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(max_length=20, default='avista')
    taxa_juros = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    valor_final = models.DecimalField(max_digits=10, decimal_places=2)
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Margens personalizadas (salvas no momento da edição)
    margem_lucro_percentual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    comissao_percentual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    imposto_percentual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Controle
    data_criacao = models.DateField(auto_now_add=True)
    validade_dias = models.IntegerField(default=10)
    pdf_gerado = models.FileField(upload_to='orcamentos/', null=True, blank=True)
    convertido_proposta = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'orcamentos'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"Orçamento {self.numero} - {self.cliente.nome}"
