# Generated migration to populate default solar panels

from django.db import migrations

def popular_paineis(apps, schema_editor):
    Painel = apps.get_model('equipamentos', 'Painel')
    
    marcas_paineis = {
        'Canadian Solar': [330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600],
        'JA Solar': [330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580],
        'Jinko Solar': [330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590],
        'LONGi': [340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600],
        'Trina Solar': [330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580],
        'BYD': [330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550],
        'Risen': [330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560],
    }
    
    paineis = []
    for marca, potencias in marcas_paineis.items():
        for potencia in potencias:
            modelo = f"Painel {potencia}W"
            paineis.append(
                Painel(
                    fabricante=marca,
                    modelo=modelo,
                    potencia_w=potencia
                )
            )
    
    Painel.objects.bulk_create(paineis, ignore_conflicts=True)

def remover_paineis(apps, schema_editor):
    Painel = apps.get_model('equipamentos', 'Painel')
    Painel.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0006_expandir_inversores'),
    ]

    operations = [
        migrations.RunPython(popular_paineis, remover_paineis),
    ]
