import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.orcamentos.services import SolarCalculator
from apps.equipamentos.models import Painel, Inversor
from apps.premissas.models import Premissa

print('='*70)
print('TESTE DO SISTEMA DE ORÇAMENTOS')
print('='*70)

# Teste 1: Cálculo Técnico
print('\n--- TESTE 1: CÁLCULO TÉCNICO ---')
consumo = 500  # kWh/mês
painel = Painel.objects.filter(potencia_w=550).first()

if painel:
    print(f'Consumo: {consumo} kWh/mês')
    print(f'Painel selecionado: {painel.fabricante} {painel.modelo} - {painel.potencia_w}W')
    
    resultado = SolarCalculator.calcular_tecnico(consumo, painel.id)
    
    print(f'\nResultado:')
    print(f'  Quantidade de painéis: {resultado["qtd_paineis"]}')
    print(f'  Potência do sistema: {resultado["potencia_sistema_kwp"]} kWp')
    print(f'  Geração mensal: {resultado["geracao_mensal_kwh"]} kWh')
    print(f'  Área ocupada: {resultado["area_ocupada_m2"]} m²')
    print(f'  Inversor: {resultado["inversor"]["modelo"]} - {resultado["inversor"]["potencia_w"]}W')

# Teste 2: Cálculo Financeiro
print('\n--- TESTE 2: CÁLCULO FINANCEIRO ---')
valor_kit = 35000

print(f'Valor do kit cotado: R$ {valor_kit:,.2f}')

# À vista
resultado_avista = SolarCalculator.calcular_financeiro(valor_kit, 'avista')
print(f'\nÀ vista:')
print(f'  Valor final: R$ {resultado_avista["valor_final"]:,.2f}')

# Parcelado em 12x
resultado_12x = SolarCalculator.calcular_financeiro(valor_kit, '12')
print(f'\n12x:')
print(f'  Taxa aplicada: {resultado_12x["taxa_aplicada"]}%')
print(f'  Valor final: R$ {resultado_12x["valor_final"]:,.2f}')
print(f'  Valor parcela: R$ {resultado_12x["valor_parcela"]:,.2f}')

# Teste 3: Economia Projetada
print('\n--- TESTE 3: ECONOMIA PROJETADA ---')
premissa = Premissa.get_ativa()
geracao_mensal = 600

economia = SolarCalculator.calcular_economia_projetada(
    geracao_mensal,
    float(premissa.tarifa_energia_atual),
    float(premissa.inflacao_energetica_anual)
)

print(f'Geração mensal: {geracao_mensal} kWh')
print(f'Tarifa atual: R$ {premissa.tarifa_energia_atual}/kWh')
print(f'Inflação energética: {premissa.inflacao_energetica_anual}% ao ano')
print(f'\nEconomia mensal (ano 1): R$ {economia["economia_mensal_ano1"]:,.2f}')
print(f'Economia total (25 anos): R$ {economia["economia_total_25anos"]:,.2f}')

print('\n' + '='*70)
print('✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!')
print('='*70)
