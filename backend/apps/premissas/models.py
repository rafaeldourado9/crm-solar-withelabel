from django.db import models

class Premissa(models.Model):
    hsp_padrao = models.FloatField(default=4.85, help_text="Horas de Sol Pico padrão")
    perda_padrao = models.FloatField(default=0.20, help_text="Perda padrão do sistema (0.20 = 20%)")
    prazo_entrega_dias = models.IntegerField(default=45)
    garantia_instalacao_meses = models.IntegerField(default=12)
    taxa_juros_maquininha = models.JSONField(default=dict, help_text="Ex: {'12': 10.5, '18': 18.3}")
    margem_lucro_percentual = models.FloatField(default=30.0, help_text="Margem de lucro padrão (%)")
    overload_inversor = models.FloatField(default=0.75, help_text="Fator de overload do inversor")
    imposto_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    comissao_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    montagem_por_painel = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_projeto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taxa_inflacao_anual = models.DecimalField(max_digits=5, decimal_places=2, default=9.5)
    tempo_vida_minima = models.IntegerField(default=25)
    validade_proposta_dias = models.IntegerField(default=10)
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
