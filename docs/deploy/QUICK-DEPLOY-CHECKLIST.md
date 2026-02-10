# ✅ Checklist Rápido de Deploy CI/CD

## 🚀 Setup Inicial (Fazer 1 vez)

### 1. Configurar Servidores
```bash
# DEV Server
ssh ubuntu@SEU_IP_DEV
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo mkdir -p /opt/crm-solar/.backup
sudo chown -R $USER:$USER /opt/crm-solar
```

### 2. Gerar Chaves SSH
```bash
# No seu PC
ssh-keygen -t ed25519 -C "github-dev" -f ~/.ssh/github_dev
ssh-keygen -t ed25519 -C "github-prod" -f ~/.ssh/github_prod

# Copiar para servidores
ssh-copy-id -i ~/.ssh/github_dev.pub ubuntu@SEU_IP_DEV
ssh-copy-id -i ~/.ssh/github_prod.pub ubuntu@SEU_IP_PROD
```

### 3. Configurar GitHub Secrets
```
Settings → Secrets and variables → Actions → New secret

DEV_SSH_KEY = [conteúdo de ~/.ssh/github_dev]
DEV_HOST = [IP do servidor DEV]
DEV_USER = ubuntu

PROD_SSH_KEY = [conteúdo de ~/.ssh/github_prod]
PROD_HOST = [IP do servidor PROD]
PROD_USER = ubuntu
```

### 4. Configurar Environments
```
Settings → Environments → New environment

Nome: development
- Sem proteções

Nome: production
- ✅ Required reviewers (adicione você)
- ✅ Deployment branches: Only protected branches
```

### 5. Preparar Servidores
```bash
# Em cada servidor (DEV e PROD)
cd /opt/crm-solar
git clone https://github.com/SEU_USUARIO/SunOps---SaaS.git .

# DEV
git checkout dev

# PROD
git checkout prod

# Criar .env
nano .env
# Copiar de .env.example e preencher

# Iniciar
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

---

## 🔄 Uso Diário

### Deploy para DEV (Automático)
```bash
git checkout dev
git add .
git commit -m "feat: minha feature"
git push origin dev
# ✅ Deploy automático inicia
```

### Deploy para PROD (Com aprovação)
```bash
git checkout prod
git merge dev
git push origin prod
# ⏸️ Aguarda aprovação no GitHub
# ✅ Após aprovar, deploy inicia
```

### Rollback Manual
```
GitHub → Actions → Manual Rollback → Run workflow
Escolher: production ou development
Clicar: Run workflow
```

---

## 🔍 Verificações

### Verificar Deploy
```bash
# Ver workflow
GitHub → Actions → Deploy DEV/PROD

# Ver logs no servidor
ssh ubuntu@servidor
cd /opt/crm-solar
docker-compose -f docker-compose.prod.yml logs -f
```

### Health Check
```bash
curl http://SEU_SERVIDOR:8000/health/
```

### Ver Backups
```bash
ssh ubuntu@servidor
ls -lh /opt/crm-solar/.backup/
```

---

## 🆘 Emergência

### Rollback Rápido
```bash
ssh ubuntu@servidor
cd /opt/crm-solar
./scripts/rollback.sh
```

### Ver Logs
```bash
docker-compose -f docker-compose.prod.yml logs --tail=100
```

### Reiniciar Tudo
```bash
docker-compose -f docker-compose.prod.yml restart
```

---

## 📊 Estrutura de Branches

```
main/prod ← PRODUÇÃO (requer aprovação)
    ↑
    | merge
    |
dev ← DESENVOLVIMENTO (deploy automático)
    ↑
    | merge
    |
feature/* ← FEATURES (CI apenas)
```

---

## ✅ Checklist Pré-Deploy

- [ ] Testes passando
- [ ] Code review feito
- [ ] .env atualizado
- [ ] Backup recente existe
- [ ] Equipe avisada

## ✅ Checklist Pós-Deploy

- [ ] Health check OK
- [ ] Login funciona
- [ ] Funcionalidades críticas OK
- [ ] Logs sem erros
- [ ] Backup criado

---

## 📞 Comandos Úteis

```bash
# Ver status
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f backend

# Entrar no container
docker-compose -f docker-compose.prod.yml exec backend bash

# Backup manual
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U postgres crm_solar > backup.sql

# Restaurar backup
docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres crm_solar < backup.sql

# Limpar imagens antigas
docker image prune -af
```

---

**Pronto! Seu CI/CD está configurado! 🎉**
