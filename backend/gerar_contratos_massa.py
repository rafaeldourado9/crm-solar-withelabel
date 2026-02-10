#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para gerar 3000 contratos em massa para teste de performance
"""

import os
import django
import sys
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Configurar Django
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contratos.models import Contrato
from apps.propostas.models import Proposta
from apps.orcamentos.models import Orcamento
from apps.clientes.models import Cliente
from apps.vendedores.models import Vendedor
from apps.contratos.utils import numero_por_extenso

def gerar_contratos_massa():
    print("🔄 Iniciando geração de 3000 contratos...\n")
    
    # Buscar propostas aceitas sem contrato
    propostas = Proposta.objects.filter(status='aceita', contrato__isnull=True)[:3000]
    
    if not propostas.exists():
        print("❌ Não há propostas aceitas disponíveis")
        print("💡 Gerando propostas primeiro...")
        
        # Buscar orçamentos sem proposta
        orcamentos = Orcamento.objects.filter(proposta__isnull=True)[:3000]
        
        if not orcamentos.exists():
            print("❌ Não há orçamentos disponíveis")
            return
        
        # Criar propostas em lote
        propostas_criar = []
        for i, orc in enumerate(orcamentos, 1):
            propostas_criar.append(Proposta(
                numero=f"PROP-{datetime.now().year}-{10000 + i}",
                orcamento=orc,
                cpf_cnpj=orc.cliente.cpf_cnpj or '000.000.000-00',
                endereco_completo=orc.cliente.endereco or 'Rua Teste',
                bairro=orc.cliente.bairro or 'Centro',
                cep=orc.cliente.cep or '00000-000',
                status='aceita',
                data_aceite=datetime.now().date()
            ))
            
            if len(propostas_criar) >= 100:
                Proposta.objects.bulk_create(propostas_criar)
                print(f"✓ {i} propostas criadas")
                propostas_criar = []
        
        if propostas_criar:
            Proposta.objects.bulk_create(propostas_criar)
            print(f"✓ Total de propostas criadas")
        
        propostas = Proposta.objects.filter(status='aceita', contrato__isnull=True)[:3000]
    
    # Gerar contratos
    contratos_criar = []
    formas_pagamento = ['vista', 'cartao', 'financiamento']
    
    for i, proposta in enumerate(propostas, 1):
        forma = random.choice(formas_pagamento)
        valor_total = proposta.orcamento.valor_final
        
        if forma == 'vista':
            num_parcelas = 1
            valor_parcela = valor_total
            descricao = f"Pagamento à vista no valor de R$ {valor_total}"
        elif forma == 'cartao':
            num_parcelas = random.choice([6, 12, 18])
            valor_parcela = valor_total * Decimal('1.18') / num_parcelas
            descricao = f"Pagamento em {num_parcelas}x de R$ {valor_parcela:.2f} no cartão de crédito"
        else:
            num_parcelas = random.choice([24, 36, 48])
            valor_parcela = valor_total * Decimal('1.25') / num_parcelas
            descricao = f"Financiamento bancário em {num_parcelas}x de R$ {valor_parcela:.2f}"
        
        contratos_criar.append(Contrato(
            numero=f"CONT-{datetime.now().year}-{20000 + i}",
            proposta=proposta,
            valor_total=valor_total,
            valor_total_extenso=numero_por_extenso(float(valor_total)),
            forma_pagamento=forma,
            descricao_pagamento=descricao,
            numero_parcelas=num_parcelas,
            valor_parcela=valor_parcela,
            valor_parcela_extenso=numero_por_extenso(float(valor_parcela)),
            data_assinatura=datetime.now().date() - timedelta(days=random.randint(0, 90)),
            prazo_execucao_dias=45,
            garantia_instalacao_meses=12
        ))
        
        if len(contratos_criar) >= 100:
            Contrato.objects.bulk_create(contratos_criar)
            print(f"✓ {i} contratos criados")
            contratos_criar = []
    
    if contratos_criar:
        Contrato.objects.bulk_create(contratos_criar)
    
    total = Contrato.objects.count()
    print(f"\n✅ Geração concluída!")
    print(f"📊 Total de contratos no sistema: {total}")

if __name__ == '__main__':
    gerar_contratos_massa()
