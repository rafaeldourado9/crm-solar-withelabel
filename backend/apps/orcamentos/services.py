from apps.premissas.models import Premissa
from apps.equipamentos.models import Equipamento

class SolarCalculator:
    def __init__(self):
        self.premissa = Premissa.get_ativa()
    
    def calcular_dimensionamento(self, consumo_kwh, painel_id, hsp_override=None, perda_override=None):
        """
        Calcula o dimensionamento do sistema fotovoltaico
        """
        painel = Equipamento.objects.get(id=painel_id, tipo='painel')
        
        hsp = hsp_override or self.premissa.hsp_padrao
        perda = perda_override or self.premissa.perda_padrao
        
        # Fórmula: Potência Wp = (Consumo / 30) / (HSP * (1 - perda))
        consumo_diario = consumo_kwh / 30
        potencia_necessaria_kw = consumo_diario / (hsp * (1 - perda))
        potencia_necessaria_wp = potencia_necessaria_kw * 1000
        
        # Calcular quantidade de painéis
        potencia_painel_wp = painel.potencia
        quantidade_paineis = int(potencia_necessaria_wp / potencia_painel_wp) + 1
        
        # Potência total instalada
        potencia_total_kwp = (quantidade_paineis * potencia_painel_wp) / 1000
        
        # Selecionar inversor compatível
        potencia_inversor_min = potencia_total_kwp * self.premissa.overload_inversor
        inversor = Equipamento.objects.filter(
            tipo='inversor',
            potencia__gte=potencia_inversor_min * 1000
        ).order_by('potencia').first()
        
        # Geração estimada mensal
        geracao_estimada_kwh = potencia_total_kwp * hsp * 30 * (1 - perda)
        
        return {
            'quantidade_paineis': quantidade_paineis,
            'potencia_total_kwp': round(potencia_total_kwp, 2),
            'painel': {
                'id': painel.id,
                'modelo': painel.modelo,
                'potencia': painel.potencia,
                'preco': float(painel.preco)
            },
            'inversor': {
                'id': inversor.id if inversor else None,
                'modelo': inversor.modelo if inversor else 'Não encontrado',
                'potencia': inversor.potencia if inversor else 0,
                'preco': float(inversor.preco) if inversor else 0
            } if inversor else None,
            'geracao_estimada_kwh': round(geracao_estimada_kwh, 2),
            'hsp_utilizado': hsp,
            'perda_utilizada': perda
        }
    
    def calcular_financeiro(self, dimensionamento, margem_lucro_override=None):
        """
        Calcula os valores financeiros do orçamento
        """
        margem = margem_lucro_override or self.premissa.margem_lucro_percentual
        
        # Custo dos equipamentos
        custo_paineis = dimensionamento['quantidade_paineis'] * dimensionamento['painel']['preco']
        custo_inversor = dimensionamento['inversor']['preco'] if dimensionamento['inversor'] else 0
        
        # Custos adicionais
        custo_montagem = float(self.premissa.montagem_por_painel) * dimensionamento['quantidade_paineis']
        custo_projeto = float(self.premissa.valor_projeto)
        
        # Custo total
        custo_total = custo_paineis + custo_inversor + custo_montagem + custo_projeto
        
        # Aplicar margem de lucro
        valor_venda = custo_total * (1 + margem / 100)
        
        # Aplicar impostos e comissões
        impostos = valor_venda * (float(self.premissa.imposto_percentual) / 100)
        comissao = valor_venda * (float(self.premissa.comissao_percentual) / 100)
        
        valor_final = valor_venda + impostos + comissao
        
        return {
            'custo_total': round(custo_total, 2),
            'valor_venda': round(valor_venda, 2),
            'impostos': round(impostos, 2),
            'comissao': round(comissao, 2),
            'valor_final': round(valor_final, 2),
            'detalhamento': {
                'custo_paineis': round(custo_paineis, 2),
                'custo_inversor': round(custo_inversor, 2),
                'custo_montagem': round(custo_montagem, 2),
                'custo_projeto': round(custo_projeto, 2)
            }
        }
    
    def calcular_parcelamento(self, valor_final, parcelas):
        """
        Calcula o valor parcelado com juros
        """
        taxas = self.premissa.taxa_juros_maquininha or {}
        taxa_juros = taxas.get(str(parcelas), 0)
        
        if taxa_juros == 0:
            return {
                'parcelas': parcelas,
                'valor_parcela': round(valor_final / parcelas, 2),
                'valor_total': valor_final,
                'taxa_juros': 0
            }
        
        # Cálculo com juros compostos
        valor_com_juros = valor_final * (1 + taxa_juros / 100)
        valor_parcela = valor_com_juros / parcelas
        
        return {
            'parcelas': parcelas,
            'valor_parcela': round(valor_parcela, 2),
            'valor_total': round(valor_com_juros, 2),
            'taxa_juros': taxa_juros
        }
    
    def calcular_completo(self, consumo_kwh, painel_id, parcelas=None, **overrides):
        """
        Calcula dimensionamento + financeiro + parcelamento
        """
        dimensionamento = self.calcular_dimensionamento(
            consumo_kwh, 
            painel_id,
            overrides.get('hsp'),
            overrides.get('perda')
        )
        
        financeiro = self.calcular_financeiro(
            dimensionamento,
            overrides.get('margem_lucro')
        )
        
        resultado = {
            **dimensionamento,
            **financeiro,
            'premissas': {
                'prazo_entrega_dias': self.premissa.prazo_entrega_dias,
                'garantia_instalacao_meses': self.premissa.garantia_instalacao_meses,
                'validade_proposta_dias': self.premissa.validade_proposta_dias
            }
        }
        
        if parcelas:
            resultado['parcelamento'] = self.calcular_parcelamento(
                financeiro['valor_final'],
                parcelas
            )
        
        return resultado
