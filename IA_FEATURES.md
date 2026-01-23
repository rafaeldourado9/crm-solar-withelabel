# 🤖 Features de IA - CRM Solar

## Funcionalidades Implementadas

### 1. Análise Inteligente de Consumo
**Endpoint**: `POST /api/ia/analisar-consumo/`

Analisa histórico de consumo e identifica padrões, sazonalidade e recomenda dimensionamento ideal.

```json
{
  "historico_consumo": [1200, 1350, 1100, 1400, 1250]
}
```

**Resposta**:
```json
{
  "consumo_medio": 1260,
  "pico_consumo": 1400,
  "sazonalidade": "moderada",
  "recomendacao_kwp": 10.5
}
```

### 2. Otimização de Proposta
**Endpoint**: `POST /api/ia/otimizar-proposta/{orcamento_id}/`

Sugere otimizações de custo mantendo qualidade baseado em histórico de vendas.

**Resposta**:
```json
{
  "economia_possivel": 1200.00,
  "sugestoes": [
    "Trocar inversor por modelo equivalente mais econômico",
    "Negociar desconto em lote de painéis"
  ],
  "valor_otimizado": 21600.00
}
```

### 3. Chatbot de Atendimento
**Endpoint**: `POST /api/ia/chatbot/`

Assistente virtual para atendimento ao cliente com contexto.

```json
{
  "mensagem": "Quanto tempo demora a instalação?",
  "cliente_id": 123
}
```

**Resposta**:
```json
{
  "resposta": "Olá! Para o seu sistema de 10kWp, a instalação leva em média 45 dias úteis..."
}
```

### 4. Análise de Viabilidade
**Endpoint**: `POST /api/ia/analisar-viabilidade/`

Analisa viabilidade técnica e financeira do projeto.

```json
{
  "consumo_kwh": 1500,
  "area_disponivel_m2": 80,
  "orcamento_cliente": 25000,
  "tipo_telhado": "ceramico"
}
```

**Resposta**:
```json
{
  "viavel": true,
  "score": 85,
  "motivos": ["Área suficiente", "Orçamento adequado"],
  "recomendacoes": ["Considerar estrutura reforçada"]
}
```

### 5. Email de Follow-up Automático
**Endpoint**: `POST /api/ia/email-followup/{cliente_id}/`

Gera emails personalizados de follow-up.

```json
{
  "dias_sem_resposta": 7
}
```

**Resposta**:
```json
{
  "email": "Olá João,\n\nEspero que esteja bem! Faz 7 dias que enviamos..."
}
```

### 6. Extração de Dados da Conta de Luz (OCR)
**Endpoint**: `POST /api/ia/extrair-conta-luz/`

Extrai dados automaticamente da foto da conta de luz.

```json
{
  "imagem_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Resposta**:
```json
{
  "consumo_kwh": 1764,
  "valor_total": 1987.04,
  "concessionaria": "Energisa"
}
```

### 7. Previsão de Economia
**Endpoint**: `POST /api/ia/prever-economia/`

Prevê economia ao longo dos anos considerando inflação energética.

```json
{
  "consumo": 1500,
  "tarifa": 0.95,
  "anos": 25
}
```

**Resposta**:
```json
{
  "previsao_anual": [
    {"ano": 1, "economia": 18540.00},
    {"ano": 2, "economia": 20023.20},
    ...
  ],
  "economia_total_25_anos": 687450.00
}
```

## 🔑 Configuração

### 1. Obter API Keys

**OpenAI**:
- Acesse: https://platform.openai.com/api-keys
- Crie uma nova chave
- Adicione ao `.env`: `OPENAI_API_KEY=sk-...`

**Anthropic (Claude)**:
- Acesse: https://console.anthropic.com/
- Crie uma nova chave
- Adicione ao `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

### 2. Instalar Dependências

```bash
pip install openai anthropic
```

### 3. Testar

```bash
# Teste rápido
curl -X POST http://localhost:8000/api/ia/chatbot/ \
  -H "Content-Type: application/json" \
  -d '{"mensagem": "Olá, quanto custa um sistema de 10kWp?"}'
```

## 💡 Casos de Uso

### Fluxo Completo com IA

1. **Cliente envia foto da conta de luz**
   - Sistema extrai dados automaticamente (OCR)
   - Cria orçamento preliminar

2. **IA analisa viabilidade**
   - Verifica se projeto é viável
   - Sugere melhor configuração

3. **Sistema otimiza proposta**
   - IA sugere economia de custos
   - Mantém qualidade

4. **Chatbot tira dúvidas**
   - Cliente conversa com IA
   - Respostas contextualizadas

5. **Follow-up automático**
   - IA gera emails personalizados
   - Aumenta taxa de conversão

## 🎯 Benefícios

- ⚡ **Agilidade**: Reduz tempo de criação de orçamento em 70%
- 🎯 **Precisão**: Dimensionamento mais preciso
- 💰 **Economia**: Otimização de custos automática
- 📈 **Conversão**: Follow-ups personalizados aumentam vendas
- 🤖 **Automação**: Menos trabalho manual

## 🚀 Roadmap Futuro

- [ ] Análise de imagens de telhado (drone/satélite)
- [ ] Previsão de geração solar por localização
- [ ] Recomendação de equipamentos por ML
- [ ] Chatbot com voz (WhatsApp/Telegram)
- [ ] Dashboard preditivo de vendas
- [ ] Análise de sentimento em conversas
- [ ] Geração automática de propostas completas

## ⚠️ Custos Estimados

**OpenAI GPT-4o-mini**:
- ~$0.15 por 1M tokens de entrada
- ~$0.60 por 1M tokens de saída
- Custo médio por orçamento: ~$0.01

**Anthropic Claude**:
- ~$3.00 por 1M tokens de entrada
- ~$15.00 por 1M tokens de saída
- Custo médio por análise: ~$0.05

**Estimativa mensal** (100 orçamentos): ~$6.00

## 🔒 Segurança

- Nunca envie dados sensíveis (CPF, senhas) para APIs
- Use anonimização quando possível
- Configure rate limiting
- Monitore uso de tokens
- Implemente cache para respostas comuns
