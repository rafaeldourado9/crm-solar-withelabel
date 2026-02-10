# 🔧 Troubleshooting CI/CD - Problemas Comuns

## 📋 Índice Rápido

1. [Erros de Deploy](#erros-de-deploy)
2. [Problemas de SSH](#problemas-de-ssh)
3. [Erros de Docker](#erros-de-docker)
4. [Problemas de Banco de Dados](#problemas-de-banco-de-dados)
5. [Health Check Falhando](#health-check-falhando)
6. [Rollback Não Funciona](#rollback-não-funciona)
7. [GitHub Actions Travado](#github-actions-travado)
8. [Problemas de Permissão](#problemas-de-permissão)

---

## 🚨 Erros de Deploy

### ❌ Erro: "Permission denied (publickey)"

**Causa:** Chave SSH não configurada corretamente

**Solução:**
```bash
# 1. Verificar se a chave existe
cat ~/.ssh/github_dev

# 2. Verificar se foi adicionada ao servidor
ssh -i ~/.ssh/github_dev ubuntu@SEU_SERVIDOR

# 3. Se não funcionar, recriar e copiar
ssh-keygen -t ed25519 -C "github-dev" -f ~/.ssh/github_dev
ssh-copy-id -i ~/.ssh/github_dev.pub ubuntu@SEU_SERVIDOR

# 4. Atualizar secret no GitHub
# Settings → Secrets → DEV_SSH_KEY
# Colar conteúdo de: cat ~/.ssh/github_dev
```

---

### ❌ Erro: "docker: command not found"

**Causa:** Docker não instalado no servidor

**Solução:**
```bash
# Conectar ao servidor
ssh ubuntu@SEU_SERVIDOR

# Instalar Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout e login novamente
exit
ssh ubuntu@SEU_SERVIDOR

# Verificar
docker --version
docker-compose --version
```

---

### ❌ Erro: "No such file or directory: docker-compose.prod.yml"

**Causa:** Aplicação não clonada no servidor

**Solução:**
```bash
# Conectar ao servidor
ssh ubuntu@SEU_SERVIDOR

# Criar diretório
sudo mkdir -p /opt/crm-solar
sudo chown -R $USER:$USER /opt/crm-solar
cd /opt/crm-solar

# Clonar repositório
git clone https://github.com/SEU_USUARIO/SunOps---SaaS.git .

# Checkout branch correta
git checkout dev  # ou prod

# Criar .env
cp .env.dev.example .env
nano .env  # Preencher variáveis

# Verificar
ls -la docker-compose.prod.yml
```

---

### ❌ Erro: "Image not found: ghcr.io/..."

**Causa:** Imagem não foi construída ou não tem permissão

**Solução:**
```bash
# 1. Verificar se workflow de build rodou
# GitHub → Actions → Verificar se "Build" passou

# 2. Verificar permissões do GHCR
# GitHub → Settings → Packages → Visibility → Public

# 3. Login manual no servidor
ssh ubuntu@SEU_SERVIDOR
echo $GITHUB_TOKEN | docker login ghcr.io -u SEU_USUARIO --password-stdin

# 4. Pull manual
docker pull ghcr.io/SEU_USUARIO/sunops---saas:dev-latest-backend
docker pull ghcr.io/SEU_USUARIO/sunops---saas:dev-latest-frontend
```

---

## 🔐 Problemas de SSH

### ❌ Erro: "Host key verification failed"

**Solução:**
```bash
# Remover host antigo
ssh-keygen -R SEU_SERVIDOR

# Adicionar novamente
ssh-keyscan -H SEU_SERVIDOR >> ~/.ssh/known_hosts

# Testar
ssh ubuntu@SEU_SERVIDOR
```

---

### ❌ Erro: "Too many authentication failures"

**Solução:**
```bash
# Especificar chave exata
ssh -i ~/.ssh/github_dev ubuntu@SEU_SERVIDOR

# Ou adicionar ao ~/.ssh/config
cat >> ~/.ssh/config << EOF
Host dev-server
    HostName SEU_IP_DEV
    User ubuntu
    IdentityFile ~/.ssh/github_dev
    IdentitiesOnly yes

Host prod-server
    HostName SEU_IP_PROD
    User ubuntu
    IdentityFile ~/.ssh/github_prod
    IdentitiesOnly yes
EOF

# Usar
ssh dev-server
```

---

## 🐳 Erros de Docker

### ❌ Erro: "Cannot connect to Docker daemon"

**Solução:**
```bash
# Verificar se Docker está rodando
sudo systemctl status docker

# Se não estiver, iniciar
sudo systemctl start docker
sudo systemctl enable docker

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Logout e login
exit
ssh ubuntu@SEU_SERVIDOR
```

---

### ❌ Erro: "No space left on device"

**Solução:**
```bash
# Verificar espaço
df -h

# Limpar imagens antigas
docker system prune -af

# Limpar volumes não usados
docker volume prune -f

# Limpar build cache
docker builder prune -af

# Se ainda não resolver, aumentar disco do servidor
```

---

### ❌ Erro: "Port already in use"

**Solução:**
```bash
# Ver o que está usando a porta
sudo lsof -i :8000
sudo lsof -i :80

# Parar containers antigos
docker-compose -f docker-compose.prod.yml down

# Ou matar processo específico
sudo kill -9 PID_DO_PROCESSO

# Reiniciar
docker-compose -f docker-compose.prod.yml up -d
```

---

## 💾 Problemas de Banco de Dados

### ❌ Erro: "FATAL: database does not exist"

**Solução:**
```bash
# Conectar ao servidor
ssh ubuntu@SEU_SERVIDOR
cd /opt/crm-solar

# Criar banco manualmente
docker-compose -f docker-compose.prod.yml exec db psql -U postgres -c "CREATE DATABASE crm_solar;"

# Executar migrações
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
```

---

### ❌ Erro: "relation does not exist"

**Solução:**
```bash
# Executar migrações
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Se não resolver, verificar migrações
docker-compose -f docker-compose.prod.yml exec backend python manage.py showmigrations

# Forçar migração específica
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate APP_NAME MIGRATION_NUMBER
```

---

### ❌ Erro: "password authentication failed"

**Solução:**
```bash
# Verificar .env
cat .env | grep DB_

# Corrigir senha
nano .env
# DB_PASSWORD=senha-correta

# Reiniciar serviços
docker-compose -f docker-compose.prod.yml restart
```

---

## 🏥 Health Check Falhando

### ❌ Erro: "Health check failed after 30 attempts"

**Diagnóstico:**
```bash
# 1. Verificar logs
docker-compose -f docker-compose.prod.yml logs backend

# 2. Verificar se backend está rodando
docker-compose -f docker-compose.prod.yml ps

# 3. Testar endpoint manualmente
curl -v http://localhost:8000/health/

# 4. Entrar no container
docker-compose -f docker-compose.prod.yml exec backend bash
python manage.py check
```

**Soluções Comuns:**

**A) Backend não iniciou:**
```bash
# Ver erro específico
docker-compose -f docker-compose.prod.yml logs backend --tail=50

# Geralmente é:
# - Erro no .env
# - Banco não conectou
# - Migração pendente
```

**B) Porta errada:**
```bash
# Verificar se está na porta 8000
docker-compose -f docker-compose.prod.yml exec backend netstat -tlnp

# Verificar docker-compose.prod.yml
cat docker-compose.prod.yml | grep -A 5 backend
```

**C) Endpoint /health/ não existe:**
```bash
# Criar endpoint de health
# backend/apps/health.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"})

# backend/config/urls.py
from apps.health import health_check

urlpatterns = [
    path('health/', health_check),
    # ...
]
```

---

## ⏮️ Rollback Não Funciona

### ❌ Erro: "No backup found"

**Solução:**
```bash
# Verificar backups
ls -lh /opt/crm-solar/.backup/

# Se não existir, criar diretório
mkdir -p /opt/crm-solar/.backup

# Criar backup manual
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U postgres crm_solar > .backup/db_manual_$(date +%Y%m%d_%H%M%S).sql

# Salvar imagens atuais
docker-compose -f docker-compose.prod.yml ps -q | xargs docker inspect --format='{{.Config.Image}}' > .backup/last_images.txt
```

---

### ❌ Erro: "Rollback script not executable"

**Solução:**
```bash
# Dar permissão de execução
chmod +x /opt/crm-solar/scripts/rollback.sh

# Executar
./scripts/rollback.sh
```

---

## 🔄 GitHub Actions Travado

### ❌ Workflow não inicia

**Solução:**
```bash
# 1. Verificar se Actions está habilitado
# GitHub → Settings → Actions → General → Allow all actions

# 2. Verificar se há runners disponíveis
# GitHub → Actions → Runners

# 3. Cancelar workflows antigos
# GitHub → Actions → [workflow] → Cancel workflow

# 4. Re-run workflow
# GitHub → Actions → [workflow] → Re-run all jobs
```

---

### ❌ Workflow fica em "Waiting for approval"

**Solução:**
```bash
# 1. Ir para o workflow
# GitHub → Actions → [workflow em espera]

# 2. Clicar em "Review deployments"

# 3. Selecionar environment (production)

# 4. Clicar em "Approve and deploy"
```

---

### ❌ Erro: "Secret not found"

**Solução:**
```bash
# Verificar secrets
# GitHub → Settings → Secrets and variables → Actions

# Adicionar secrets faltantes:
# DEV_SSH_KEY
# DEV_HOST
# DEV_USER
# PROD_SSH_KEY
# PROD_HOST
# PROD_USER

# Importante: Secrets devem estar no repositório, não no environment
```

---

## 🔒 Problemas de Permissão

### ❌ Erro: "Permission denied: /opt/crm-solar"

**Solução:**
```bash
# Dar permissão ao usuário
sudo chown -R $USER:$USER /opt/crm-solar

# Verificar
ls -la /opt/
```

---

### ❌ Erro: "Cannot write to .backup/"

**Solução:**
```bash
# Criar diretório com permissões corretas
mkdir -p /opt/crm-solar/.backup
chmod 755 /opt/crm-solar/.backup

# Verificar
ls -la /opt/crm-solar/
```

---

## 🆘 Comandos de Emergência

### Parar tudo e recomeçar:
```bash
cd /opt/crm-solar
docker-compose -f docker-compose.prod.yml down
docker system prune -af
git pull origin dev  # ou prod
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
```

### Ver todos os logs:
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

### Resetar banco (CUIDADO!):
```bash
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

### Verificar tudo:
```bash
# Status dos containers
docker-compose -f docker-compose.prod.yml ps

# Health check
curl http://localhost:8000/health/

# Logs recentes
docker-compose -f docker-compose.prod.yml logs --tail=50

# Espaço em disco
df -h

# Memória
free -h

# Processos
top
```

---

## 📞 Checklist de Diagnóstico

Quando algo der errado, siga esta ordem:

1. **Ver logs do GitHub Actions**
   - Qual step falhou?
   - Qual a mensagem de erro?

2. **Conectar ao servidor**
   ```bash
   ssh ubuntu@SEU_SERVIDOR
   cd /opt/crm-solar
   ```

3. **Verificar containers**
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   ```

4. **Ver logs dos containers**
   ```bash
   docker-compose -f docker-compose.prod.yml logs backend
   docker-compose -f docker-compose.prod.yml logs frontend
   docker-compose -f docker-compose.prod.yml logs db
   ```

5. **Testar health check**
   ```bash
   curl -v http://localhost:8000/health/
   ```

6. **Verificar .env**
   ```bash
   cat .env
   ```

7. **Verificar backups**
   ```bash
   ls -lh .backup/
   ```

8. **Se tudo falhar: ROLLBACK**
   ```bash
   ./scripts/rollback.sh
   ```

---

## 📚 Recursos Adicionais

- **Documentação Completa:** [DEPLOY-CICD-GUIDE.md](./DEPLOY-CICD-GUIDE.md)
- **Checklist Rápido:** [QUICK-DEPLOY-CHECKLIST.md](./QUICK-DEPLOY-CHECKLIST.md)
- **Diagrama de Fluxo:** [CICD-FLOW-DIAGRAM.md](./CICD-FLOW-DIAGRAM.md)

---

**Dica:** Mantenha este arquivo aberto durante deploys! 🚀
