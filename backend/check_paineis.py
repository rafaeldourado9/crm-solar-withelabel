import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.equipamentos.models import Painel

print('Total painéis:', Painel.objects.count())
print('\nPor potência:')
for p in [450, 500, 550, 600, 630, 650, 700, 705]:
    count = Painel.objects.filter(potencia_w=p).count()
    print(f'{p}W: {count}')

print('\nPrimeiros 20 painéis:')
for painel in Painel.objects.all()[:20]:
    print(f'{painel.fabricante} - {painel.modelo} - {painel.potencia_w}W')
