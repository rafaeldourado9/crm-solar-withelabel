from django.db import models

class Equipamento(models.Model):
    CATEGORIA_CHOICES = [
        ('kit', 'Kit'),
        ('servicos', 'Serviços'),
        ('custos', 'Custos'),
    ]
    
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    item = models.CharField(max_length=255)
    codigo = models.CharField(max_length=50, unique=True)
    quantidade = models.IntegerField(default=0)
    custo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    custo_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'equipamentos'
        ordering = ['categoria', 'item']
    
    def save(self, *args, **kwargs):
        self.custo_total = self.quantidade * self.custo_unitario
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.categoria} - {self.item}"
