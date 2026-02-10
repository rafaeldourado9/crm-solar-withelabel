import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.clientes.models import Cliente
from apps.vendedores.models import Vendedor
from apps.orcamentos.models import Orcamento
from apps.contratos.models import Contrato

print("🗑️  Removendo dados...")

# Remover contratos
contratos_count = Contrato.objects.count()
Contrato.objects.all().delete()
print(f"✅ {contratos_count} contratos removidos")

# Remover orçamentos
orcamentos_count = Orcamento.objects.count()
Orcamento.objects.all().delete()
print(f"✅ {orcamentos_count} orçamentos removidos")

# Remover clientes
clientes_count = Cliente.objects.count()
Cliente.objects.all().delete()
print(f"✅ {clientes_count} clientes removidos")

# Remover vendedores
vendedores_count = Vendedor.objects.count()
Vendedor.objects.all().delete()
print(f"✅ {vendedores_count} vendedores removidos")

print("\n✨ Limpeza concluída!")
