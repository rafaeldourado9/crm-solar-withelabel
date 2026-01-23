from django.db import models
from apps.clientes.models import Cliente
from apps.vendedores.models import Vendedor

class Orcamento(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='orcamentos')
    vendedor = models.ForeignKey(Vendedor, on_delete=models.SET_NULL, null=True, related_name='orcamentos')
    
    # Dados do dimensionamento
    consumo_medio_kwh = models.DecimalField(max_digits=10, decimal_places=2)
    geracao_requerida_kwh = models.DecimalField(max_digits=10, decimal_places=2)
    potencia_instalada_kwp = models.DecimalField(max_digits=10, decimal_places=2)
    potencia_placas_w = models.IntegerField()
    quantidade_placas = models.IntegerField()
    area_necessaria_m2 = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Equipamentos
    modelo_placa = models.CharField(max_length=255)
    modelo_inversor = models.CharField(max_length=255)
    quantidade_inversores = models.IntegerField(default=1)
    
    # Valores
    custo_atual_energia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custo_com_sistema = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    economia_mensal = models.DecimalField(max_digits=10, decimal_places=2)
    economia_percentual = models.DecimalField(max_digits=5, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    
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
