#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django
import sys

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.clientes.models import Cliente

print("🔄 Completando dados dos clientes...\n")

clientes = Cliente.objects.filter(cpf_cnpj='')
total = clientes.count()

for i, cliente in enumerate(clientes, 1):
    cliente.cpf_cnpj = f"{str(i).zfill(3)}.{str(i).zfill(3)}.{str(i).zfill(3)}-{str(i % 100).zfill(2)}"
    cliente.endereco = f"Rua Teste, nº {i}"
    cliente.bairro = "Centro"
    cliente.cep = f"{str(i % 100000).zfill(5)}-{str(i % 1000).zfill(3)}"
    cliente.save()
    
    if i % 100 == 0:
        print(f"✓ {i}/{total} clientes atualizados")

print(f"\n✅ {total} clientes atualizados com sucesso!")
