# Sprint 3 - Calculadora Solar Inteligente

**Período:** Semana 3  
**Status:** ✅ Concluído

## Objetivos
Implementar sistema de dimensionamento automático com cálculos de engenharia e financeiros.

## User Stories

### US-007: Configurar Premissas Globais
**Como** gestor  
**Quero** configurar parâmetros do sistema  
**Para** padronizar cálculos

**Critérios de Aceitação:**
- [x] Model Premissa com campos: HSP, perda, prazos, taxas
- [x] Método get_ativa() para buscar premissa ativa
- [x] Endpoint /api/premissas/ativa/
- [x] Taxa de juros em JSON para múltiplas parcelas

**Implementação:**
- `apps/premissas/models.py` - Modelo atualizado
- `apps/premissas/views.py` - Endpoint ativa

### US-008: Calcular Dimensionamento Automático
**Como** vendedor  
**Quero** calcular automaticamente o sistema  
**Para** agilizar orçamentos

**Critérios de Aceitação:**
- [x] Fórmula: Potência = (Consumo/30) / (HSP × (1-perda))
- [x] Cálculo de quantidade de painéis
- [x] Seleção automática de inversor compatível
- [x] Geração estimada mensal
- [x] Possibilidade de override manual (HSP, perda)

**Implementação:**
- `apps/orcamentos/services.py` - SolarCalculator
- Método calcular_dimensionamento()

### US-009: Calcular Valores Financeiros
**Como** vendedor  
**Quero** calcular preços automaticamente  
**Para** gerar orçamentos precisos

**Critérios de Aceitação:**
- [x] Custo: painéis + inversor + montagem + projeto
- [x] Aplicar margem de lucro configurável
- [x] Calcular impostos e comissões
- [x] Simular parcelamento com juros

**Implementação:**
- Método calcular_financeiro()
- Método calcular_parcelamento()
- Método calcular_completo()

### US-010: Interface de Calculadora
**Como** vendedor  
**Quero** interface intuitiva para cálculos  
**Para** criar orçamentos rapidamente

**Critérios de Aceitação:**
- [x] Botão "Calcular" que chama API
- [x] Campos preenchidos automaticamente
- [x] Ajuste manual de quantidade com recálculo
- [x] Seleção de parcelas atualiza valores
- [x] Loading state durante cálculo

**Implementação:**
- `pages/Orcamentos.jsx` - Calculadora completa
- Endpoint POST /api/orcamentos/calcular/

## Fórmulas Implementadas

### Dimensionamento
```
Consumo Diário = Consumo Mensal / 30
Potência Necessária (kW) = Consumo Diário / (HSP × (1 - Perda))
Potência Necessária (Wp) = Potência (kW) × 1000
Quantidade Painéis = ⌈Potência Wp / Potência Painel⌉
Potência Total (kWp) = (Qtd Painéis × Potência Painel) / 1000
Potência Inversor Mín = Potência Total × Overload (0.75)
Geração Estimada = Potência Total × HSP × 30 × (1 - Perda)
```

### Financeiro
```
Custo Painéis = Qtd × Preço Unitário
Custo Montagem = Qtd Painéis × Valor por Painel
Custo Total = Painéis + Inversor + Montagem + Projeto
Valor Venda = Custo Total × (1 + Margem/100)
Impostos = Valor Venda × (Imposto%/100)
Comissão = Valor Venda × (Comissão%/100)
Valor Final = Valor Venda + Impostos + Comissão
```

### Parcelamento
```
Valor com Juros = Valor Final × (1 + Taxa/100)
Valor Parcela = Valor com Juros / Número Parcelas
```

## Tarefas Técnicas

### Backend
- [x] Atualizar modelo Premissa
- [x] Criar SolarCalculator service
- [x] Implementar CalcularDimensionamentoView
- [x] Atualizar urls de orcamentos
- [x] Buscar equipamentos por tipo

### Frontend
- [x] Carregar premissas ativas
- [x] Carregar lista de painéis
- [x] Implementar calcularDimensionamento()
- [x] Implementar recalcularComAjuste()
- [x] Interface com 3 seções (Cliente, Dimensionamento, Pagamento)

## Métricas
- **Commits:** 10
- **Arquivos Alterados:** 8
- **Linhas de Código:** ~1200

## Retrospectiva

### O que funcionou bem ✅
- Cálculos precisos e validados
- Interface intuitiva e responsiva
- Separação clara de responsabilidades (service layer)
- Ajuste manual mantém consistência

### Melhorias para próxima sprint 🔄
- Adicionar histórico de cálculos
- Implementar comparação de cenários
- Adicionar gráficos de geração
- Integrar API de clima para HSP por cidade
