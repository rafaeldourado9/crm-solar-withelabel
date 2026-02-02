from django.core.management.base import BaseCommand
from apps.templates.models import Template

class Command(BaseCommand):
    help = 'Ativa todos os templates existentes'

    def handle(self, *args, **options):
        count = Template.objects.all().update(ativo=True)
        self.stdout.write(self.style.SUCCESS(f'✓ {count} template(s) ativado(s) com sucesso!'))
