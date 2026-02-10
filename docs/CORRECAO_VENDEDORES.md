# Correção: Isolamento de Vendedores

## 🎯 Problema Resolvido

Vendedores não tinham visibilidade isolada de seus clientes e orçamentos. Um orçamento criado pelo ROOT aparecia para todos os vendedores.

## ✅ Solução Implementada

### 1. **Backend - Filtro de Orçamentos** (`apps/orcamentos/views.py`)

```python
def get_queryset(self):
    user = self.request.user
    if user.is_staff or user.is_superuser:
        return Orcamento.objects.all()  # Admin vê tudo
    if hasattr(user, 'vendedor'):
        return Orcamento.objects.filter(vendedor=user.vendedor)  # Vendedor vê só seus
    return Orcamento.objects.filter(cliente__criado_por=user)
```

### 2. **Backend - Atribuição Automática de Vendedor**

Quando um orçamento é criado, o vendedor do cliente é automaticamente atribuído:

```python
vendedor_id = data.get('vendedor_id') or (cliente.vendedor.id if cliente.vendedor else None)
```

### 3. **Migração de Dados**

Criada migração `0012_sync_vendedor_orcamentos.py` que sincroniza orçamentos existentes com o vendedor do cliente.

## 🚀 Como Aplicar

### Windows:
```bash
aplicar-correcoes-vendedor.bat
```

### Linux/Mac:
```bash
chmod +x aplicar-correcoes-vendedor.sh
./aplicar-correcoes-vendedor.sh
```

### Manual:
```bash
docker-compose exec backend python manage.py migrate orcamentos
docker-compose restart backend
```

## 📊 Comportamento Após Correção

### Admin/Root (is_staff ou is_superuser):
- ✅ Vê TODOS os clientes
- ✅ Vê TODOS os orçamentos
- ✅ Pode criar orçamentos para qualquer cliente

### Vendedor (user.vendedor existe):
- ✅ Vê APENAS seus clientes (onde `cliente.vendedor = user.vendedor`)
- ✅ Vê APENAS seus orçamentos (onde `orcamento.vendedor = user.vendedor`)
- ✅ Ao criar orçamento, lista apenas seus clientes
- ✅ Orçamento criado é automaticamente atribuído a ele

### Usuário Comum:
- ✅ Vê clientes que ele criou
- ✅ Vê orçamentos de clientes que ele criou

## 🔍 Fluxo Completo

1. **Admin cria cliente** → Atribui vendedor ao cliente
2. **Vendedor faz login** → Vê apenas clientes atribuídos a ele
3. **Vendedor cria orçamento** → Seleciona entre seus clientes
4. **Sistema atribui automaticamente** → `orcamento.vendedor = cliente.vendedor`
5. **Vendedor vê orçamento** → Aparece na lista dele

## 🧪 Como Testar

1. **Login como Admin:**
   - Crie um cliente
   - Atribua um vendedor ao cliente
   - Crie um orçamento para esse cliente

2. **Login como Vendedor:**
   - Verifique que vê apenas seus clientes
   - Verifique que vê apenas seus orçamentos
   - Crie um novo orçamento
   - Confirme que só aparecem seus clientes na lista

3. **Login como Admin novamente:**
   - Confirme que vê todos os orçamentos de todos os vendedores

## 📝 Arquivos Modificados

- `backend/apps/orcamentos/views.py` - Adicionado `get_queryset()` e lógica de atribuição
- `backend/apps/orcamentos/migrations/0012_sync_vendedor_orcamentos.py` - Nova migração
- `aplicar-correcoes-vendedor.bat` - Script Windows
- `aplicar-correcoes-vendedor.sh` - Script Linux/Mac

## ⚠️ Importante

- Clientes SEM vendedor atribuído não aparecerão para vendedores
- Admin sempre vê tudo
- A migração sincroniza orçamentos existentes automaticamente
