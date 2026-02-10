from rest_framework import serializers
from .models import Premissa

class PremissaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Premissa
        fields = [
            'id',
            'margem_lucro_percentual',
            'comissao_percentual',
            'imposto_percentual',
            'margem_desconto_avista_percentual',
            'montagem_por_painel',
            'valor_projeto',
            'hsp_padrao',
            'perda_padrao',
            'overload_inversor',
            'tarifa_energia_atual',
            'inflacao_energetica_anual',
            'perda_eficiencia_anual',
            'material_eletrico_faixas',
            'cidade_empresa',
            'consumo_veiculo_km_por_litro',
            'preco_combustivel_litro',
            'margem_deslocamento_percentual',
            'cidades_sem_cobranca',
            'taxas_maquininha',
            'ativo',
            'created_at',
            'updated_at'
        ]
