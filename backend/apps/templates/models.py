from django.db import models

class Template(models.Model):
    TIPO_CHOICES = [
        ('orcamento', 'Orçamento'),
        ('contrato', 'Contrato'),
    ]
    
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    arquivo = models.FileField(upload_to='templates/')
    arquivo_nome = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'templates'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"
