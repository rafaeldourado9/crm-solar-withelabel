from django.db import models

class Premissa(models.Model):
    hsp_padrao = models.DecimalField(max_digits=5, decimal_places=2, default=4.85, help_text="Horas de Sol Pleno")
    tarifa_energia_atual = models.DecimalField(max_digits=6, decimal_places=2, default=1.05, help_text="R$/kWh")
    inflacao_energetica_anual = models.DecimalField(max_digits=5, decimal_places=2, default=10.0, help_text="%")
    perda_eficiencia_anual = models.DecimalField(max_digits=5, decimal_places=2, default=0.8, help_text="%")
    perda_padrao = models.DecimalField(max_digits=5, decimal_places=2, default=0.20, help_text="Performance ratio")
    prazo_entrega_padrao = models.IntegerField(default=45, help_text="Dias")
    garantia_instalacao_meses = models.IntegerField(default=12)
    taxas_maquininha = models.JSONField(default=dict, help_text="Ex: {'12': 12.5, '18': 18.3, '24': 25.0}")
    margem_lucro_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=30.0)
    overload_inversor = models.DecimalField(max_digits=5, decimal_places=2, default=0.75)
    imposto_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    comissao_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    montagem_por_painel = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_projeto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'premissas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Premissa {self.id} - {self.created_at.strftime('%d/%m/%Y')}"
    
    @classmethod
    def get_ativa(cls):
        return cls.objects.filter(ativo=True).first() or cls.objects.create()
