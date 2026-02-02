# Sistema de Cálculo de Deslocamento

## Como Funciona

O sistema calcula o custo de deslocamento com fallback automático:

### 1. Verificação de Cidades Isentas
Primeiro verifica se a cidade está na lista de "Cidades sem cobrança" configurada nas Premissas.

### 2. Cálculo de Distância (Prioridade)
1. **Google Maps API** (se configurada no .env)
2. **Tabela de distâncias** (fallback automático)

### 3. Cálculo do Custo
```
Distância Total = Distância × 2 (ida e volta)
Litros = Distância Total / Consumo (km/L)
Custo Combustível = Litros × Preço/Litro
Valor Cobrado = Custo × (1 + Margem%/100)
Margem Lucro = Valor Cobrado - Custo
```

## Configurar Google Maps API

### 1. Obter Chave da API
1. Acesse: https://console.cloud.google.com/
2. Crie um projeto ou selecione um existente
3. Vá em: **APIs & Services > Credentials**
4. Clique em: **Create Credentials > API Key**
5. Habilite a API: **Distance Matrix API**

### 2. Adicionar no Backend
Edite o arquivo `backend/.env`:
```bash
GOOGLE_MAPS_API_KEY=AIzaSyC...
```

### 3. Reiniciar o Backend
```bash
docker-compose restart backend
```

## Tabela de Distâncias (Fallback)

Usada quando Google Maps não está disponível:

| Cidade | Distância (km) |
|--------|----------------|
| Campo Grande | 120 |
| Dourados | 0 |
| Ponta Porã | 30 |
| Itaporã | 20 |
| Caarapó | 40 |
| Maracaju | 60 |
| Naviraí | 70 |
| Fátima do Sul | 50 |
| Rio Brilhante | 70 |
| Nova Andradina | 100 |

## Adicionar Novas Cidades na Tabela

Edite: `backend/apps/orcamentos/services/deslocamento_service.py`

```python
DISTANCIAS_CONHECIDAS = {
    'campo grande': 120,
    'sua_cidade': 150,  # Adicione aqui
    # ...
}
```

## Configurar Margem de Deslocamento

Acesse: **Premissas > Deslocamento > Margem Deslocamento (%)**

Padrão: 20% sobre o custo do combustível

## Configurar Cidades Sem Cobrança

Acesse: **Premissas > Deslocamento > Cidades Sem Cobrança**

Exemplo: `Dourados, Itaporã, Fátima do Sul`

## Exemplo de Cálculo

**Cliente em Campo Grande:**
- Distância: 120 km (ida) = 240 km (ida e volta)
- Consumo: 240 km ÷ 8 km/L = 30 litros
- Custo: 30 L × R$ 6,50 = R$ 195,00
- Margem 20%: R$ 195 × 1,20 = R$ 234,00
- Lucro: R$ 39,00

## Vantagens do Sistema

✅ **Com Google Maps:**
- Distâncias precisas para qualquer cidade
- Atualização automática de rotas
- Sem manutenção manual

✅ **Fallback Automático:**
- Funciona mesmo sem API key
- Tabela para cidades principais
- Sem dependência externa
