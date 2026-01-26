from decimal import Decimal
import math
from apps.premissas.models import Premissa
from apps.equipamentos.models import Painel, Inversor

class SolarCalculator:
    
    @staticmethod
    def calcular_tecnico(consumo_mensal, painel_id, hsp_custom=None):
        """
        Calcula dimensionamento técnico do sistema solar
        """
        premissa = Premissa.get_ativa()
        painel = Painel.objects.get(id=painel_id, ativo=True)
        
        hsp = Decimal(str(hsp_custom)) if hsp_custom else premissa.hsp_padrao
        perda = premissa.perda_padrao
        
        # Potência necessária (Wp)
        consumo_diario = Decimal(str(consumo_mensal)) / 30
        potencia_necessaria = consumo_diario / (hsp * (1 - perda))
        
        # Quantidade de painéis (arredondar para cima)
        qtd_paineis = math.ceil(potencia_necessaria / painel.potencia_w)
        
        # Potência total do sistema (kWp)
        potencia_sistema = (qtd_paineis * painel.potencia_w) / 1000
        
        # Buscar inversor compatível
        potencia_minima_inversor = potencia_sistema * 1000 * float(premissa.overload_inversor)
        inversor = Inversor.objects.filter(
            potencia_w__gte=potencia_minima_inversor,
            ativo=True
        ).first()
        
        if not inversor:
            raise ValueError("Nenhum inversor compatível encontrado")
        
        # Geração mensal estimada (kWh)
        geracao_mensal = potencia_sistema * float(hsp) * 30 * (1 - float(perda))
        
        # Área ocupada
        area_ocupada = qtd_paineis * float(painel.area_m2)
        
        return {
            'qtd_paineis': qtd_paineis,
            'potencia_sistema_kwp': round(potencia_sistema, 2),
            'geracao_mensal_kwh': round(geracao_mensal, 2),
            'area_ocupada_m2': round(area_ocupada, 2),
            'inversor': {
                'id': inversor.id,
                'modelo': inversor.modelo,
                'potencia_w': inversor.potencia_w
            },
            'painel': {
                'id': painel.id,
                'modelo': painel.modelo,
                'potencia_w': painel.potencia_w,
                'preco_unitario': float(painel.preco_unitario)
            },
            'hsp_utilizado': float(hsp),
            'perda_utilizada': float(perda)
        }
    
    @staticmethod
    def calcular_financeiro(valor_kit_base, forma_pagamento):
        """
        Calcula valor final com base na forma de pagamento
        forma_pagamento: "avista" ou "12", "18", "24" (número de parcelas)
        """
        premissa = Premissa.get_ativa()
        valor_base = Decimal(str(valor_kit_base))
        
        if forma_pagamento == "avista" or not forma_pagamento:
            return {
                'valor_final': float(valor_base),
                'valor_parcela': None,
                'taxa_aplicada': 0,
                'parcelas': None
            }
        
        # Buscar taxa no JSON
        taxas = premissa.taxas_maquininha
        taxa_percentual = Decimal(str(taxas.get(str(forma_pagamento), 0)))
        
        # Aplicar taxa (juros simples)
        valor_final = valor_base * (1 + (taxa_percentual / 100))
        valor_parcela = valor_final / int(forma_pagamento)
        
        return {
            'valor_final': round(float(valor_final), 2),
            'valor_parcela': round(float(valor_parcela), 2),
            'taxa_aplicada': float(taxa_percentual),
            'parcelas': int(forma_pagamento)
        }
    
    @staticmethod
    def calcular_economia_projetada(geracao_mensal, tarifa_energia, inflacao_anual, anos=25):
        """
        Calcula economia projetada considerando inflação energética
        """
        economia_total = 0
        tarifa_atual = Decimal(str(tarifa_energia))
        inflacao = Decimal(str(inflacao_anual)) / 100
        geracao = Decimal(str(geracao_mensal))
        
        for ano in range(1, anos + 1):
            economia_anual = geracao * 12 * tarifa_atual
            economia_total += float(economia_anual)
            tarifa_atual *= (1 + inflacao)
        
        return {
            'economia_total_25anos': round(economia_total, 2),
            'economia_mensal_ano1': round(float(geracao * Decimal(str(tarifa_energia))), 2)
        }
