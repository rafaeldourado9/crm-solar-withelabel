from django.db import models
from django.contrib.auth.models import User

class Vendedor(models.Model):
    TIPO_CHOICES = [
        ('vendedor', 'Vendedor'),
        ('indicacao', 'Indicação'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='vendedor')
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='vendedor')
    ativo = models.BooleanField(default=True)
    bloqueado = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'vendedores'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

class VendaVendedor(models.Model):
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='vendas')
    contrato = models.ForeignKey('contratos.Contrato', on_delete=models.CASCADE)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2)
    valor_comissao = models.DecimalField(max_digits=10, decimal_places=2)
    data_venda = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    pago = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'vendas_vendedor'
        ordering = ['-data_venda']
