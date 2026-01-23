# Sprint 1 - Autenticação e Estrutura Base

**Período:** Semana 1  
**Status:** ✅ Concluído

## Objetivos
Estabelecer a base do sistema com autenticação funcional e estrutura de rotas.

## User Stories

### US-001: Login de Usuário
**Como** vendedor  
**Quero** fazer login no sistema  
**Para** acessar minhas funcionalidades

**Critérios de Aceitação:**
- [x] Tela de login responsiva e centralizada
- [x] Validação de credenciais
- [x] Token salvo no localStorage
- [x] Redirecionamento para dashboard após login
- [x] Mensagem de erro para credenciais inválidas

**Implementação:**
- Backend: Token Authentication (Django REST Framework)
- Frontend: `pages/Login.jsx`
- Endpoint: `POST /api/auth/login/`

### US-002: Rotas Protegidas
**Como** sistema  
**Quero** proteger rotas privadas  
**Para** garantir que apenas usuários autenticados acessem

**Critérios de Aceitação:**
- [x] Componente PrivateRoute criado
- [x] Redirecionamento para /login se não autenticado
- [x] Interceptor Axios para incluir token
- [x] Logout automático em erro 401

**Implementação:**
- `components/PrivateRoute.jsx`
- `services/api.js` com interceptors
- `components/Sidebar.jsx` com botão de logout

### US-003: Dashboard Básico
**Como** vendedor  
**Quero** ver métricas do meu trabalho  
**Para** acompanhar meu desempenho

**Critérios de Aceitação:**
- [x] Cards com total de clientes, leads e propostas
- [x] Tabela com últimos 5 clientes
- [x] Dados filtrados por usuário (não admin)

**Implementação:**
- Backend: `apps/dashboard/views.py` - DashboardResumoView
- Frontend: `pages/Dashboard.jsx`
- Endpoint: `GET /api/dashboard/resumo/`

## Tarefas Técnicas

### Backend
- [x] Configurar rest_framework.authtoken
- [x] Criar app dashboard
- [x] Implementar DashboardResumoView
- [x] Adicionar campo criado_por em Cliente
- [x] Configurar CORS

### Frontend
- [x] Criar página de Login
- [x] Implementar PrivateRoute
- [x] Configurar interceptors Axios
- [x] Atualizar App.jsx com rotas
- [x] Criar serviço clientesService

## Métricas
- **Commits:** 8
- **Arquivos Alterados:** 12
- **Linhas de Código:** ~800

## Retrospectiva

### O que funcionou bem ✅
- Autenticação simples e eficaz
- Interceptors do Axios facilitaram o fluxo
- Dashboard com dados reais

### Melhorias para próxima sprint 🔄
- Adicionar refresh token
- Implementar loading states
- Melhorar tratamento de erros
