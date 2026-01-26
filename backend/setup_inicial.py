import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.clientes.models import Cliente
from apps.premissas.models import Premissa

User = get_user_model()

# Criar superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
    print('✅ Superuser criado: admin/admin123')

# Criar premissa padrão
if not Premissa.objects.exists():
    Premissa.objects.create(
        material_eletrico_faixas={'3': 250, '5': 350, '6': 450, '10': 600},
        taxas_maquininha={'12': 12.5, '18': 18.3, '24': 25.0}
    )
    print('✅ Premissas criadas')

# Criar cliente de teste
if not Cliente.objects.exists():
    Cliente.objects.create(
        nome='João Silva',
        cidade='São Paulo',
        telefone='11999999999',
        email='joao@email.com'
    )
    print('✅ Cliente de teste criado')

print('\n✅ Setup completo!')
