# API Documentation

## Autenticação

### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "usuario",
  "password": "senha"
}

Response:
{
  "token": "abc123..."
}
```

Todas as requisições autenticadas devem incluir:
```
Authorization: Token abc123...
```

## Endpoints

### Dashboard
```http
GET /api/dashboard/resumo/
```
Retorna KPIs: total_clientes, novos_leads, propostas_ativas, ultimos_clientes

### Clientes
```http
GET    /api/clientes/              # Listar (filtrado por usuário)
POST   /api/clientes/              # Criar
GET    /api/clientes/{id}/         # Detalhar
PUT    /api/clientes/{id}/         # Atualizar
DELETE /api/clientes/{id}/         # Deletar
```

### Premissas
```http
GET /api/premissas/ativa/          # Buscar premissa ativa
```

Response:
```json
{
  "id": 1,
  "hsp_padrao": 4.85,
  "perda_padrao": 0.20,
  "prazo_entrega_dias": 45,
  "garantia_instalacao_meses": 12,
  "taxa_juros_maquininha": {
    "12": 10.5,
    "18": 18.3,
    "24": 25.0
  },
  "margem_lucro_percentual": 30.0,
  "overload_inversor": 0.75
}
```

### Calculadora Solar
```http
POST /api/orcamentos/calcular/
Content-Type: application/json

{
  "consumo_kwh": 500,
  "painel_id": 1,
  "parcelas": 12,
  "hsp": 5.0,              // Opcional (override)
  "perda": 0.15,           // Opcional (override)
  "margem_lucro": 35.0     // Opcional (override)
}
```

Response:
```json
{
  "quantidade_paineis": 12,
  "potencia_total_kwp": 8.4,
  "painel": {
    "id": 1,
    "modelo": "MÓDULO 700W",
    "potencia": 700,
    "preco": 850.00
  },
  "inversor": {
    "id": 2,
    "modelo": "INVERSOR 8000W",
    "potencia": 8000,
    "preco": 4500.00
  },
  "geracao_estimada_kwh": 510.2,
  "hsp_utilizado": 4.85,
  "perda_utilizada": 0.20,
  "custo_total": 15200.00,
  "valor_venda": 19760.00,
  "impostos": 1976.00,
  "comissao": 988.00,
  "valor_final": 22724.00,
  "parcelamento": {
    "parcelas": 12,
    "valor_parcela": 2095.47,
    "valor_total": 25145.64,
    "taxa_juros": 10.5
  },
  "premissas": {
    "prazo_entrega_dias": 45,
    "garantia_instalacao_meses": 12,
    "validade_proposta_dias": 10
  }
}
```

### Orçamentos
```http
GET  /api/orcamentos/              # Listar
POST /api/orcamentos/              # Criar
POST /api/orcamentos/{id}/gerar_pdf/
POST /api/orcamentos/{id}/converter_proposta/
```

### Equipamentos
```http
GET /api/equipamentos/?tipo=painel    # Listar painéis
GET /api/equipamentos/?tipo=inversor  # Listar inversores
```

## Códigos de Status

- `200 OK` - Sucesso
- `201 Created` - Recurso criado
- `400 Bad Request` - Dados inválidos
- `401 Unauthorized` - Não autenticado
- `403 Forbidden` - Sem permissão
- `404 Not Found` - Não encontrado
- `500 Internal Server Error` - Erro no servidor
