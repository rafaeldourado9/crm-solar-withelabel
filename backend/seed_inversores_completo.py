import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.equipamentos.models import Inversor

marcas_config = {
    'ABB': {
        'series': ['UNO-DM', 'TRIO', 'PVS', 'REACT2', 'PVI'],
        'potencias_mono': [1200, 2000, 3000, 3300, 4000, 4600, 5000, 6000],
        'potencias_tri': [5800, 7500, 8500, 10000, 12500, 15000, 20000, 25000, 27600, 30000, 40000, 50000, 60000, 75000, 100000, 120000]
    },
    'APsystems': {
        'series': ['QS1', 'YC', 'DS3'],
        'potencias_mono': [1200, 1600, 2000],
        'potencias_tri': [1200, 1600, 2000]
    },
    'Auxsol': {
        'series': ['ASW', 'ASW-H'],
        'potencias_mono': [2000, 3000, 3600, 4000, 5000, 6000],
        'potencias_tri': [8000, 10000, 12000, 15000, 17000, 20000, 25000, 30000, 40000, 50000, 60000, 75000, 80000]
    },
    'Chint': {
        'series': ['CPS SCA', 'CPS SCH'],
        'potencias_mono': [2000, 3000, 3600, 4000, 5000, 6000],
        'potencias_tri': [8000, 10000, 12000, 15000, 17000, 20000, 25000, 30000, 33000, 40000, 50000, 60000, 70000, 80000, 100000, 110000]
    },
    'Delta': {
        'series': ['RPI', 'M', 'H'],
        'potencias_mono': [3000, 4600, 5000, 6000],
        'potencias_tri': [5000, 6000, 8000, 10000, 12000, 15000, 20000, 25000, 30000, 50000]
    },
    'Deye': {
        'series': ['SUN', 'SUN-SG01HP3', 'SUN-SG04LP3', 'SUN-G05'],
        'potencias_mono': [2000, 2500, 3000, 3600, 4000, 4600, 5000, 6000],
        'potencias_tri': [8000, 10000, 12000, 15000, 17000, 20000, 25000, 30000, 33000, 36000, 40000, 50000, 60000, 70000, 80000, 100000, 110000]
    },
    'Enphase': {
        'series': ['IQ7', 'IQ7+', 'IQ7A', 'IQ8', 'IQ8+', 'IQ8M', 'IQ8A', 'IQ8H'],
        'potencias_mono': [240, 290, 295, 300, 330, 349, 366, 384],
        'potencias_tri': []
    },
    'Fimer': {
        'series': ['PVS', 'UNO-DM-PLUS'],
        'potencias_mono': [3000, 3300, 4000, 4600, 5000, 6000],
        'potencias_tri': [10000, 12500, 15000, 20000, 27600, 33000, 50000, 60000]
    },
    'Fronius': {
        'series': ['Primo', 'Symo', 'Eco'],
        'potencias_mono': [3000, 3700, 4000, 4600, 5000, 6000, 8200],
        'potencias_tri': [3000, 4000, 5000, 6000, 7000, 8000, 10000, 12500, 15000, 17500, 20000, 22000, 24000, 25000, 27000]
    },
    'Goodwe': {
        'series': ['GW', 'DNS', 'SDT', 'SMT', 'MT'],
        'potencias_mono': [2000, 2500, 3000, 3600, 4000, 4600, 5000, 6000],
        'potencias_tri': [8000, 10000, 12000, 15000, 17000, 20000, 25000, 29900, 30000, 36000, 40000, 50000, 60000, 70000, 80000]
    },
    'Growatt': {
        'series': ['MIN', 'MIC', 'MOD', 'MAX', 'SPH'],
        'potencias_mono': [2500, 3000, 3300, 3600, 4200, 5000, 6000],
        'potencias_tri': [3000, 4000, 5000, 6000, 8000, 10000, 12000, 15000, 17000, 20000, 25000, 30000, 33000, 40000, 50000, 60000, 70000, 80000, 100000, 110000, 125000]
    },
    'Hoymiles': {
        'series': ['MI', 'HMS', 'HM'],
        'potencias_mono': [600, 800, 1000, 1200, 1500, 2000],
        'potencias_tri': [1500, 1800, 2000, 2250]
    },
    'Huawei': {
        'series': ['SUN2000'],
        'potencias_mono': [2000, 3000, 3680, 4000, 5000, 6000],
        'potencias_tri': [8000, 10000, 12000, 15000, 17000, 20000, 23000, 25000, 30000, 33000, 36000, 40000, 45000, 50000, 60000, 65000, 70000, 100000]
    },
    'Ingeteam': {
        'series': ['INGECON SUN'],
        'potencias_mono': [3000, 5000, 6000],
        'potencias_tri': [10000, 12000, 17000, 20000, 25000, 30000, 40000, 50000, 60000, 75000, 100000]
    },
    'KSTAR': {
        'series': ['KSG', 'KSG-M'],
        'potencias_mono': [3000, 3600, 4000, 5000, 6000],
        'potencias_tri': [5000, 6000, 8000, 10000, 12000, 15000, 20000, 25000, 30000, 40000, 50000]
    },
    'Refusol': {
        'series': ['008K', '010K', '015K', '020K', '023K'],
        'potencias_mono': [],
        'potencias_tri': [8000, 10000, 15000, 20000, 23000, 25000, 30000, 40000, 50000]
    },
    'SMA': {
        'series': ['Sunny Boy', 'Sunny Tripower', 'Sunny Central'],
        'potencias_mono': [3000, 3600, 4000, 5000, 6000],
        'potencias_tri': [5000, 6000, 8000, 10000, 12000, 15000, 17000, 20000, 25000, 30000, 40000, 50000, 60000, 100000, 110000]
    },
    'Sofar': {
        'series': ['SOFAR'],
        'potencias_mono': [2200, 3000, 3300, 3600, 4400, 5000, 5500, 6000],
        'potencias_tri': [8800, 10000, 11000, 12000, 15000, 17000, 20000, 25000, 30000, 33000, 36000, 40000, 50000, 60000]
    },
    'Solis': {
        'series': ['S5-GR1P', 'S6-GR1P', 'S6-GR3P', 'RHI-ES', 'S6-EH1P'],
        'potencias_mono': [3000, 3600, 4000, 4600, 5000, 6000],
        'potencias_tri': [5000, 6000, 8000, 10000, 12000, 15000, 17000, 20000, 25000, 30000, 40000, 50000, 60000, 75000, 80000, 100000, 110000, 125000]
    },
    'Sungrow': {
        'series': ['SG', 'SH'],
        'potencias_mono': [3000, 3600, 4000, 5000, 6000],
        'potencias_tri': [5000, 6000, 8000, 10000, 12000, 15000, 17000, 20000, 25000, 30000, 33000, 36000, 40000, 50000, 60000, 75000, 80000, 100000, 110000, 125000]
    },
    'WEG': {
        'series': ['SIW', 'SIW700'],
        'potencias_mono': [2000, 3000, 4000, 5000, 6000],
        'potencias_tri': [10000, 12000, 15000, 17000, 20000, 25000, 30000, 33000, 36000, 40000, 50000, 60000, 75000]
    }
}

