from django.contrib import admin
from .models import Premissa

@admin.register(Premissa)
class PremissaAdmin(admin.ModelAdmin):
    list_display = ['id', 'margem_lucro_percentual', 'comissao_percentual', 'imposto_percentual', 'ativo', 'created_at']
    list_filter = ['ativo']
    
    fieldsets = (
        ('Margens e Serviços', {
            'fields': ('margem_lucro_percentual', 'comissao_percentual', 'imposto_percentual', 'margem_desconto_avista_percentual', 'montagem_por_painel', 'valor_projeto')
        }),
        ('Parâmetros Técnicos (Opcional)', {
            'fields': ('hsp_padrao', 'perda_padrao', 'overload_inversor'),
            'classes': ('collapse',)
        }),
        ('Material Elétrico', {
            'fields': ('material_eletrico_faixas',)
        }),
        ('Deslocamento', {
            'fields': ('cidade_empresa', 'consumo_veiculo_km_por_litro', 'preco_combustivel_litro', 'cidades_sem_cobranca')
        }),
        ('Parcelamento', {
            'fields': ('taxas_maquininha',)
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )
