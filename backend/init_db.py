import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

print("🔄 Executando migrações...")
call_command('migrate')

print("✅ Banco de dados inicializado!")
print("\n📝 Para criar um superusuário, execute:")
print("   python manage.py createsuperuser")
