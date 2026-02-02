# CRM Solar - Sistema de Gestão para Energia Solar

Sistema completo de CRM para empresas de energia solar fotovoltaica, com cálculo automático de dimensionamento, gestão de orçamentos, propostas e contratos.

## 🚀 Tecnologias

### Backend
- Django 5.0.1
- Django REST Framework
- PostgreSQL
- Token Authentication
- Alembic (Migrações)

### Frontend
- React 18
- Vite
- TailwindCSS
- Axios
- React Router DOM
- Lucide Icons

## 📋 Funcionalidades

### ✅ Implementadas
- **Autenticação:** Login com token, rotas protegidas
- **Dashboard:** KPIs e métricas em tempo real
- **Gestão de Clientes:** CRUD completo com filtros
- **Calculadora Solar Inteligente:**
  - Dimensionamento automático baseado em consumo
  - Cálculo de quantidade de painéis e inversores
  - Simulação financeira com margem de lucro
  - Parcelamento com taxas de juros configuráveis
  - Ajuste manual com recálculo automático
- **Premissas Globais:** Configurações centralizadas (HSP, perdas, taxas)
- **Orçamentos:** Geração automática com PDF
- **Propostas:** Conversão de orçamentos
- **Contratos:** Gestão completa

## 🏗️ Arquitetura

```
crm_solar/
├── backend/
│   ├── apps/
│   │   ├── clientes/       # Gestão de clientes
│   │   ├── dashboard/      # Métricas e KPIs
│   │   ├── premissas/      # Configurações globais
│   │   ├── equipamentos/   # Painéis e inversores
│   │   ├── orcamentos/     # Orçamentos + Calculadora
│   │   ├── propostas/      # Propostas comerciais
│   │   ├── contratos/      # Contratos fechados
│   │   └── vendedores/     # Gestão de vendedores
│   ├── config/             # Configurações Django
│   └── alembic/            # Migrações
├── frontend/
│   └── src/
│       ├── components/     # Componentes reutilizáveis
│       ├── pages/          # Páginas da aplicação
│       └── services/       # Integração com API
└── docs/                   # Documentação completa
```

## 🔧 Instalação

### Pré-requisitos
- Docker & Docker Compose
- Git
- Google Maps API Key (opcional, para cálculo de deslocamento)

### Passo a Passo

1. Clone o repositório:
```bash
git clone <repo-url>
cd crm_solar
```

2. Configure as variáveis de ambiente:
```bash
cp backend/.env.example backend/.env
# Edite backend/.env e adicione sua GOOGLE_MAPS_API_KEY
```

3. Suba os containers:
```bash
docker-compose up -d
```

4. Execute as migrações:
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

5. Acesse:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin

## 📊 Fórmulas de Cálculo

### Dimensionamento
```
Potência Necessária (Wp) = (Consumo Mensal / 30) / (HSP × (1 - Perda))
Quantidade de Painéis = Potência Necessária / Potência do Painel
Potência do Inversor ≥ Potência Total × 0.75 (Overload)
Geração Estimada = Potência Total × HSP × 30 × (1 - Perda)
```

### Financeiro
```
Custo Total = Painéis + Inversor + Montagem + Projeto
Valor Venda = Custo Total × (1 + Margem/100)
Valor Final = Valor Venda + Impostos + Comissão
Valor Parcelado = Valor Final × (1 + Taxa Juros/100)
```

## 📚 Documentação

Consulte a pasta `/docs` para documentação detalhada:
- [Sprints](./docs/sprints/) - Planejamento e entregas
- [API](./docs/API.md) - Endpoints e exemplos
- [Arquitetura](./docs/ARCHITECTURE.md) - Decisões técnicas
- [Deploy](./docs/DEPLOY.md) - Guia de produção
- [Deslocamento](./docs/DESLOCAMENTO.md) - Cálculo de deslocamento e Google Maps

## 🤝 Contribuindo

Use o script de commits atômicos:
```bash
./commit.sh
```

## 📝 Licença

Proprietary - Todos os direitos reservados
