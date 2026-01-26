from django.db import models
from apps.orcamentos.models import Orcamento

class Proposta(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceita', 'Aceita'),
        ('recusada', 'Recusada'),
    ]
    
    numero = models.CharField(max_length=20, unique=True)
    orcamento = models.OneToOneField(Orcamento, on_delete=models.CASCADE, related_name='proposta')
    
    # Dados completos do cliente (coletados nesta etapa)
    cpf_cnpj = models.CharField(max_length=18)
    endereco_completo = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    cep = models.CharField(max_length=9)
    
    # Status e datas
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_criacao = models.DateField(auto_now_add=True)
    data_aceite = models.DateField(null=True, blank=True)
    dias_desde_aceite = models.IntegerField(default=0)
    
    # Prazos (em dias)
    prazo_entrega = models.IntegerField(default=45)
    prazo_vistoria = models.IntegerField(default=60)
    prazo_monitoramento = models.IntegerField(default=90)
    
    # Arquivos
    pdf_proposta = models.FileField(upload_to='propostas/', null=True, blank=True)
    convertido_contrato = models.BooleanField(default=False)
    
    # Margens personalizadas (salvas no momento da criação/edição)
    margem_lucro_percentual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    comissao_percentual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    imposto_percentual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        db_table = 'propostas'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"Proposta {self.numero} - {self.orcamento.cliente.nome}"
