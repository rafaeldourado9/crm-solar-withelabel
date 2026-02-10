from django.db import migrations


def sync_vendedor_orcamentos(apps, schema_editor):
    """Sincroniza vendedor dos orçamentos com vendedor do cliente"""
    Orcamento = apps.get_model('orcamentos', 'Orcamento')
    
    for orcamento in Orcamento.objects.select_related('cliente').all():
        if orcamento.cliente and orcamento.cliente.vendedor:
            orcamento.vendedor = orcamento.cliente.vendedor
            orcamento.save(update_fields=['vendedor'])


class Migration(migrations.Migration):

    dependencies = [
        ('orcamentos', '0011_add_margens_personalizadas'),
    ]

    operations = [
        migrations.RunPython(sync_vendedor_orcamentos, migrations.RunPython.noop),
    ]
