from django.db import migrations

def popular_equipamentos(apps, schema_editor):
    Inversor = apps.get_model('equipamentos', 'Inversor')
    Painel = apps.get_model('equipamentos', 'Painel')
    
    # INVERSORES - Máximo 3 modelos por potência por marca
    marcas_inv = ['Chint', 'Deye', 'Growatt', 'Solis', 'Sungrow']
    series_inv = ['S1', 'S2', 'S3']  # Apenas 3 séries
    potencias_inv = [1000, 1200, 1500, 2000, 2500, 3000, 3300, 3600, 4000, 4200, 4600, 5000, 5500, 6000,
                     7000, 8000, 10000, 12000, 15000, 17000, 20000, 25000, 30000, 33000,
                     36000, 40000, 50000, 60000, 75000, 80000, 100000, 110000, 125000, 150000]
    
    inversores = []
    for marca in marcas_inv:
        for pot in potencias_inv:
            for i, serie in enumerate(series_inv, 1):
                kw = pot / 1000
                modelo = f"{serie}-{kw:.1f}K" if kw < 10 else f"{serie}-{int(kw)}K"
                inversores.append(Inversor(
                    fabricante=marca,
                    modelo=modelo,
                    potencia_w=pot,
                    potencia_maxima_w=int(pot * 1.15)
                ))
    Inversor.objects.bulk_create(inversores)
    
    # PAINÉIS - Máximo 3 modelos por potência por marca
    marcas_painel = ['Chint', 'Deye', 'Growatt', 'Solis', 'Sungrow']
    series_painel = ['P1', 'P2', 'P3']  # Apenas 3 séries
    potencias_painel = [350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500,
                        510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650]
    
    paineis = []
    for marca in marcas_painel:
        for pot in potencias_painel:
            for serie in series_painel:
                modelo = f"{serie}-{pot}W"
                paineis.append(Painel(
                    fabricante=marca,
                    modelo=modelo,
                    potencia_w=pot
                ))
    Painel.objects.bulk_create(paineis)

class Migration(migrations.Migration):
    dependencies = [
        ('equipamentos', '0007_popular_paineis'),
    ]

    operations = [
        migrations.RunPython(popular_equipamentos, migrations.RunPython.noop),
    ]
