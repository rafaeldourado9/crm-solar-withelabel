# Frontend - CRM Solar

Interface moderna e responsiva para o sistema de gestão de energia solar.

## 🎨 Design

- **Cores principais**: 
  - Preto (#000000) - Principal
  - Amarelo (#fdd639) - Detalhes/Accent
- **Framework**: React + Vite
- **Estilização**: Tailwind CSS
- **Ícones**: Lucide React

## 🚀 Instalação

```bash
cd frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev

# Build para produção
npm run build
```

## 📱 Páginas

- **Dashboard** - Visão geral com estatísticas
- **Clientes** - Gestão de clientes com filtros
- **Orçamentos** - Criar e gerenciar orçamentos
- **Propostas** - Acompanhar propostas e aceites
- **Contratos** - Contratos fechados
- **Vendedores** - Gestão de vendedores e comissões
- **Equipamentos** - Estoque e custos
- **Premissas** - Configurações do sistema
- **IA Features** - Funcionalidades de inteligência artificial

## 🎯 Funcionalidades

✅ Interface responsiva
✅ Filtros e busca em tempo real
✅ Modais para criação rápida
✅ Cards informativos
✅ Tabelas com ações
✅ Badges de status coloridos
✅ Integração completa com API
✅ Chatbot de IA
✅ Upload de arquivos

## 🔌 API

O frontend se conecta automaticamente ao backend Django em `http://localhost:8000/api`

Proxy configurado no Vite para desenvolvimento.

## 📦 Estrutura

```
src/
├── components/     # Componentes reutilizáveis
│   ├── Sidebar.jsx
│   └── Header.jsx
├── pages/          # Páginas da aplicação
│   ├── Dashboard.jsx
│   ├── Clientes.jsx
│   ├── Orcamentos.jsx
│   ├── Propostas.jsx
│   ├── Contratos.jsx
│   ├── Vendedores.jsx
│   ├── Equipamentos.jsx
│   ├── Premissas.jsx
│   └── IAFeatures.jsx
├── services/       # Serviços de API
│   └── api.js
├── styles/         # Estilos globais
│   └── index.css
├── App.jsx         # Componente principal
└── main.jsx        # Entry point
```

## 🎨 Componentes Customizados

### Botões
- `.btn-primary` - Botão preto
- `.btn-accent` - Botão amarelo
- `.btn-outline` - Botão com borda

### Cards
- `.card` - Card padrão branco

### Badges
- `.badge-orcamento` - Azul
- `.badge-proposta` - Amarelo
- `.badge-contrato` - Verde

### Inputs
- `.input` - Input padrão com foco amarelo

## 🌐 Acesso

Após iniciar: http://localhost:5173
