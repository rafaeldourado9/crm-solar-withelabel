"""
Execute este script para criar as migrações necessárias:

docker-compose exec backend python manage.py makemigrations premissas
docker-compose exec backend python manage.py makemigrations equipamentos
docker-compose exec backend python manage.py migrate

Depois, crie dados iniciais:

docker-compose exec backend python manage.py shell

from apps.premissas.models import Premissa
from apps.equipamentos.models_solar import Painel, Inversor

# Criar premissa padrão
Premissa.objects.create(
    hsp_padrao=4.85,
    tarifa_energia_atual=1.05,
    inflacao_energetica_anual=10.0,
    perda_eficiencia_anual=0.8,
    taxas_maquininha={'12': 12.5, '18': 18.3, '24': 25.0}
)

# Criar painéis exemplo
Painel.objects.create(
    modelo='Canadian 550W',
    fabricante='Canadian Solar',
    potencia_w=550,
    preco_unitario=850.00
)

# Criar inversores exemplo
Inversor.objects.create(
    modelo='Growatt 5kW',
    fabricante='Growatt',
    potencia_w=5000,
    potencia_maxima_w=6500,
    preco_unitario=3500.00
)
"""
