# Generated migration to expand inverters catalog

from django.db import migrations

def expandir_inversores(apps, schema_editor):
    Inversor = apps.get_model('equipamentos', 'Inversor')
    
    # Potências comerciais padrão do mercado
    potencias_mono = [1000, 1200, 1500, 2000, 2500, 3000, 3300, 3600, 4000, 4200, 4600, 5000, 5500, 6000]
    potencias_tri_pequeno = [3000, 5000, 6000, 7000, 8000, 10000, 12000, 15000, 17000, 20000, 25000, 30000, 33000]
    potencias_tri_medio = [36000, 40000, 50000, 60000, 75000, 80000, 100000, 110000, 125000, 150000]
    
    marcas_expandidas = {
        'Auxsol': {
            'series_mono': ['ASW-M', 'ASW-H', 'ASW-S'],
            'series_tri': ['ASW-T', 'ASW-HT', 'ASW-ST'],
        },
        'Chint': {
            'series_mono': ['CPS SCA', 'CPS SCH', 'CPS SCM'],
            'series_tri': ['CPS SCT', 'CPS SCHT', 'CPS SCMT'],
        },
        'Deye': {
            'series_mono': ['SUN-M', 'SUN-SG01HP3', 'SUN-H'],
            'series_tri': ['SUN-T', 'SUN-SG04LP3', 'SUN-HT'],
        },
        'Growatt': {
            'series_mono': ['MIN', 'MIC', 'MOD-M'],
            'series_tri': ['MOD', 'MAX', 'MID'],
        },
        'Solis': {
            'series_mono': ['S5-GR1P', 'S6-GR1P', 'S6-EH1P'],
            'series_tri': ['S6-GR3P', 'RHI-3P', 'S6-EH3P'],
        },
        'Sungrow': {
            'series_mono': ['SG-M', 'SH-M', 'SG-RS'],
            'series_tri': ['SG-T', 'SH-T', 'SG-RT'],
        },
    }
    
    inversores = []
    
    for marca, config in marcas_expandidas.items():
        # Monofásicos
        for serie in config['series_mono']:
            for potencia in potencias_mono:
                pot_kw = potencia / 1000
                modelo = f"{serie}-{pot_kw:.1f}K"
                inversores.append(
                    Inversor(
                        fabricante=marca,
                        modelo=modelo,
                        potencia_w=potencia,
                        potencia_maxima_w=int(potencia * 1.15)
                    )
                )
        
        # Trifásicos pequeno porte
        for serie in config['series_tri']:
            for potencia in potencias_tri_pequeno:
                pot_kw = potencia / 1000
                modelo = f"{serie}-{pot_kw:.1f}K-T" if pot_kw < 10 else f"{serie}-{int(pot_kw)}K-T"
                inversores.append(
                    Inversor(
                        fabricante=marca,
                        modelo=modelo,
                        potencia_w=potencia,
                        potencia_maxima_w=int(potencia * 1.15)
                    )
                )
        
        # Trifásicos médio/grande porte
        for serie in config['series_tri']:
            for potencia in potencias_tri_medio:
                pot_kw = potencia / 1000
                modelo = f"{serie}-{int(pot_kw)}K-T"
                inversores.append(
                    Inversor(
                        fabricante=marca,
                        modelo=modelo,
                        potencia_w=potencia,
                        potencia_maxima_w=int(potencia * 1.15)
                    )
                )
    
    Inversor.objects.bulk_create(inversores, ignore_conflicts=True)

def reverter_expansao(apps, schema_editor):
    pass  # Não remove os dados antigos

class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0004_popular_inversores'),
    ]

    operations = [
        migrations.RunPython(expandir_inversores, reverter_expansao),
    ]
