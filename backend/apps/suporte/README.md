# 🤖 Módulo Suporte IA - CRM Solar

Assistente inteligente integrado com Google Gemini para suporte aos vendedores.

## ✨ Funcionalidades

### 🎯 Inteligência Artificial
- **Google Gemini Pro** - IA conversacional avançada
- **Contexto Automático** - Acessa dados do vendedor em tempo real
- **Respostas Personalizadas** - Baseadas no desempenho e situação atual

### 💼 Recursos de Vendas
- ✅ Alertas de propostas vencendo (próximos 7 dias)
- 📞 Identificação de clientes sem retorno (15+ dias)
- 📊 Relatórios de desempenho em tempo real
- 💰 Estatísticas de conversão e valores

### 🔧 Suporte Técnico
- ⚡ Dúvidas sobre HSP, perdas e dimensionamento
- 📐 Fórmulas de cálculo solar
- 🛠️ Orientações de engenharia

### 😄 Entretenimento
- 🌞 Piadas sobre energia solar
- 💬 Conversação natural e amigável
- 🎨 Interface moderna e intuitiva

## 🚀 Como Usar

### Backend

1. **Configurar API Key do Gemini** (`.env`):
```env
GEMINI_API_KEY=sua-chave-aqui
```

2. **Executar Migrations**:
```bash
docker-compose exec backend python manage.py migrate suporte
```

3. **Endpoints Disponíveis**:
- `POST /api/suporte/conversas/chat/` - Enviar mensagem
- `GET /api/suporte/conversas/historico/` - Ver histórico
- `DELETE /api/suporte/conversas/limpar_historico/` - Limpar chat
- `GET /api/suporte/agentes/meu_agente/` - Dados do agente
- `POST /api/suporte/agentes/renomear/` - Renomear agente

### Frontend

1. **Acessar**: `/suporte` no menu lateral
2. **Personalizar**: Clique no ícone de edição para renomear seu agente
3. **Conversar**: Digite mensagens naturalmente

## 💡 Exemplos de Uso

### Perguntas Comuns
```
"Olá! Como você está?"
"Mostre propostas vencendo"
"Quais clientes precisam de follow-up?"
"Gerar relatório de vendas"
"Como calcular HSP?"
"Conte uma piada solar"
```

### Respostas Inteligentes
O agente detecta automaticamente a intenção e:
- 📊 Busca dados reais do banco
- 🎯 Fornece informações específicas
- 💡 Sugere ações práticas
- ⚠️ Alerta sobre urgências

## 🛡️ Segurança

- ✅ Apenas responde sobre energia solar
- ❌ Recusa assuntos pessoais, políticos ou sensíveis
- 🔒 Dados isolados por vendedor
- 🔐 Autenticação obrigatória

## 🎨 Interface

- **Design Solar**: Gradiente amarelo/laranja
- **Chat Moderno**: Bolhas de mensagem estilizadas
- **Responsivo**: Funciona em desktop e mobile
- **Animações**: Loading suave e transições

## 📊 Contexto Automático

O agente sempre tem acesso a:
- Total de orçamentos do mês
- Valor total em vendas
- Taxa de conversão
- Propostas vencendo
- Clientes sem retorno
- Configurações HSP e perdas

## 🔄 Fallback

Se a API do Gemini falhar, o sistema usa respostas pré-programadas baseadas em:
- Análise de palavras-chave
- Consultas diretas ao banco
- Mensagens estruturadas

## 🚧 Próximas Melhorias

- [ ] Integração com WhatsApp
- [ ] Notificações push
- [ ] Análise de sentimento
- [ ] Sugestões proativas
- [ ] Treinamento personalizado
- [ ] Exportar conversas

## 📝 Notas Técnicas

- **Modelo**: Gemini Pro (Google)
- **Banco**: PostgreSQL (tabelas: agentes_ia, conversas_ia)
- **Cache**: Não implementado (futuro)
- **Rate Limit**: Controlado pela API do Gemini

---

**Desenvolvido com ☀️ para o CRM Solar**
