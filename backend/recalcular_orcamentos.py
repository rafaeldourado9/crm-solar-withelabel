import os
import django
from decimal import Decimal, ROUND_UP, ROUND_HALF_UP

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.orcamentos.models import Orcamento
from apps.premissas.models import Premissa

def recalcular_orcamento(orcamento):
    premissa = Premissa.get_ativa()
    
    # Calcular totais
    valor_kit = orcamento.valor_kit
    valor_projeto = premissa.valor_projeto
    valor_montagem = premissa.montagem_por_painel * orcamento.quantidade_paineis
    valor_estrutura = orcamento.valor_estrutura
    valor_material_eletrico = orcamento.valor_material_eletrico
    
    # Somar itens adicionais
    valor_adicionais = sum(
        Decimal(str(item.get('valor_total', 0))) 
        for item in orcamento.itens_adicionais
    )
    
    # Subtotal
    subtotal = (
        valor_kit + valor_projeto + valor_montagem + 
        valor_estrutura + valor_material_eletrico + valor_adicionais
    )
    
    # Adicionar margens (comissão, lucro, imposto)
    comissao = subtotal * (premissa.comissao_percentual / 100)
    lucro = subtotal * (premissa.margem_lucro_percentual / 100)
    imposto = subtotal * (premissa.imposto_percentual / 100)
    
    valor_total = subtotal + comissao + lucro + imposto
    
    # Arredondar valor_total para centena mais próxima
    valor_total_arredondado = (valor_total / 100).quantize(Decimal('1'), rounding=ROUND_UP) * 100
    
    # Adicionar margem de desconto
    margem_desconto = valor_total_arredondado * (premissa.margem_desconto_avista_percentual / 100)
    valor_final = valor_total_arredondado + margem_desconto
    
    # Arredondar valor final
    valor_final = (valor_final / 100).quantize(Decimal('1'), rounding=ROUND_UP) * 100
    
    # Aplicar taxa de juros se parcelado
    forma_pagamento = orcamento.forma_pagamento
    valor_parcela = None
    
    if forma_pagamento != 'avista':
        taxa_juros = orcamento.taxa_juros
        valor_final = valor_final * (1 + taxa_juros / 100)
        valor_final = valor_final.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        valor_parcela = (valor_final / int(forma_pagamento)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # Atualizar
    orcamento.valor_total = subtotal
    orcamento.valor_final = valor_final
    orcamento.valor_parcela = valor_parcela
    orcamento.save()
    
    print(f"✓ {orcamento.numero} - {orcamento.nome_kit}: R$ {valor_final}")

print("Recalculando orcamentos com todas as margens...\n")
orcamentos = Orcamento.objects.all()
for orc in orcamentos:
    recalcular_orcamento(orc)

print(f"\n✅ {orcamentos.count()} orçamentos recalculados com sucesso!")
