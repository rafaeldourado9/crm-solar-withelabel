from django.db import models

class Premissa(models.Model):
    # Margens e Serviços
    margem_lucro_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=18.0, help_text="% de lucro")
    comissao_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=5.0, help_text="% de comissão")
    imposto_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=6.0, help_text="% de imposto")
    margem_desconto_avista_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=2.0, help_text="% margem para desconto")
    montagem_por_painel = models.DecimalField(max_digits=10, decimal_places=2, default=70, help_text="R$ por painel")
    valor_projeto = models.DecimalField(max_digits=10, decimal_places=2, default=400, help_text="R$ valor fixo")
    
    # Parâmetros Técnicos (Opcionais)
    hsp_padrao = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Horas de Sol Pleno")
    perda_padrao = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Performance ratio")
    overload_inversor = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Overload padrão")
    
    # Material Elétrico
    material_eletrico_faixas = models.JSONField(
        default=dict,
        help_text="Faixas de potência em kWp"
    )
    
    # Deslocamento
    cidade_empresa = models.CharField(max_length=200, default='Itaporã, MS', help_text="Cidade sede da empresa")
    consumo_veiculo_km_por_litro = models.DecimalField(max_digits=5, decimal_places=2, default=10.0, help_text="Km por litro")
    preco_combustivel_litro = models.DecimalField(max_digits=6, decimal_places=2, default=6.75, help_text="R$ por litro")
    cidades_sem_cobranca = models.JSONField(
        default=list,
        help_text="Cidades sem cobrança de deslocamento"
    )
    
    # Parcelamento
    taxas_maquininha = models.JSONField(
        default=dict,
        help_text="Taxas por quantidade de parcelas"
    )
    
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
        premissa = cls.objects.filter(ativo=True).first()
        if not premissa:
            premissa = cls.objects.create(
                margem_lucro_percentual=18.0,
                comissao_percentual=5.0,
                imposto_percentual=6.0,
                margem_desconto_avista_percentual=2.0,
                montagem_por_painel=70,
                valor_projeto=400,
                material_eletrico_faixas={'3': 250, '5': 350, '6': 400, '8': 500, '10': 900},
                cidade_empresa='Itaporã, MS',
                consumo_veiculo_km_por_litro=10.0,
                preco_combustivel_litro=6.75,
                cidades_sem_cobranca=['Itaporã', 'Dourados'],
                taxas_maquininha={'2': 2.5, '3': 3.5, '6': 5.0, '12': 8.0}
            )
        return premissa
