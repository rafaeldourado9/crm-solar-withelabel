# Guia Rápido - CRM Solar

## 🚀 Início Rápido

### Subir o Sistema
```bash
docker-compose up -d
```

### Acessar
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin

---

## 📋 Tarefas Comuns

### Criar Orçamento

1. **Selecionar Cliente**
2. **Escolher Painéis** (busca por fabricante ou potência)
3. **Escolher Inversor** (busca por fabricante ou potência)
4. **Verificar Overload** (badge verde = OK)
5. **Confirmar Material Elétrico** (calculado automaticamente)
6. **Criar Orçamento**

### Editar Orçamento

1. Clicar em "Ver Detalhes"
2. Clicar em "Editar"
3. Duplo clique nos itens para editar
4. Valores recalculam automaticamente
5. Clicar em "Salvar"

---

## 🔢 Fórmulas Rápidas

### Dimensionamento
```
Capacidade Inversor = Potência × Overload × Quantidade
Válido se: Potência Painéis ≤ Capacidade Inversor
```

### Overload por Fabricante
- **Solis**: 70%
- **SAJ**: 100%
- **Deye**: 50%
- **Outros**: 50%

### Material Elétrico
```
Base = (Potência Inversor × Qtd) / 1000 kWp
```

### Valor Final
```
1. Subtotal (kit + projeto + montagem + estrutura + material)
2. + Margens (comissão + lucro + imposto)
3. Arredondar para centena
4. + Margem desconto (2%)
5. Arredondar para centena = VALOR FINAL
```

---

## 🛠️ Comandos Úteis

### Recalcular Orçamentos
```bash
docker-compose exec backend python recalcular_orcamentos.py
```

### Corrigir Overload
```bash
docker-compose exec backend python corrigir_overload.py
```

### Ver Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Acessar Banco de Dados
```bash
docker-compose exec db psql -U postgres -d crm_solar
```

### Reiniciar Serviços
```bash
docker-compose restart backend
docker-compose restart frontend
```

---

## 🎨 Atalhos do Sistema

### Clientes
- **Buscar**: Digite nome ou cidade
- **Filtrar**: Todos / Orçamento / Proposta / Contrato
- **CEP**: Preenche endereço automaticamente

### Orçamentos
- **Buscar Painel**: Digite 2+ caracteres
- **Buscar Inversor**: Digite 2+ caracteres
- **Overload**: Verde = OK, Vermelho = Excedido

### Edição
- **Duplo Clique**: Editar item
- **✓ OK**: Confirmar edição
- **Lixeira**: Remover item

---

## ⚠️ Validações

### Dimensionamento
- ❌ Potência painéis > Capacidade inversor
- ✅ Potência painéis ≤ Capacidade inversor

### Campos Obrigatórios
- Nome do Kit
- Cliente
- Valor do Kit
- Painel (fabricante + potência)
- Inversor (fabricante + potência)
- Cidade
- Estado

---

## 🐛 Problemas Comuns

### Valores não arredondados
```bash
docker-compose exec backend python recalcular_orcamentos.py
```

### Overload incorreto
```bash
docker-compose exec backend python corrigir_overload.py
```

### Cards não atualizam
- Recarregar página (F5)
- Verificar console do navegador

### CEP não preenche
- Verificar conexão com ViaCEP
- CEP deve ter 8 dígitos

---

## 📞 Suporte

### Logs de Erro
1. Abrir DevTools (F12)
2. Aba Console
3. Copiar mensagem de erro

### Banco de Dados
```sql
-- Ver orçamentos
SELECT * FROM orcamentos ORDER BY id DESC LIMIT 10;

-- Ver inversores
SELECT fabricante, potencia_w, overload FROM inversores;

-- Ver premissas
SELECT * FROM premissas WHERE ativa = true;
```

---

## 📚 Documentação Completa

- [Cálculos Detalhados](./CALCULOS.md)
- [Changelog](./CHANGELOG.md)
- [README Principal](../README.md)

---

**Dica:** Mantenha este guia aberto durante o uso do sistema! 📌
