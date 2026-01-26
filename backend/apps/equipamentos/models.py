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

class Painel(models.Model):
    modelo = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    potencia_w = models.IntegerField(help_text="Potência em Watts")
    area_m2 = models.DecimalField(max_digits=5, decimal_places=2, default=2.5)
    eficiencia = models.DecimalField(max_digits=5, decimal_places=2, default=0.21, help_text="Ex: 0.21 = 21%")
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'paineis'
        ordering = ['-potencia_w']
    
    def __str__(self):
        return f"{self.modelo} - {self.potencia_w}W"

class Inversor(models.Model):
    OVERLOAD_CHOICES = [
        (0.50, '50%'),
        (0.60, '60%'),
        (0.70, '70%'),
        (0.80, '80%'),
    ]
    
    modelo = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    potencia_w = models.IntegerField(help_text="Potência nominal em Watts")
    potencia_maxima_w = models.IntegerField(help_text="Potência máxima suportada")
    overload = models.DecimalField(max_digits=3, decimal_places=2, default=0.70, choices=OVERLOAD_CHOICES, help_text="Capacidade de overload")
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'inversores'
        ordering = ['potencia_w']
    
    def __str__(self):
        return f"{self.modelo} - {self.potencia_w}W"
