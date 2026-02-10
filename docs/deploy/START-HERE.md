# 🎯 CRM Solar - Deploy em 30 Minutos

## 🆓 Setup GRATUITO - Passo a Passo Visual

```
┌─────────────────────────────────────────────────────────────┐
│  PASSO 1: AWS (10 min)                                      │
├─────────────────────────────────────────────────────────────┤
│  1. https://aws.amazon.com → Criar conta                   │
│  2. Console → EC2 → Launch Instance                         │
│  3. Ubuntu 22.04 + t2.micro (FREE) ✅                       │
│  4. Baixar chave .pem                                       │
│  5. Copiar IP público                                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  PASSO 2: Conectar (2 min)                                  │
├─────────────────────────────────────────────────────────────┤
│  ssh -i ~/.ssh/crm-solar-key.pem ubuntu@SEU_IP             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  PASSO 3: Instalar (15 min)                                 │
├─────────────────────────────────────────────────────────────┤
│  cd /opt/crm-solar                                          │
│  git clone https://github.com/SEU_USER/SunOps---SaaS.git . │
│  docker-compose up -d --build                               │
│  docker-compose exec backend python manage.py migrate      │
│  docker-compose exec backend python manage.py createsuperuser│
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  PASSO 4: GitHub Actions (3 min)                            │
├─────────────────────────────────────────────────────────────┤
│  GitHub → Settings → Secrets:                               │
│  - SSH_KEY                                                  │
│  - SERVER_HOST                                              │
│  - SERVER_USER                                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  ✅ PRONTO!                                                 │
├─────────────────────────────────────────────────────────────┤
│  Frontend: http://SEU_IP                                    │
│  Backend:  http://SEU_IP:8000/admin                         │
│  Deploy:   git push → automático!                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Comparação Rápida

```
┌──────────────────┬─────────────────┬─────────────────┐
│                  │   🆓 FREE       │  🏢 PRO         │
├──────────────────┼─────────────────┼─────────────────┤
│ Custo/mês        │ $0 (12 meses)   │ $85-150         │
│ Usuários         │ 20 simultâneos  │ Ilimitado       │
│ RAM              │ 1 GB            │ 4-8 GB          │
│ Servidores       │ 1 EC2           │ 2 EC2 + RDS     │
│ Backup           │ Manual          │ Automático      │
│ CDN              │ ❌              │ ✅ CloudFront   │
│ Setup            │ 30 min          │ 2 horas         │
│ Ideal para       │ Teste/MVP       │ Produção        │
└──────────────────┴─────────────────┴─────────────────┘
```

---

## 🚀 Começar Agora

### Opção 1: Teste Rápido (30 min)
```bash
# Seguir: QUICK-FREE-SETUP.md
# Resultado: Sistema funcionando em 30 minutos
# Custo: $0
```

### Opção 2: Produção (2 horas)
```bash
# Seguir: AWS-SETUP-COMPLETO.md
# Resultado: Infraestrutura completa
# Custo: ~$85/mês
```

---

## 📚 Documentação

```
📁 Guias Principais
├── 🆓 QUICK-FREE-SETUP.md          ⭐ Comece aqui (FREE)
├── 🏢 AWS-SETUP-COMPLETO.md        ⭐ Comece aqui (PRO)
├── 🎯 QUAL-SETUP-ESCOLHER.md       Ajuda na decisão
└── 📚 INDEX-DEPLOY.md              Índice completo

📁 Documentação Adicional
├── 📖 DEPLOY-CICD-GUIDE.md         CI/CD completo
├── 🔧 TROUBLESHOOTING-CICD.md      Problemas comuns
├── 📊 CICD-FLOW-DIAGRAM.md         Diagramas visuais
└── ✅ QUICK-DEPLOY-CHECKLIST.md    Checklist rápido
```

---

## 💡 Recomendação

```
1️⃣ Comece com FREE (30 min)
   ↓
2️⃣ Teste com usuários reais (1-3 meses)
   ↓
3️⃣ Se funcionar bem:
   ↓
4️⃣ Migre para PRO (quando necessário)
```

**Por quê?**
- ✅ Não gasta dinheiro testando
- ✅ Valida o sistema
- ✅ Aprende AWS
- ✅ Só investe quando tiver certeza

---

## 🎯 Próximo Passo

**Escolha seu caminho:**

### Para Teste/MVP:
👉 **[QUICK-FREE-SETUP.md](./QUICK-FREE-SETUP.md)**

### Para Produção:
👉 **[AWS-SETUP-COMPLETO.md](./AWS-SETUP-COMPLETO.md)**

### Ainda em dúvida?
👉 **[QUAL-SETUP-ESCOLHER.md](./QUAL-SETUP-ESCOLHER.md)**

---

**Boa sorte! 🚀**