inversores = []

for marca, config in marcas_config.items():
    for serie in config['series']:
        for potencia in config['potencias_mono']:
            pot_kw = potencia / 1000
            if pot_kw < 1:
                modelo = f"{serie}-{int(potencia)}"
            else:
                modelo = f"{serie}-{pot_kw:.1f}K" if pot_kw < 10 else f"{serie}-{int(pot_kw)}K"
            
            inversores.append({
                'fabricante': marca,
                'modelo': modelo,
                'potencia_w': potencia,
                'potencia_maxima_w': int(potencia * 1.15)
            })
    
    for serie in config['series']:
        for potencia in config['potencias_tri']:
            pot_kw = potencia / 1000
            modelo = f"{serie}-{pot_kw:.1f}K-T" if pot_kw < 10 else f"{serie}-{int(pot_kw)}K-T"
            
            inversores.append({
                'fabricante': marca,
                'modelo': modelo,
                'potencia_w': potencia,
                'potencia_maxima_w': int(potencia * 1.15)
            })

print(f"Gerando {len(inversores)} inversores...")

for inv in inversores:
    Inversor.objects.get_or_create(
        fabricante=inv['fabricante'],
        modelo=inv['modelo'],
        defaults={
            'potencia_w': inv['potencia_w'],
            'potencia_maxima_w': inv['potencia_maxima_w']
        }
    )

print(f"✅ {len(inversores)} inversores cadastrados com sucesso!")
print(f"Marcas: {len(marcas_config)}")
