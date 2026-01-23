import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.equipamentos.models import Inversor

print('Total inversores:', Inversor.objects.count())
for marca in ['ABB', 'Auxsol', 'Chint', 'Deye', 'Growatt', 'Solis', 'Sungrow']:
    count = Inversor.objects.filter(fabricante=marca).count()
    print(f'{marca}: {count}')
