from django.db import migrations

def atualizar_paineis(apps, schema_editor):
    Painel = apps.get_model('equipamentos', 'Painel')
    
    # Remover todos os painéis existentes
    Painel.objects.all().delete()
    
    # Novas marcas e potências
    marcas = ['Era Solar', 'OSDA', 'Sunova', 'BYD', 'DAH']
    potencias = [450, 500, 550, 600, 630, 650, 700, 705]
    
    # Criar 10 modelos de cada potência para cada marca
    paineis = []
    for marca in marcas:
        for potencia in potencias:
            for i in range(1, 11):
                modelo = f"{marca.replace(' ', '')}-{potencia}W-M{i}"
                paineis.append(Painel(
                    fabricante=marca,
                    modelo=modelo,
                    potencia_w=potencia,
                    area_m2=2.5,
                    eficiencia=0.21,
                    preco_unitario=0,
                    ativo=True
                ))
    
    Painel.objects.bulk_create(paineis)

class Migration(migrations.Migration):
    dependencies = [
        ('equipamentos', '0008_popular_equipamentos_completo'),
    ]

    operations = [
        migrations.RunPython(atualizar_paineis, migrations.RunPython.noop),
    ]
