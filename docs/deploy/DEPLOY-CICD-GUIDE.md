# 🚀 Guia de Deploy CI/CD com Fallback

## 📋 Índice
1. [Pré-requisitos](#pré-requisitos)
2. [Configuração dos Servidores](#configuração-dos-servidores)
3. [Configuração do GitHub](#configuração-do-github)
4. [Estrutura de Branches](#estrutura-de-branches)
5. [Fluxo de Deploy](#fluxo-de-deploy)
6. [Rollback Manual](#rollback-manual)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 Pré-requisitos

### Servidores
- **DEV:** 1 servidor (mínimo 2GB RAM, 2 vCPUs)
- **PROD:** 1 servidor (mínimo 4GB RAM, 4 vCPUs)
- Ubuntu 20.04+ ou Amazon Linux 2
- Docker e Docker Compose instalados
- Acesso SSH configurado

### GitHub
- Repositório com GitHub Actions habilitado
- GitHub Container Registry (GHCR) habilitado
- Secrets configurados

---

## 🖥️ Configuração dos Servidores

### 1. Preparar Servidor DEV

```bash
# Conectar ao servidor
ssh ubuntu@seu-servidor-dev

# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Criar estrutura de diretórios
sudo mkdir -p /opt/crm-solar/.backup
sudo chown -R $USER:$USER /opt/crm-solar
cd /opt/crm-solar

# Clonar repositório
git clone https://github.com/seu-usuario/SunOps---SaaS.git .
git checkout dev

# Criar arquivo .env
cat > .env << 'EOF'
# Django
SECRET_KEY=your-super-secret-key-change-this
DEBUG=False
ALLOWED_HOSTS=seu-dominio-dev.com,localhost

# Database
DB_NAME=crm_solar
DB_USER=postgres
DB_PASSWORD=strong-password-here
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# CORS
CORS_ORIGINS=https://seu-dominio-dev.com

# APIs (opcional)
GOOGLE_MAPS_API_KEY=
GEMINI_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
EOF

# Iniciar serviços
docker-compose -f docker-compose.prod.yml up -d

# Executar migrações
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

# Verificar
docker-compose -f docker-compose.prod.yml ps
curl http://localhost:8000/health/
```

### 2. Preparar Servidor PROD

```bash
# Repetir os mesmos passos do DEV, mas:
# - Usar branch 'prod' ou 'main'
# - Usar senhas mais fortes
# - Configurar domínio de produção
# - Configurar SSL/TLS (Let's Encrypt)

# Instalar Certbot para SSL
sudo apt install certbot python3-certbot-nginx -y

# Configurar SSL
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
```

### 3. Configurar Nginx (Opcional - para SSL)

```bash
# Criar configuração Nginx
sudo nano /etc/nginx/sites-available/crm-solar

# Adicionar:
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name seu-dominio.com www.seu-dominio.com;

    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Ativar configuração
sudo ln -s /etc/nginx/sites-available/crm-solar /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔐 Configuração do GitHub

### 1. Gerar Chaves SSH

```bash
# No seu computador local
ssh-keygen -t ed25519 -C "github-actions-dev" -f ~/.ssh/github_dev
ssh-keygen -t ed25519 -C "github-actions-prod" -f ~/.ssh/github_prod

# Copiar chaves públicas para os servidores
ssh-copy-id -i ~/.ssh/github_dev.pub ubuntu@servidor-dev
ssh-copy-id -i ~/.ssh/github_prod.pub ubuntu@servidor-prod

# Exibir chaves privadas (para adicionar nos secrets)
cat ~/.ssh/github_dev
cat ~/.ssh/github_prod
```

### 2. Configurar Secrets no GitHub

Vá em: **Settings → Secrets and variables → Actions → New repository secret**

#### Secrets para DEV:
```
DEV_SSH_KEY = conteúdo de ~/.ssh/github_dev (chave privada)
DEV_HOST = IP ou domínio do servidor DEV
DEV_USER = ubuntu (ou seu usuário SSH)
```

#### Secrets para PROD:
```
PROD_SSH_KEY = conteúdo de ~/.ssh/github_prod (chave privada)
PROD_HOST = IP ou domínio do servidor PROD
PROD_USER = ubuntu (ou seu usuário SSH)
```

### 3. Configurar Environments

Vá em: **Settings → Environments**

#### Environment: development
- Sem proteções (deploy automático)

#### Environment: production
- ✅ Required reviewers: adicione você mesmo
- ✅ Wait timer: 5 minutos (opcional)
- ✅ Deployment branches: Only protected branches

### 4. Habilitar GitHub Container Registry

```bash
# No seu computador local
echo $GITHUB_TOKEN | docker login ghcr.io -u SEU_USUARIO --password-stdin

# Ou criar Personal Access Token:
# Settings → Developer settings → Personal access tokens → Tokens (classic)
# Permissões: write:packages, read:packages, delete:packages
```

---

## 🌿 Estrutura de Branches

```
main/prod (produção)
    ↑
    | (merge após aprovação)
    |
dev (desenvolvimento)
    ↑
    | (merge após testes)
    |
feature/* (features)
```

### Workflow:

1. **Desenvolvimento:**
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feature/nova-funcionalidade
   # ... fazer alterações ...
   git add .
   git commit -m "feat: nova funcionalidade"
   git push origin feature/nova-funcionalidade
   ```

2. **Pull Request para DEV:**
   - Criar PR de `feature/*` → `dev`
   - CI roda automaticamente
   - Após merge, deploy automático para DEV

3. **Pull Request para PROD:**
   - Criar PR de `dev` → `prod` (ou `main`)
   - CI roda automaticamente
   - Requer aprovação manual
   - Após aprovação, deploy para PROD

---

## 🚀 Fluxo de Deploy

### Deploy Automático DEV

```bash
# Qualquer push para branch 'dev' dispara deploy automático
git checkout dev
git merge feature/minha-feature
git push origin dev

# GitHub Actions irá:
# 1. Rodar testes
# 2. Build das imagens Docker
# 3. Push para GHCR
# 4. Deploy no servidor DEV
# 5. Health check
# 6. Rollback automático se falhar
```

### Deploy Manual DEV

```bash
# Via GitHub Actions UI:
# Actions → Deploy DEV → Run workflow → Run workflow
```

### Deploy PROD (com aprovação)

```bash
# Push para branch prod/main
git checkout prod
git merge dev
git push origin prod

# GitHub Actions irá:
# 1. Rodar testes + security scan
# 2. Build das imagens
# 3. AGUARDAR APROVAÇÃO MANUAL
# 4. Criar backup completo (DB + images)
# 5. Deploy no servidor PROD
# 6. Health check + smoke tests
# 7. Rollback automático se falhar
```

---

## ⏮️ Rollback Manual

### Via GitHub Actions (Recomendado)

```bash
# 1. Ir em: Actions → Manual Rollback → Run workflow
# 2. Selecionar:
#    - Environment: production ou development
#    - Backup timestamp: deixar vazio para último backup
# 3. Clicar em "Run workflow"
```

### Via SSH (Emergência)

```bash
# Conectar ao servidor
ssh ubuntu@servidor-prod
cd /opt/crm-solar

# Ver backups disponíveis
ls -lh .backup/

# Rollback completo
./scripts/rollback.sh

# Ou manual:
docker-compose -f docker-compose.prod.yml down

# Restaurar imagens anteriores
while IFS= read -r image; do
  docker pull "$image"
done < .backup/last_images.txt

# Restaurar banco de dados
LAST_BACKUP=$(ls -t .backup/db_*.sql | head -n 1)
docker-compose -f docker-compose.prod.yml up -d db
sleep 5
docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres crm_solar < "$LAST_BACKUP"

# Subir serviços
docker-compose -f docker-compose.prod.yml up -d

# Verificar
curl http://localhost:8000/health/
```

---

## 🔍 Troubleshooting

### 1. Deploy falhou mas não fez rollback

```bash
# Verificar logs do GitHub Actions
# Se necessário, fazer rollback manual via SSH

ssh ubuntu@servidor
cd /opt/crm-solar
docker-compose -f docker-compose.prod.yml logs --tail=100
```

### 2. Health check falhando

```bash
# Verificar serviços
docker-compose -f docker-compose.prod.yml ps

# Verificar logs
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend
docker-compose -f docker-compose.prod.yml logs db

# Testar manualmente
curl -v http://localhost:8000/health/
docker-compose -f docker-compose.prod.yml exec backend python manage.py check
```

### 3. Erro de permissão SSH

```bash
# Verificar chave SSH
ssh -i ~/.ssh/github_dev ubuntu@servidor-dev

# Verificar permissões no servidor
ls -la ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 4. Imagens Docker não encontradas

```bash
# Verificar login no GHCR
docker login ghcr.io -u SEU_USUARIO

# Verificar se imagens existem
docker images | grep ghcr.io

# Pull manual
docker pull ghcr.io/seu-usuario/sunops---saas:dev-latest-backend
```

### 5. Banco de dados corrompido

```bash
# Restaurar do backup mais recente
cd /opt/crm-solar
ls -lh .backup/db_*.sql

# Escolher backup
BACKUP_FILE=".backup/db_20240115_143000.sql"

# Restaurar
docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres crm_solar < "$BACKUP_FILE"

# Verificar
docker-compose -f docker-compose.prod.yml exec backend python manage.py check --database default
```

---

## 📊 Monitoramento

### Logs em tempo real

```bash
# Todos os serviços
docker-compose -f docker-compose.prod.yml logs -f

# Apenas backend
docker-compose -f docker-compose.prod.yml logs -f backend

# Últimas 100 linhas
docker-compose -f docker-compose.prod.yml logs --tail=100
```

### Status dos serviços

```bash
# Ver containers rodando
docker-compose -f docker-compose.prod.yml ps

# Ver uso de recursos
docker stats

# Health check
curl http://localhost:8000/health/
```

### Backups

```bash
# Ver backups disponíveis
ls -lh /opt/crm-solar/.backup/

# Criar backup manual
cd /opt/crm-solar
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U postgres crm_solar > .backup/db_manual_$(date +%Y%m%d_%H%M%S).sql
```

---

## 🎯 Checklist de Deploy

### Antes do Deploy

- [ ] Testes passando localmente
- [ ] Código revisado (code review)
- [ ] Variáveis de ambiente atualizadas
- [ ] Backup recente disponível
- [ ] Comunicar equipe sobre deploy

### Durante o Deploy

- [ ] Monitorar logs do GitHub Actions
- [ ] Verificar health checks
- [ ] Testar funcionalidades críticas

### Após o Deploy

- [ ] Verificar aplicação no navegador
- [ ] Testar login e funcionalidades principais
- [ ] Verificar logs por erros
- [ ] Confirmar backup foi criado
- [ ] Comunicar sucesso do deploy

---

## 📞 Suporte

Em caso de problemas críticos:

1. **Rollback imediato** via GitHub Actions
2. Verificar logs: `docker-compose logs`
3. Restaurar backup se necessário
4. Documentar o incidente

---

## 🔄 Atualizações Futuras

### Adicionar notificações (Slack/Discord)

```yaml
# Adicionar ao final dos workflows
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Adicionar testes de carga

```yaml
- name: Load test
  run: |
    docker run --rm -i grafana/k6 run - < loadtest.js
```

### Adicionar análise de código

```yaml
- name: SonarQube Scan
  uses: sonarsource/sonarqube-scan-action@master
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

---

**Documentação criada em:** $(date)
**Versão:** 1.0.0
