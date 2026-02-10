import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.equipamentos.models import Inversor, Painel

print("🔍 Verificando equipamentos...")
print()

inversores = Inversor.objects.count()
paineis = Painel.objects.count()

print(f"📊 Inversores: {inversores}")
print(f"📊 Painéis: {paineis}")
print()

if inversores == 0 or paineis == 0:
    print("❌ ERRO: Equipamentos não carregados!")
    print()
    print("Executando migração de dados...")
    
    from django.core.management import call_command
    call_command('migrate', 'equipamentos', '0008')
    
    inversores = Inversor.objects.count()
    paineis = Painel.objects.count()
    
    print(f"✅ Inversores carregados: {inversores}")
    print(f"✅ Painéis carregados: {paineis}")
else:
    print("✅ Equipamentos já carregados!")
    
print()
print("📋 Exemplos:")
print(f"  - Inversores 3kW: {Inversor.objects.filter(potencia_w=3000).count()}")
print(f"  - Painéis 550W: {Painel.objects.filter(potencia_w=550).count()}")
