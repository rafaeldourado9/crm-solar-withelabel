# CRM Solar - Sistema de Gestão para Energia Solar

Sistema completo de CRM para empresas de energia solar fotovoltaica, com cálculo automático de dimensionamento, gestão de orçamentos, propostas e contratos.

## 🚀 Quick Start

### Opção 1: Setup Gratuito (30 min - $0/mês)
```bash
# Para 20 usuários - AWS Free Tier
📖 Seguir: docs/deploy/QUICK-FREE-SETUP.md
```

### Opção 2: Setup Profissional (2h - ~$85/mês)
```bash
# Produção escalável - EC2 + RDS + S3 + CDN
📖 Seguir: docs/deploy/AWS-SETUP-COMPLETO.md
```

**📚 [Índice Completo de Deploy](./docs/deploy/INDEX-DEPLOY.md)**

---

## 🎯 Tecnologias

### Backend
- Django 5.0.1
- Django REST Framework
- PostgreSQL
- Redis
- Token Authentication

### Frontend
- React 18
- Vite
- TailwindCSS
- Axios
- React Router DOM
- Lucide Icons

---

## 📋 Funcionalidades

- ✅ **Autenticação:** Login com token, rotas protegidas
- ✅ **Dashboard:** KPIs e métricas em tempo real
- ✅ **Gestão de Clientes:** CRUD completo com filtros
- ✅ **Calculadora Solar Inteligente:**
  - Dimensionamento automático baseado em consumo
  - Cálculo de quantidade de painéis e inversores
  - Simulação financeira com margem de lucro
  - Parcelamento com taxas de juros configuráveis
- ✅ **Premissas Globais:** Configurações centralizadas (HSP, perdas, taxas)
- ✅ **Orçamentos:** Geração automática com PDF
- ✅ **Propostas:** Conversão de orçamentos
- ✅ **Contratos:** Gestão completa

---

## 🏗️ Estrutura do Projeto

```
crm-solar/
├── .github/workflows/      # CI/CD GitHub Actions
│   ├── ci.yml             # Testes + OWASP
│   ├── deploy-dev.yml     # Deploy DEV automático
│   ├── deploy-prod.yml    # Deploy PROD com aprovação
│   ├── rollback.yml       # Rollback manual
│   └── owasp-security.yml # Scan OWASP semanal
│
├── backend/               # Django API
│   ├── apps/             # Módulos da aplicação
│   ├── config/           # Configurações Django
│   └── requirements.txt  # Dependências Python
│
├── frontend/             # React SPA
│   ├── src/             # Código fonte
│   └── package.json     # Dependências Node
│
├── docs/                # Documentação
│   ├── deploy/          # Guias de deploy
│   ├── templates/       # Templates de documentos
│   └── sprints/         # Planejamento
│
├── scripts/             # Scripts auxiliares
│   ├── setup-ec2.sh    # Setup automático servidor
│   ├── rollback.sh     # Rollback emergência
│   └── deploy-helper.sh # Menu interativo
│
├── nginx/               # Configurações Nginx
├── docker-compose.yml   # Desenvolvimento local
└── README.md           # Este arquivo
```

---

## 🔧 Desenvolvimento Local

```bash
# Clonar repositório
git clone https://github.com/rafaeldourado8/SunOps---SaaS.git
cd SunOps---SaaS

# Configurar variáveis
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Iniciar containers
docker-compose up -d

# Executar migrações
docker-compose exec backend python manage.py migrate

# Criar superusuário
docker-compose exec backend python manage.py createsuperuser

# Acessar
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
# Admin:    http://localhost:8000/admin
```

---

## 🚀 Deploy & CI/CD

### Estrutura de Branches
```
feature/* → development → prod
```

### Deploy Automático
```bash
# DEV: Push automático
git push origin development

# PROD: Requer aprovação no GitHub
git push origin prod
```

### Segurança OWASP
- ✅ Dependency Check
- ✅ Bandit (Python)
- ✅ Safety (vulnerabilidades)
- ✅ NPM Audit
- ✅ Trivy (containers)
- ✅ ZAP (web scan)

---

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

---

## 📚 Documentação

- **[Índice de Deploy](./docs/deploy/INDEX-DEPLOY.md)** - Todos os guias
- **[Quick Start FREE](./docs/deploy/QUICK-FREE-SETUP.md)** - Setup gratuito
- **[Setup Completo](./docs/deploy/AWS-SETUP-COMPLETO.md)** - Produção
- **[Troubleshooting](./docs/deploy/TROUBLESHOOTING-CICD.md)** - Problemas
- **[API](./docs/API.md)** - Endpoints
- **[Sprints](./docs/sprints/)** - Planejamento

---

## 💰 Custos

### FREE Tier (12 meses)
- EC2 t2.micro: $0
- 30 GB storage: $0
- 20 usuários: ✅
- **Total: $0/mês**

### Produção
- EC2 + RDS + S3 + CDN
- **Total: ~$85-150/mês**

---

## 🤝 Contribuindo

```bash
# Criar feature
git checkout -b feature/minha-feature

# Commit
git commit -m "feat: minha funcionalidade"

# Push
git push origin feature/minha-feature

# Criar Pull Request no GitHub
```

---

## 📝 Licença

Proprietary - Todos os direitos reservados

---

## 📞 Suporte

- **Documentação:** [docs/deploy/](./docs/deploy/)
- **Issues:** GitHub Issues
- **Deploy:** Seguir guias em docs/deploy/

---

**Desenvolvido com ❤️ para o setor de energia solar**
