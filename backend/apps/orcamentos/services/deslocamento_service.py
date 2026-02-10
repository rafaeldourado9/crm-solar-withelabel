import requests
from decimal import Decimal
from django.conf import settings


class DeslocamentoService:
    
    # Tabela de distâncias de Itaporã/Dourados para cidades principais (km) - FALLBACK
    DISTANCIAS_CONHECIDAS = {
        'campo grande': 230,
        'dourados': 20,
        'ponta porã': 50,
        'itaporã': 0,
        'caarapó': 60,
        'maracaju': 80,
        'naviraí': 90,
        'fátima do sul': 70,
        'rio brilhante': 90,
        'nova andradina': 120,
        'bonito': 280,
    }
    
    @staticmethod
    def calcular_distancia_google_maps(origem, destino):
        """Calcula distância entre duas cidades usando Google Maps Distance Matrix API"""
        api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
        
        if not api_key:
            return None
        
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            'origins': origem,
            'destinations': destino,
            'key': api_key,
            'language': 'pt-BR'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data['status'] == 'OK':
                element = data['rows'][0]['elements'][0]
                if element['status'] == 'OK':
                    distancia_km = element['distance']['value'] / 1000
                    return Decimal(str(distancia_km))
            
            return None
        except Exception as e:
            print(f"Erro ao calcular distância via Google Maps: {e}")
            return None
    
    @staticmethod
    def obter_distancia(cidade_cliente, cidade_empresa):
        """Busca distância: primeiro tenta Google Maps, depois tabela"""
        # Tentar Google Maps primeiro
        distancia = DeslocamentoService.calcular_distancia_google_maps(
            cidade_empresa,
            cidade_cliente
        )
        
        if distancia:
            return distancia
        
        # Fallback: tabela de distâncias
        cidade_normalizada = cidade_cliente.split(',')[0].strip().lower()
        for cidade, dist in DeslocamentoService.DISTANCIAS_CONHECIDAS.items():
            if cidade in cidade_normalizada:
                return Decimal(str(dist))
        
        return None
    
    @staticmethod
    def calcular_custo_deslocamento(cidade_cliente, premissas):
        """Calcula o custo de deslocamento até o cliente"""
        cidade_normalizada = cidade_cliente.split(',')[0].strip()
        
        # Verificar se está na lista de cidades sem cobrança
        cidades_sem_cobranca = premissas.cidades_sem_cobranca or []
        for cidade_isenta in cidades_sem_cobranca:
            if cidade_isenta.lower() in cidade_normalizada.lower():
                return {
                    'distancia_km': 0,
                    'distancia_total_km': 0,
                    'custo_combustivel': 0,
                    'margem_lucro': 0,
                    'valor_total': 0,
                    'cobrar': False,
                    'motivo': f'Cidade {cidade_normalizada} isenta de cobrança'
                }
        
        # Buscar distância (Google Maps ou tabela)
        distancia_km = DeslocamentoService.obter_distancia(cidade_cliente, premissas.cidade_empresa)
        
        # Se não encontrar, não cobrar
        if distancia_km is None:
            return {
                'distancia_km': 0,
                'distancia_total_km': 0,
                'custo_combustivel': 0,
                'margem_lucro': 0,
                'valor_total': 0,
                'cobrar': False,
                'motivo': f'Cidade {cidade_normalizada} não encontrada'
            }
        
        # Distância ida e volta
        distancia_total_km = distancia_km * 2
        
        # Calcular consumo: litros = distância / km_por_litro
        litros_necessarios = distancia_total_km / premissas.consumo_veiculo_km_por_litro
        
        # Custo do combustível (ida e volta) - valor repassado ao montador
        custo_combustivel = litros_necessarios * premissas.preco_combustivel_litro
        
        # Valor cobrado do cliente = custo × 1,20 (20% a mais)
        margem_percentual = premissas.margem_deslocamento_percentual or Decimal('20')
        valor_cobrado = custo_combustivel * (1 + margem_percentual / 100)
        
        # Montador recebe: apenas custo do combustível
        # Margem (20%): vira margem de desconto disponível para negociação
        valor_montador = custo_combustivel
        margem_desconto_disponivel = valor_cobrado - custo_combustivel
        
        return {
            'distancia_km': float(distancia_km),
            'distancia_total_km': float(distancia_total_km),
            'litros_necessarios': float(litros_necessarios),
            'custo_combustivel': float(custo_combustivel),
            'valor_montador': float(valor_montador),
            'valor_cobrado': float(valor_cobrado),
            'margem_desconto_disponivel': float(margem_desconto_disponivel),
            'valor_total': float(valor_cobrado),
            'cobrar': True,
            'cidade_origem': premissas.cidade_empresa,
            'cidade_destino': cidade_cliente
        }
