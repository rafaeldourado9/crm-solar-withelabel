# Módulo de Premissas e Calculadora Solar

## Implementação Completa

### 1. Backend - Migrações

```bash
# Criar migrações
docker-compose exec backend python manage.py makemigrations premissas
docker-compose exec backend python manage.py makemigrations equipamentos
docker-compose exec backend python manage.py migrate
```

### 2. Dados Iniciais

```bash
docker-compose exec backend python manage.py shell
```

```python
from apps.premissas.models import Premissa
from apps.equipamentos.models_solar import Painel, Inversor
from decimal import Decimal

# Premissa padrão
Premissa.objects.create(
    hsp_padrao=Decimal('4.85'),
    tarifa_energia_atual=Decimal('1.05'),
    inflacao_energetica_anual=Decimal('10.0'),
    perda_eficiencia_anual=Decimal('0.8'),
    perda_padrao=Decimal('0.20'),
    prazo_entrega_padrao=45,
    garantia_instalacao_meses=12,
    taxas_maquininha={'12': '12.5', '18': '18.3', '24': '25.0'},
    margem_lucro_percentual=Decimal('30.0'),
    overload_inversor=Decimal('0.75'),
    ativo=True
)

# Painéis
Painel.objects.create(
    modelo='Canadian 550W',
    fabricante='Canadian Solar',
    potencia_w=550,
    area_m2=Decimal('2.5'),
    eficiencia=Decimal('0.21'),
    preco_unitario=Decimal('850.00')
)

Painel.objects.create(
    modelo='Jinko 450W',
    fabricante='Jinko Solar',
    potencia_w=450,
    area_m2=Decimal('2.1'),
    eficiencia=Decimal('0.20'),
    preco_unitario=Decimal('720.00')
)

# Inversores
Inversor.objects.create(
    modelo='Growatt 5kW',
    fabricante='Growatt',
    potencia_w=5000,
    potencia_maxima_w=6500,
    preco_unitario=Decimal('3500.00')
)

Inversor.objects.create(
    modelo='Growatt 10kW',
    fabricante='Growatt',
    potencia_w=10000,
    potencia_maxima_w=13000,
    preco_unitario=Decimal('5800.00')
)
```

### 3. Arquitetura

#### Backend
- **apps/premissas/models.py**: Model Premissa (Singleton)
- **apps/equipamentos/models_solar.py**: Models Painel e Inversor
- **apps/orcamentos/services.py**: SolarCalculator (lógica de cálculo)
- **apps/orcamentos/views.py**: CalcularDimensionamentoView (endpoint de preview)

#### Frontend
- **pages/PremissasConfig.jsx**: Configuração de premissas globais
- **pages/Orcamentos.jsx**: Calculadora interativa (já existe, precisa atualizar)

### 4. Fluxo da Calculadora

1. **Usuário informa**: Consumo (kWh) + Seleciona Painel
2. **Sistema calcula**: Qtd Painéis, Inversor, Geração, Área
3. **Usuário ajusta**: Pode alterar qtd de painéis manualmente
4. **Usuário informa**: Valor do Kit (R$)
5. **Usuário seleciona**: Forma de Pagamento (À vista, 12x, 18x, 24x)
6. **Sistema calcula**: Valor Final com taxa aplicada
7. **Sistema mostra**: Economia projetada 25 anos

### 5. Endpoints API

```
GET  /api/premissas/ativa/          # Buscar premissa ativa
PUT  /api/premissas/{id}/           # Atualizar premissa
GET  /api/equipamentos/paineis/     # Listar painéis
GET  /api/equipamentos/inversores/  # Listar inversores
POST /api/orcamentos/calcular/      # Calcular (preview)
POST /api/orcamentos/               # Criar orçamento
```

### 6. Exemplo de Requisição

```javascript
// Calcular dimensionamento
const response = await api.post('/orcamentos/calcular/', {
  consumo_kwh: 500,
  painel_id: 1,
  valor_kit: 25000,
  forma_pagamento: '18'  // ou 'avista'
});

// Resposta
{
  qtd_paineis: 18,
  potencia_sistema_kwp: 9.9,
  geracao_mensal_kwh: 1188,
  area_ocupada_m2: 45,
  inversor: { id: 2, modelo: 'Growatt 10kW', potencia_w: 10000 },
  painel: { id: 1, modelo: 'Canadian 550W', potencia_w: 550 },
  valor_final: 29575.00,
  valor_parcela: 1643.06,
  taxa_aplicada: 18.3,
  parcelas: 18,
  economia_total_25anos: 450000.00,
  economia_mensal_ano1: 1247.40
}
```

### 7. Próximos Passos

1. Execute as migrações
2. Crie os dados iniciais
3. Teste o endpoint `/api/orcamentos/calcular/`
4. Atualize a página Orcamentos.jsx para usar a nova calculadora
5. Adicione a rota para PremissasConfig.jsx no App.jsx
