import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.equipamentos.models import Inversor

# Mapeamento de fabricantes e seus overloads corretos
overload_por_fabricante = {
    'Solis': 1.70,      # 70% overload
    'Deye': 1.50,       # 50% overload
    'SAJ': 2.00,        # 100% overload
    'Growatt': 1.50,    # 50% overload
    'Fronius': 1.50,    # 50% overload
    'SMA': 1.50,        # 50% overload
    'ABB': 1.50,        # 50% overload
    'Huawei': 1.50,     # 50% overload
    'Goodwe': 1.50,     # 50% overload
}

print("Corrigindo valores de overload...\n")

inversores = Inversor.objects.all()
for inv in inversores:
    # Buscar overload correto para o fabricante
    overload_correto = overload_por_fabricante.get(inv.fabricante, 1.50)  # Padrão 50%
    
    if inv.overload != overload_correto:
        print(f"✓ {inv.fabricante} {inv.potencia_w}W: {inv.overload} → {overload_correto}")
        inv.overload = overload_correto
        inv.save()

print(f"\n✅ {inversores.count()} inversores verificados!")
print("\nOverloads configurados:")
for fab, over in sorted(overload_por_fabricante.items()):
    print(f"  {fab}: {int((over - 1) * 100)}%")
