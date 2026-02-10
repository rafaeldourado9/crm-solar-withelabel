#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django
import sys

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contratos.models import Contrato

# Buscar primeiro contrato
contrato = Contrato.objects.first()

if contrato:
    print(f"📄 Contrato: {contrato.numero}")
    print(f"👤 Cliente: {contrato.proposta.orcamento.cliente.nome}")
    print(f"💰 Valor: R$ {contrato.valor_total}")
    print(f"📅 Data: {contrato.data_assinatura}")
    print(f"💳 Forma: {contrato.get_forma_pagamento_display()}")
    print(f"📦 Parcelas: {contrato.numero_parcelas}x de R$ {contrato.valor_parcela}")
    
    cliente = contrato.proposta.orcamento.cliente
    print(f"\n✅ Dados do cliente completos:")
    print(f"   Nome: {cliente.nome}")
    print(f"   CPF: {cliente.cpf_cnpj}")
    print(f"   Telefone: {cliente.telefone}")
    print(f"   Email: {cliente.email}")
    print(f"   Endereço: {cliente.endereco}")
    print(f"   Bairro: {cliente.bairro}")
    print(f"   Cidade: {cliente.cidade}")
    print(f"   Estado: {cliente.estado}")
    print(f"   CEP: {cliente.cep}")
else:
    print("❌ Nenhum contrato encontrado")
