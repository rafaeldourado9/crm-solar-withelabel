# Changelog - Correções e Melhorias

## 🔧 Correções Implementadas

### 1. Arredondamento de Valores ✅

**Problema:** Valores dos orçamentos ficavam com números quebrados (ex: R$ 16.422,00)

**Solução:**
- Implementado arredondamento para centena mais próxima em dois momentos:
  1. Após calcular total com margens
  2. Após adicionar margem de desconto
- Valores sempre múltiplos de 100

**Arquivos alterados:**
- `backend/apps/orcamentos/views.py`
- `frontend/src/pages/OrcamentoDetalhe.jsx`

---

### 2. Persistência de Valores nos Cards ✅

**Problema:** Cards mostravam valores duplicados/incorretos após criar orçamento

**Solução:**
- Corrigida ordem de execução no `handleSubmit`
- Adicionado cache-busting com timestamp na URL
- Garantido await no carregamento de dados

**Arquivos alterados:**
- `frontend/src/pages/Orcamentos.jsx`

---

### 3. Cálculo de Overload do Inversor ✅

**Problema:** Overload estava sendo dividido ao invés de multiplicado

**Antes:**
```javascript
capacidade = potencia / overload  // ❌ ERRADO
```

**Depois:**
```javascript
capacidade = potencia × overload  // ✅ CORRETO
```

**Exemplo:**
- Inversor 5kW com overload 1.70
- Antes: 5.000 / 1.70 = 2.941W ❌
- Depois: 5.000 × 1.70 = 8.500W ✅

**Arquivos alterados:**
- `backend/apps/orcamentos/views.py`

---

### 4. Material Elétrico Baseado no Inversor ✅

**Problema:** Material elétrico calculado com base nos painéis

**Solução:**
- Alterado para usar potência do INVERSOR
- Cálculo: `(potencia_inversor × quantidade) / 1000`

**Exemplo:**
- Antes: 11 painéis × 705W = 7,755 kWp → R$ 900
- Depois: 1 inversor × 5.000W = 5 kWp → R$ 700

**Arquivos alterados:**
- `frontend/src/pages/Orcamentos.jsx`

---

### 5. Formatação de CEP ✅

**Problema:** 
- CEP limitado a 8 caracteres sem formatação
- CEP desaparecia ao editar cliente

**Solução:**
- Adicionada máscara: 00000-000
- CEP formatado ao carregar para edição
- Removida formatação antes de salvar no banco

**Arquivos alterados:**
- `frontend/src/pages/Clientes.jsx`

---

### 6. Indicador de Overload Visual ✅

**Problema:** Não havia indicação visual do overload disponível/usado

**Solução:**
- Adicionado badge mostrando overload máximo do fabricante
- Adicionado badge mostrando overload em uso
- Cores: verde (OK) / vermelho (excedido)

**Exemplo visual:**
```
Overload: 70%  |  Usando: 55.1% ✅
```

**Arquivos alterados:**
- `frontend/src/pages/Orcamentos.jsx`

---

### 7. Valores Null em Selects ✅

**Problema:** Warning no console sobre valores null em selects

**Solução:**
- Garantido valores vazios ('') ao invés de null
- Aplicado em vendedor e estado

**Arquivos alterados:**
- `frontend/src/pages/Clientes.jsx`

---

### 8. Tratamento de Erros no Login ✅

**Problema:** Erros de login mostravam apenas "Object"

**Solução:**
- Adicionados logs detalhados
- Mensagens de erro mais descritivas
- Fallback para erro de conexão

**Arquivos alterados:**
- `frontend/src/pages/Login.jsx`

---

## 📜 Scripts Criados

### 1. recalcular_orcamentos.py

**Função:** Recalcula todos os orçamentos existentes com as fórmulas corretas

**Uso:**
```bash
docker-compose exec backend python recalcular_orcamentos.py
```

**O que faz:**
- Recalcula subtotal
- Adiciona margens (comissão, lucro, imposto)
- Arredonda valores
- Adiciona margem de desconto
- Arredonda valor final
- Atualiza banco de dados

---

### 2. corrigir_overload.py

**Função:** Corrige valores de overload por fabricante

**Uso:**
```bash
docker-compose exec backend python corrigir_overload.py
```

**Valores configurados:**
- Solis: 1.70 (70%)
- SAJ: 2.00 (100%)
- Deye: 1.50 (50%)
- Outros: 1.50 (50% padrão)

---

## 🎯 Melhorias de UX

### 1. Cálculo Automático
- Material elétrico calculado automaticamente ao selecionar inversor
- Validação de dimensionamento em tempo real

### 2. Feedback Visual
- Badges coloridos para status de overload
- Indicadores de potência (kWp)
- Mensagens de toast para ações

### 3. Formatação Automática
- CEP: 00000-000
- CPF: 000.000.000-00
- CNPJ: 00.000.000/0000-00
- Telefone: (00) 00000-0000

---

## 📊 Impacto das Mudanças

### Performance
- ✅ Cache-busting evita dados desatualizados
- ✅ Cálculos otimizados no frontend

### Precisão
- ✅ Valores sempre arredondados corretamente
- ✅ Overload calculado corretamente
- ✅ Material elétrico baseado no inversor

### Usabilidade
- ✅ Feedback visual claro
- ✅ Validações em tempo real
- ✅ Formatação automática de campos

---

## 🔄 Próximos Passos Sugeridos

1. [ ] Adicionar histórico de alterações em orçamentos
2. [ ] Implementar exportação de orçamentos em PDF
3. [ ] Criar dashboard com gráficos de vendas
4. [ ] Adicionar notificações por email
5. [ ] Implementar sistema de aprovação de descontos

---

**Data:** 2024
**Versão:** 1.0
