# 🚀 Deploy Completo - CI/CD + Terraform

## ⚡ Setup Rápido (20 minutos)

### 1️⃣ Criar Infraestrutura AWS com Terraform

```bash
cd terraform

# Inicializar Terraform
terraform init

# Criar ambiente DEV
terraform workspace new dev
terraform plan -var-file="dev.tfvars" -var="db_password=SENHA_FORTE"
terraform apply -var-file="dev.tfvars" -var="db_password=SENHA_FORTE"

# Criar ambiente PROD
terraform workspace new prod
terraform plan -var-file="prod.tfvars" -var="db_password=SENHA_FORTE"
terraform apply -var-file="prod.tfvars" -var="db_password=SENHA_FORTE"

# Ver outputs
terraform output
```

### 2️⃣ Configurar Secrets no GitHub

Vá em: `Settings > Secrets and variables > Actions > New repository secret`

```
DEV_HOST=<IP do servidor DEV>
PROD_HOST=<IP do servidor PROD>
SSH_PRIVATE_KEY=<conteúdo da chave privada>
```

### 3️⃣ Configurar Servidores

```bash
# SSH no servidor DEV
ssh -i sunops-key.pem ubuntu@DEV_IP

# Clonar repositório
git clone https://github.com/seu-usuario/sunops.git /home/ubuntu/sunops
cd /home/ubuntu/sunops

# Configurar .env
cp .env.example .env.dev
nano .env.dev  # Editar com dados do Terraform output

# Gerar SSL
sudo certbot certonly --standalone -d dev.sunops.com.br
sudo cp /etc/letsencrypt/live/dev.sunops.com.br/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/dev.sunops.com.br/privkey.pem nginx/ssl/

# Repetir para PROD
```

### 4️⃣ Primeiro Deploy Manual

```bash
# No servidor
cd /home/ubuntu/sunops

# Login no GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u seu-usuario --password-stdin

# Subir aplicação
docker-compose -f docker-compose.prod.yml up -d

# Migrations
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

---

## 🔄 Fluxo de CI/CD

### Deploy Automático

```bash
# Deploy para DEV
git checkout develop
git add .
git commit -m "feat: nova funcionalidade"
git push origin develop
# ✅ Deploy automático em DEV

# Deploy para PROD
git checkout main
git merge develop
git push origin main
# ✅ Testes + Deploy automático em PROD
```

### Rollback Manual

```bash
# Via GitHub Actions
# 1. Ir em Actions > Rollback PROD > Run workflow
# 2. Informar commit SHA (ou deixar vazio para versão anterior)
# 3. Confirmar

# Via SSH no servidor
ssh ubuntu@PROD_IP
cd /home/ubuntu/sunops
./scripts/rollback.sh  # Versão anterior
# ou
./scripts/rollback.sh abc123def  # Commit específico
```

---

## 📊 Workflows Disponíveis

### 1. CI - Tests (`.github/workflows/ci.yml`)
- **Trigger**: Push/PR em `develop` ou `main`
- **Ações**:
  - Testa backend (Django)
  - Testa frontend (React)
  - Build de validação

### 2. Deploy DEV (`.github/workflows/deploy-dev.yml`)
- **Trigger**: Push em `develop`
- **Ações**:
  - Build de imagens Docker
  - Push para GitHub Container Registry
  - Deploy em servidor DEV
  - Migrations automáticas
  - Health check

### 3. Deploy PROD (`.github/workflows/deploy-prod.yml`)
- **Trigger**: Push em `main`
- **Ações**:
  - Roda todos os testes (obrigatório)
  - Build de imagens Docker
  - Backup automático do banco
  - Deploy em servidor PROD
  - Migrations automáticas
  - Health check
  - Rollback automático se falhar

### 4. Rollback (`.github/workflows/rollback.yml`)
- **Trigger**: Manual
- **Ações**:
  - Backup de emergência
  - Rollback para versão anterior ou commit específico
  - Health check
  - Notificação

---

## 🏗️ Infraestrutura Terraform

### Recursos Criados

**Rede:**
- VPC com subnets públicas e privadas
- Internet Gateway
- Route Tables

**Compute:**
- EC2 t3.micro (DEV + PROD)
- Elastic IP
- Security Groups

**Database:**
- RDS PostgreSQL t3.micro
- Backup automático (7 dias em PROD)
- Multi-subnet

**Storage:**
- S3 para arquivos
- S3 para backups (lifecycle para Glacier)

**Custo estimado:** ~$33/mês

### Comandos Úteis

```bash
# Ver recursos criados
terraform state list

# Ver detalhes de um recurso
terraform state show aws_instance.app

# Destruir ambiente (cuidado!)
terraform destroy -var-file="dev.tfvars"

# Atualizar infraestrutura
terraform plan -var-file="prod.tfvars"
terraform apply -var-file="prod.tfvars"
```

---

## 🔐 Segurança

### Secrets Necessários

```bash
# GitHub Secrets
DEV_HOST=1.2.3.4
PROD_HOST=5.6.7.8
SSH_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----...

# .env.prod (no servidor)
DEBUG=False
SECRET_KEY=chave-super-secreta-aqui
DATABASE_URL=postgresql://user:pass@host:5432/db
AWS_ACCESS_KEY_ID=AKIAXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxx
```

### Gerar Chave SSH

```bash
# Local
ssh-keygen -t rsa -b 4096 -f sunops-key
# Adicionar chave pública no AWS EC2
# Adicionar chave privada no GitHub Secrets
```

---

## 📈 Monitoramento

### Health Checks

```bash
# DEV
curl https://dev.sunops.com.br/health/

# PROD
curl https://sunops.com.br/health/
```

### Logs

```bash
# Ver logs dos containers
docker-compose -f docker-compose.prod.yml logs -f

# Logs específicos
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

### Backup Manual

```bash
# No servidor
cd /home/ubuntu/sunops
./scripts/backup.sh

# Restaurar backup
./scripts/restore.sh 20240123_030000
```

---

## 🎯 Checklist de Deploy

- [ ] Criar infraestrutura com Terraform
- [ ] Configurar DNS (Route53 ou outro)
- [ ] Adicionar secrets no GitHub
- [ ] Configurar servidores (SSH + Docker)
- [ ] Gerar certificados SSL
- [ ] Fazer primeiro deploy manual
- [ ] Testar CI/CD (push para develop)
- [ ] Testar rollback
- [ ] Configurar backup automático (cron)
- [ ] Documentar credenciais

---

## 🆘 Troubleshooting

### Deploy falhou

```bash
# Ver logs do GitHub Actions
# Ir em Actions > Ver workflow com erro

# SSH no servidor e verificar
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs
```

### Rollback não funciona

```bash
# Verificar backups disponíveis
ls -lh /home/ubuntu/sunops/backups/

# Rollback manual
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

### Banco de dados com problema

```bash
# Conectar no RDS
psql -h <RDS_ENDPOINT> -U sunops -d sunops

# Restaurar backup
./scripts/restore.sh <BACKUP_DATE>
```

---

## 📞 Suporte

- **Documentação AWS**: https://docs.aws.amazon.com/
- **Terraform Docs**: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- **GitHub Actions**: https://docs.github.com/actions

---

## 🎉 Pronto!

Agora você tem:
- ✅ CI/CD completo
- ✅ 2 ambientes (DEV + PROD)
- ✅ Testes automáticos
- ✅ Deploy automático
- ✅ Rollback em 1 clique
- ✅ Backup automático
- ✅ Infraestrutura como código

**Tempo total de setup: ~20 minutos** ⚡
