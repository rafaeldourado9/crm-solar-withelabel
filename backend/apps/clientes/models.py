from django.db import models

class Cliente(models.Model):
    STATUS_CHOICES = [
        ('orcamento', 'Orçamento'),
        ('proposta', 'Proposta'),
        ('contrato', 'Contrato'),
    ]
    
    nome = models.CharField(max_length=255)
    cpf_cnpj = models.CharField(max_length=18, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, blank=True)
    cep = models.CharField(max_length=9, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='orcamento')
    criado_por = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='clientes_criados')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'clientes'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.nome
