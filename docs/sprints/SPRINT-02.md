# Sprint 2 - Gestão de Clientes

**Período:** Semana 2  
**Status:** ✅ Concluído

## Objetivos
Implementar CRUD completo de clientes com filtros e busca.

## User Stories

### US-004: Listar Clientes
**Como** vendedor  
**Quero** ver meus clientes  
**Para** gerenciar minha carteira

**Critérios de Aceitação:**
- [x] Tabela responsiva com clientes
- [x] Filtro por status (orçamento, proposta, contrato)
- [x] Busca por nome e cidade
- [x] Usuário comum vê apenas seus clientes
- [x] Admin vê todos os clientes

**Implementação:**
- Backend: ClienteViewSet com get_queryset customizado
- Frontend: `pages/Clientes.jsx`

### US-005: Criar/Editar Cliente
**Como** vendedor  
**Quero** cadastrar novos clientes  
**Para** iniciar o processo comercial

**Critérios de Aceitação:**
- [x] Modal com formulário
- [x] Campos: nome, CPF/CNPJ, telefone, email, cidade, estado, status
- [x] Validação de campos obrigatórios
- [x] Edição inline
- [x] Cliente associado ao usuário logado

**Implementação:**
- Método perform_create no ViewSet
- Modal reutilizável no frontend

### US-006: Excluir Cliente
**Como** vendedor  
**Quero** excluir clientes  
**Para** manter minha base limpa

**Critérios de Aceitação:**
- [x] Confirmação antes de excluir
- [x] Apenas criador ou admin pode excluir
- [x] Atualização automática da lista

## Tarefas Técnicas

### Backend
- [x] Adicionar permission_classes em ClienteViewSet
- [x] Implementar filtros (status, cidade)
- [x] Adicionar search_fields
- [x] Criar serializer com criado_por_nome

### Frontend
- [x] Criar modal de formulário
- [x] Implementar estados de edição
- [x] Adicionar botões de ação (editar/excluir)
- [x] Tratamento de resposta paginada

## Métricas
- **Commits:** 6
- **Arquivos Alterados:** 4
- **Linhas de Código:** ~400

## Retrospectiva

### O que funcionou bem ✅
- CRUD completo e funcional
- Filtros facilitam navegação
- Modal reutilizável

### Melhorias para próxima sprint 🔄
- Adicionar paginação no frontend
- Implementar exportação para Excel
- Adicionar mais campos de endereço
