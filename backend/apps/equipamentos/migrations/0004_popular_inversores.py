# Generated migration to populate default inverters

from django.db import migrations

def popular_inversores(apps, schema_editor):
    Inversor = apps.get_model('equipamentos', 'Inversor')
    
    marcas_config = {
        'ABB': {
            'series': ['UNO-DM-1.2', 'UNO-DM-2.0', 'UNO-DM-3.0', 'UNO-DM-3.3', 'UNO-DM-4.0', 'UNO-DM-4.6', 'UNO-DM-5.0', 'UNO-DM-6.0',
                       'TRIO-5.8', 'TRIO-7.5', 'TRIO-8.5', 'TRIO-20.0', 'TRIO-27.6', 'TRIO-50.0',
                       'PVS-10', 'PVS-50', 'PVS-100', 'PVS-120',
                       'REACT2-3.6', 'REACT2-5.0', 'REACT2-6.0',
                       'PVI-3.0', 'PVI-3.6', 'PVI-4.2', 'PVI-5.0', 'PVI-6.0', 'PVI-10.0', 'PVI-12.5'],
            'potencias': [
                # Monofásicos
                (1200, 'UNO-DM-1.2-TL-PLUS'), (2000, 'UNO-DM-2.0-TL-PLUS'), (3000, 'UNO-DM-3.0-TL-PLUS'),
                (3300, 'UNO-DM-3.3-TL-PLUS'), (4000, 'UNO-DM-4.0-TL-PLUS'), (4600, 'UNO-DM-4.6-TL-PLUS'),
                (5000, 'UNO-DM-5.0-TL-PLUS'), (6000, 'UNO-DM-6.0-TL-PLUS'),
                # Bifásicos
                (3600, 'REACT2-3.6-TL'), (5000, 'REACT2-5.0-TL'), (6000, 'REACT2-6.0-TL'),
                # Trifásicos pequeno porte
                (5800, 'TRIO-5.8-TL-OUTD'), (7500, 'TRIO-7.5-TL-OUTD'), (8500, 'TRIO-8.5-TL-OUTD'),
                (10000, 'TRIO-10.0-TL-OUTD'), (12500, 'TRIO-12.5-TL-OUTD'), (15000, 'TRIO-15.0-TL-OUTD'),
                (20000, 'TRIO-20.0-TL-OUTD'), (27600, 'TRIO-27.6-TL-OUTD'), (30000, 'TRIO-30.0-TL-OUTD'),
                # Trifásicos médio porte
                (10000, 'PVI-10.0-TL-OUTD'), (12500, 'PVI-12.5-TL-OUTD'), (15000, 'PVI-15.0-TL-OUTD'),
                (20000, 'PVI-20.0-TL-OUTD'), (25000, 'PVI-25.0-TL-OUTD'), (30000, 'PVI-30.0-TL-OUTD'),
                (33000, 'PVI-33.0-TL-OUTD'), (36000, 'PVI-36.0-TL-OUTD'),
                # Trifásicos grande porte
                (50000, 'PVS-50-TL'), (60000, 'PVS-60-TL'), (75000, 'PVS-75-TL'),
                (100000, 'PVS-100-TL'), (120000, 'PVS-120-TL'),
                # Série TRIO adicional
                (8000, 'TRIO-8.0-TL-OUTD'), (17000, 'TRIO-17.0-TL-OUTD'), (25000, 'TRIO-25.0-TL-OUTD'),
                # Série PVI adicional  
                (3000, 'PVI-3.0-TL-OUTD'), (3600, 'PVI-3.6-TL-OUTD'), (4200, 'PVI-4.2-TL-OUTD'),
                (5000, 'PVI-5.0-TL-OUTD'), (6000, 'PVI-6.0-TL-OUTD'),
                # Série UNO adicional
                (2500, 'UNO-DM-2.5-TL-PLUS'), (3500, 'UNO-DM-3.5-TL-PLUS'), (4500, 'UNO-DM-4.5-TL-PLUS'),
                (5500, 'UNO-DM-5.5-TL-PLUS'),
                # Série REACT adicional
                (4000, 'REACT2-4.0-TL'), (4600, 'REACT2-4.6-TL'),
                # Trifásicos adicionais
                (40000, 'PVS-40-TL'), (80000, 'PVS-80-TL'), (110000, 'PVS-110-TL'),
                (12000, 'TRIO-12.0-TL-OUTD'), (22000, 'TRIO-22.0-TL-OUTD'),
                (40000, 'PVI-40.0-TL-OUTD'), (50000, 'PVI-50.0-TL-OUTD'),
                # Modelos adicionais para completar 60
                (1500, 'UNO-DM-1.5-TL-PLUS'), (2200, 'UNO-DM-2.2-TL-PLUS'),
                (3800, 'UNO-DM-3.8-TL-PLUS'), (5200, 'UNO-DM-5.2-TL-PLUS'),
                (18000, 'TRIO-18.0-TL-OUTD'), (35000, 'PVI-35.0-TL-OUTD'),
            ]
        },
        'Auxsol': {
            'series': ['ASW'],
            'potencias_mono': [3000, 4000, 5000, 6000],
            'potencias_tri': [10000, 12000, 15000, 20000, 25000, 30000, 50000, 75000]
        },
        'Chint': {
            'series': ['CPS SCA'],
            'potencias_mono': [3000, 4000, 5000, 6000],
            'potencias_tri': [10000, 12000, 15000, 20000, 25000, 30000, 50000, 80000, 100000]
        },
        'Deye': {
            'series': ['SUN'],
            'potencias_mono': [3000, 4000, 5000, 6000],
            'potencias_tri': [10000, 12000, 15000, 20000, 25000, 30000, 50000, 80000, 100000]
        },
        'Growatt': {
            'series': ['MIN', 'MOD', 'MAX'],
            'potencias_mono': [3000, 4000, 5000, 6000],
            'potencias_tri': [10000, 12000, 15000, 20000, 25000, 30000, 50000, 80000, 100000, 125000]
        },
        'Solis': {
            'series': ['S6-GR1P', 'S6-GR3P'],
            'potencias_mono': [3000, 4000, 5000, 6000],
            'potencias_tri': [10000, 12000, 15000, 20000, 25000, 30000, 50000, 80000, 100000, 125000]
        },
        'Sungrow': {
            'series': ['SG'],
            'potencias_mono': [3000, 4000, 5000, 6000],
            'potencias_tri': [10000, 12000, 15000, 20000, 25000, 30000, 50000, 80000, 100000, 125000]
        },
    }
    
    inversores = []
    for marca, config in marcas_config.items():
        if marca == 'ABB':
            # ABB usa lista customizada de potencias com modelos específicos
            for potencia, modelo in config['potencias']:
                inversores.append(
                    Inversor(
                        fabricante=marca,
                        modelo=modelo,
                        potencia_w=potencia,
                        potencia_maxima_w=int(potencia * 1.15)
                    )
                )
        else:
            # Outras marcas usam o padrão antigo
            for serie in config['series']:
                for potencia in config['potencias_mono']:
                    pot_kw = potencia / 1000
                    modelo = f"{serie}-{pot_kw:.1f}K" if pot_kw < 10 else f"{serie}-{int(pot_kw)}K"
                    inversores.append(
                        Inversor(
                            fabricante=marca,
                            modelo=modelo,
                            potencia_w=potencia,
                            potencia_maxima_w=int(potencia * 1.15)
                        )
                    )
            
            for serie in config['series']:
                for potencia in config['potencias_tri']:
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
    
    Inversor.objects.bulk_create(inversores, ignore_conflicts=True)

def remover_inversores(apps, schema_editor):
    Inversor = apps.get_model('equipamentos', 'Inversor')
    Inversor.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0003_alter_inversor_preco_unitario_and_more'),
    ]

    operations = [
        migrations.RunPython(popular_inversores, remover_inversores),
    ]
