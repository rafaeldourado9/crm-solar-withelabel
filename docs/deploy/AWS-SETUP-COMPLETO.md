# 🚀 Setup Completo AWS + GitHub Actions - Passo a Passo

## 📋 Índice
1. [Criar Conta AWS](#1-criar-conta-aws)
2. [Criar VPC e Rede](#2-criar-vpc-e-rede)
3. [Criar RDS PostgreSQL](#3-criar-rds-postgresql)
4. [Criar EC2 (DEV e PROD)](#4-criar-ec2-dev-e-prod)
5. [Criar S3 para Mídia](#5-criar-s3-para-mídia)
6. [Criar CloudFront CDN](#6-criar-cloudfront-cdn)
7. [Configurar GitHub Actions](#7-configurar-github-actions)
8. [Deploy Inicial](#8-deploy-inicial)

---

## 1. Criar Conta AWS

### 1.1 Acessar AWS
```
1. Ir para: https://aws.amazon.com
2. Clicar em "Criar uma conta da AWS"
3. Preencher:
   - Email
   - Senha
   - Nome da conta AWS
4. Adicionar cartão de crédito (não será cobrado no free tier)
5. Verificar identidade (telefone)
6. Escolher plano: "Plano básico (gratuito)"
```

### 1.2 Fazer Login no Console
```
1. Ir para: https://console.aws.amazon.com
2. Login com email e senha
3. Região: Escolher "us-east-1" (N. Virginia) ou "sa-east-1" (São Paulo)
```

### 1.3 Criar Usuário IAM (Segurança)
```
1. Console AWS → Buscar "IAM" → IAM Dashboard
2. Users → Add users
3. User name: github-actions
4. Select AWS credential type: ✅ Access key - Programmatic access
5. Next: Permissions
6. Attach existing policies directly:
   ✅ AmazonEC2FullAccess
   ✅ AmazonRDSFullAccess
   ✅ AmazonS3FullAccess
   ✅ CloudFrontFullAccess
7. Next → Next → Create user
8. ⚠️ IMPORTANTE: Copiar e guardar:
   - Access key ID
   - Secret access key
   (Não será mostrado novamente!)
```

---

## 2. Criar VPC e Rede

### 2.1 Criar VPC
```
1. Console AWS → Buscar "VPC" → VPC Dashboard
2. Create VPC
3. Configurar:
   - Name: crm-solar-vpc
   - IPv4 CIDR: 10.0.0.0/16
4. Create VPC
```

### 2.2 Criar Subnets
```
1. VPC Dashboard → Subnets → Create subnet
2. VPC: crm-solar-vpc

SUBNET PÚBLICA 1:
- Name: crm-solar-public-1a
- Availability Zone: us-east-1a (ou sa-east-1a)
- IPv4 CIDR: 10.0.1.0/24
- Create subnet

SUBNET PÚBLICA 2:
- Name: crm-solar-public-1b
- Availability Zone: us-east-1b (ou sa-east-1b)
- IPv4 CIDR: 10.0.2.0/24
- Create subnet

SUBNET PRIVADA 1:
- Name: crm-solar-private-1a
- Availability Zone: us-east-1a
- IPv4 CIDR: 10.0.10.0/24
- Create subnet

SUBNET PRIVADA 2:
- Name: crm-solar-private-1b
- Availability Zone: us-east-1b
- IPv4 CIDR: 10.0.11.0/24
- Create subnet
```

### 2.3 Criar Internet Gateway
```
1. VPC Dashboard → Internet Gateways → Create internet gateway
2. Name: crm-solar-igw
3. Create → Actions → Attach to VPC → crm-solar-vpc
```

### 2.4 Criar Route Table
```
1. VPC Dashboard → Route Tables → Create route table
2. Name: crm-solar-public-rt
3. VPC: crm-solar-vpc
4. Create

5. Selecionar route table criada → Routes → Edit routes
6. Add route:
   - Destination: 0.0.0.0/0
   - Target: Internet Gateway → crm-solar-igw
7. Save changes

8. Subnet associations → Edit subnet associations
9. Selecionar: crm-solar-public-1a e crm-solar-public-1b
10. Save associations
```

---

## 3. Criar RDS PostgreSQL

### 3.1 Criar Subnet Group
```
1. Console AWS → Buscar "RDS" → RDS Dashboard
2. Subnet groups → Create DB subnet group
3. Configurar:
   - Name: crm-solar-db-subnet
   - Description: Subnets for CRM Solar database
   - VPC: crm-solar-vpc
   - Add subnets:
     ✅ crm-solar-private-1a
     ✅ crm-solar-private-1b
4. Create
```

### 3.2 Criar Security Group para RDS
```
1. Console AWS → EC2 → Security Groups → Create security group
2. Configurar:
   - Name: crm-solar-rds-sg
   - Description: Security group for RDS
   - VPC: crm-solar-vpc
3. Inbound rules → Add rule:
   - Type: PostgreSQL
   - Port: 5432
   - Source: Custom → 10.0.0.0/16 (toda VPC)
4. Create security group
```

### 3.3 Criar RDS PostgreSQL
```
1. RDS Dashboard → Databases → Create database
2. Configurar:

ENGINE:
- Engine type: PostgreSQL
- Version: PostgreSQL 15.x
- Templates: ✅ Free tier (ou Production para PROD)

SETTINGS:
- DB instance identifier: crm-solar-db-prod
- Master username: postgres
- Master password: [SENHA FORTE - GUARDAR!]
- Confirm password: [MESMA SENHA]

INSTANCE:
- DB instance class: db.t3.micro (free tier) ou db.t3.small (prod)
- Storage type: General Purpose SSD (gp3)
- Allocated storage: 20 GB

CONNECTIVITY:
- VPC: crm-solar-vpc
- Subnet group: crm-solar-db-subnet
- Public access: No
- VPC security group: crm-solar-rds-sg
- Availability Zone: No preference

DATABASE OPTIONS:
- Initial database name: crm_solar
- Port: 5432

BACKUP:
- Enable automated backups: Yes
- Backup retention period: 7 days

3. Create database

4. ⏳ Aguardar ~10 minutos até status "Available"

5. Copiar endpoint:
   - Databases → crm-solar-db-prod → Connectivity & security
   - Endpoint: crm-solar-db-prod.xxxxx.us-east-1.rds.amazonaws.com
   - ⚠️ GUARDAR ESTE ENDPOINT!
```

---

## 4. Criar EC2 (DEV e PROD)

### 4.1 Criar Security Group para EC2
```
1. EC2 Dashboard → Security Groups → Create security group
2. Configurar:
   - Name: crm-solar-ec2-sg
   - Description: Security group for EC2 instances
   - VPC: crm-solar-vpc

3. Inbound rules → Add rules:
   
   SSH:
   - Type: SSH
   - Port: 22
   - Source: My IP (seu IP atual)
   
   HTTP:
   - Type: HTTP
   - Port: 80
   - Source: Anywhere IPv4 (0.0.0.0/0)
   
   HTTPS:
   - Type: HTTPS
   - Port: 443
   - Source: Anywhere IPv4 (0.0.0.0/0)
   
   Backend:
   - Type: Custom TCP
   - Port: 8000
   - Source: Anywhere IPv4 (0.0.0.0/0)

4. Create security group
```

### 4.2 Criar Key Pair
```
1. EC2 Dashboard → Key Pairs → Create key pair
2. Configurar:
   - Name: crm-solar-key
   - Key pair type: RSA
   - Private key format: .pem
3. Create key pair
4. ⚠️ Arquivo .pem será baixado automaticamente
5. ⚠️ GUARDAR EM LOCAL SEGURO!

6. No seu PC (Linux/Mac):
   chmod 400 ~/Downloads/crm-solar-key.pem
   mv ~/Downloads/crm-solar-key.pem ~/.ssh/

7. No Windows:
   - Mover para C:\Users\SEU_USUARIO\.ssh\
```

### 4.3 Criar EC2 DEV
```
1. EC2 Dashboard → Instances → Launch instances

NAME:
- Name: crm-solar-dev

AMI:
- Ubuntu Server 22.04 LTS (Free tier eligible)

INSTANCE TYPE:
- t2.small (2 vCPU, 2GB RAM) ou t2.micro (free tier)

KEY PAIR:
- crm-solar-key

NETWORK:
- VPC: crm-solar-vpc
- Subnet: crm-solar-public-1a
- Auto-assign public IP: Enable

SECURITY GROUP:
- Select existing: crm-solar-ec2-sg

STORAGE:
- 20 GB gp3

ADVANCED DETAILS → User data:
```
```bash
#!/bin/bash
apt-get update
apt-get install -y docker.io docker-compose git curl
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu
mkdir -p /opt/crm-solar/.backup
chown -R ubuntu:ubuntu /opt/crm-solar
```
```
2. Launch instance

3. ⏳ Aguardar status "Running"

4. Copiar:
   - Public IPv4 address: 54.xxx.xxx.xxx
   - ⚠️ GUARDAR ESTE IP!
```

### 4.4 Criar EC2 PROD
```
Repetir passos 4.3, mas:
- Name: crm-solar-prod
- Instance type: t2.medium (2 vCPU, 4GB RAM) ou maior
- Storage: 30 GB gp3
- Subnet: crm-solar-public-1b

⚠️ GUARDAR O IP PÚBLICO!
```

### 4.5 Testar Conexão SSH
```bash
# DEV
ssh -i ~/.ssh/crm-solar-key.pem ubuntu@IP_DO_EC2_DEV

# PROD
ssh -i ~/.ssh/crm-solar-key.pem ubuntu@IP_DO_EC2_PROD

# Se conectou, está OK! Digite 'exit' para sair
```

---

## 5. Criar S3 para Mídia

### 5.1 Criar Bucket S3
```
1. Console AWS → Buscar "S3" → S3 Dashboard
2. Create bucket

BUCKET NAME:
- Bucket name: crm-solar-media-[SEU-NOME-UNICO]
  (exemplo: crm-solar-media-empresa123)

REGION:
- AWS Region: us-east-1 (mesma do EC2)

OBJECT OWNERSHIP:
- ACLs disabled

BLOCK PUBLIC ACCESS:
- ⚠️ DESMARCAR "Block all public access"
- ✅ Confirmar que entende os riscos

VERSIONING:
- Enable (opcional, mas recomendado)

3. Create bucket
```

### 5.2 Configurar Bucket Policy
```
1. S3 → Buckets → crm-solar-media-xxx
2. Permissions → Bucket policy → Edit
3. Colar:
```
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::crm-solar-media-SEU-BUCKET/*"
        }
    ]
}
```
```
⚠️ Substituir "crm-solar-media-SEU-BUCKET" pelo nome real do seu bucket!

4. Save changes
```

### 5.3 Configurar CORS
```
1. Permissions → Cross-origin resource sharing (CORS) → Edit
2. Colar:
```
```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": ["ETag"]
    }
]
```
```
3. Save changes
```

---

## 6. Criar CloudFront CDN

### 6.1 Criar Distribuição CloudFront
```
1. Console AWS → Buscar "CloudFront" → CloudFront Dashboard
2. Create distribution

ORIGIN:
- Origin domain: crm-solar-media-xxx.s3.us-east-1.amazonaws.com
- Name: S3-crm-solar-media
- Origin access: Public

DEFAULT CACHE BEHAVIOR:
- Viewer protocol policy: Redirect HTTP to HTTPS
- Allowed HTTP methods: GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE
- Cache policy: CachingOptimized

SETTINGS:
- Price class: Use only North America and Europe (mais barato)
- Alternate domain name (CNAME): cdn.seudominio.com (opcional)
- Custom SSL certificate: Default CloudFront Certificate

3. Create distribution

4. ⏳ Aguardar status "Deployed" (~15 minutos)

5. Copiar:
   - Distribution domain name: d111111abcdef8.cloudfront.net
   - ⚠️ GUARDAR ESTE DOMÍNIO!
```

---

## 7. Configurar GitHub Actions

### 7.1 Preparar Chaves SSH para GitHub
```bash
# No seu PC local

# Gerar chave para DEV
ssh-keygen -t ed25519 -C "github-actions-dev" -f ~/.ssh/github_crm_dev
# Pressionar Enter 3x (sem senha)

# Gerar chave para PROD
ssh-keygen -t ed25519 -C "github-actions-prod" -f ~/.ssh/github_crm_prod
# Pressionar Enter 3x (sem senha)

# Copiar chaves públicas para os servidores
ssh-copy-id -i ~/.ssh/github_crm_dev.pub -o "IdentityFile ~/.ssh/crm-solar-key.pem" ubuntu@IP_DO_EC2_DEV

ssh-copy-id -i ~/.ssh/github_crm_prod.pub -o "IdentityFile ~/.ssh/crm-solar-key.pem" ubuntu@IP_DO_EC2_PROD

# Testar
ssh -i ~/.ssh/github_crm_dev ubuntu@IP_DO_EC2_DEV
ssh -i ~/.ssh/github_crm_prod ubuntu@IP_DO_EC2_PROD
```

### 7.2 Configurar Secrets no GitHub
```
1. GitHub → Seu repositório → Settings
2. Secrets and variables → Actions
3. New repository secret

Adicionar os seguintes secrets:
```

**Secrets AWS:**
```
AWS_ACCESS_KEY_ID
Valor: [Access key do usuário IAM criado no passo 1.3]

AWS_SECRET_ACCESS_KEY
Valor: [Secret access key do usuário IAM]

AWS_REGION
Valor: us-east-1
```

**Secrets DEV:**
```
DEV_SSH_KEY
Valor: [Conteúdo completo de ~/.ssh/github_crm_dev]
# Para ver: cat ~/.ssh/github_crm_dev

DEV_HOST
Valor: [IP público do EC2 DEV]

DEV_USER
Valor: ubuntu

DEV_DB_HOST
Valor: [Endpoint do RDS copiado no passo 3.3]

DEV_DB_PASSWORD
Valor: [Senha do RDS criada no passo 3.3]
```

**Secrets PROD:**
```
PROD_SSH_KEY
Valor: [Conteúdo completo de ~/.ssh/github_crm_prod]
# Para ver: cat ~/.ssh/github_crm_prod

PROD_HOST
Valor: [IP público do EC2 PROD]

PROD_USER
Valor: ubuntu

PROD_DB_HOST
Valor: [Endpoint do RDS copiado no passo 3.3]

PROD_DB_PASSWORD
Valor: [Senha do RDS criada no passo 3.3]
```

**Secrets S3/CloudFront:**
```
S3_BUCKET_NAME
Valor: crm-solar-media-[SEU-BUCKET]

CLOUDFRONT_DOMAIN
Valor: [Domain do CloudFront copiado no passo 6.1]
```

**Secrets Aplicação:**
```
DJANGO_SECRET_KEY
Valor: [Gerar com comando abaixo]

GOOGLE_MAPS_API_KEY
Valor: [Sua chave do Google Maps - opcional]
```

**Gerar Django Secret Key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 7.3 Configurar Environments
```
1. GitHub → Settings → Environments
2. New environment

ENVIRONMENT: development
- Sem proteções
- Add secret (environment-specific):
  DJANGO_DEBUG=False
  ALLOWED_HOSTS=IP_DO_EC2_DEV

ENVIRONMENT: production
- ✅ Required reviewers: [Seu usuário]
- ✅ Wait timer: 5 minutes
- ✅ Deployment branches: Only protected branches
- Add secret (environment-specific):
  DJANGO_DEBUG=False
  ALLOWED_HOSTS=IP_DO_EC2_PROD,seudominio.com
```

---

## 8. Deploy Inicial

### 8.1 Preparar Servidores

**Conectar ao EC2 DEV:**
```bash
ssh -i ~/.ssh/crm-solar-key.pem ubuntu@IP_DO_EC2_DEV
```

**Executar no servidor:**
```bash
# Verificar Docker
docker --version
docker-compose --version

# Se não estiver instalado:
sudo apt-get update
sudo apt-get install -y docker.io docker-compose git curl
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# Logout e login novamente
exit
ssh -i ~/.ssh/crm-solar-key.pem ubuntu@IP_DO_EC2_DEV

# Criar estrutura
sudo mkdir -p /opt/crm-solar/.backup
sudo chown -R ubuntu:ubuntu /opt/crm-solar
cd /opt/crm-solar

# Clonar repositório
git clone https://github.com/SEU_USUARIO/SunOps---SaaS.git .
git checkout dev

# Criar .env
cat > .env << 'EOF'
# Django
SECRET_KEY=sua-secret-key-aqui
DEBUG=False
ALLOWED_HOSTS=IP_DO_EC2_DEV,localhost

# Database (RDS)
DB_NAME=crm_solar
DB_USER=postgres
DB_PASSWORD=SENHA_DO_RDS_AQUI
DB_HOST=ENDPOINT_DO_RDS_AQUI
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# CORS
CORS_ORIGINS=http://IP_DO_EC2_DEV

# S3
AWS_ACCESS_KEY_ID=sua-access-key
AWS_SECRET_ACCESS_KEY=sua-secret-key
AWS_STORAGE_BUCKET_NAME=crm-solar-media-xxx
AWS_S3_REGION_NAME=us-east-1

# CloudFront
CLOUDFRONT_DOMAIN=d111111abcdef8.cloudfront.net

# GitHub (para CI/CD)
GITHUB_REPOSITORY=seu-usuario/SunOps---SaaS
IMAGE_TAG=dev-latest
EOF

# Editar .env com valores reais
nano .env

# Iniciar aplicação
docker-compose -f docker-compose.prod.yml up -d

# Aguardar containers iniciarem
sleep 30

# Executar migrações
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Criar superusuário
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

# Verificar
docker-compose -f docker-compose.prod.yml ps
curl http://localhost:8000/health/
```

**Repetir para EC2 PROD:**
```bash
ssh -i ~/.ssh/crm-solar-key.pem ubuntu@IP_DO_EC2_PROD
# Executar os mesmos comandos, mas:
# - git checkout prod
# - Usar IP_DO_EC2_PROD no .env
# - IMAGE_TAG=prod-latest
```

### 8.2 Testar Aplicação
```
1. Abrir navegador:
   - DEV: http://IP_DO_EC2_DEV
   - Backend DEV: http://IP_DO_EC2_DEV:8000/admin

2. Fazer login com superusuário criado

3. Se funcionar, está OK! ✅
```

### 8.3 Primeiro Deploy via GitHub Actions
```bash
# No seu PC local
cd /caminho/para/SunOps---SaaS

# Fazer uma alteração simples
echo "# Deploy test" >> README.md

# Commit e push para DEV
git checkout dev
git add .
git commit -m "test: primeiro deploy automatizado"
git push origin dev

# Acompanhar no GitHub
# GitHub → Actions → Deploy DEV
# Deve executar automaticamente

# Se passar, testar PROD
git checkout prod
git merge dev
git push origin prod

# GitHub → Actions → Deploy PROD
# Clicar em "Review deployments" → Approve
```

---

## ✅ Checklist Final

### Infraestrutura AWS
- [ ] Conta AWS criada
- [ ] Usuário IAM criado com access keys
- [ ] VPC criada com subnets públicas e privadas
- [ ] Internet Gateway e Route Table configurados
- [ ] RDS PostgreSQL criado e acessível
- [ ] EC2 DEV criado e rodando
- [ ] EC2 PROD criado e rodando
- [ ] Security Groups configurados
- [ ] Key Pair criado e guardado
- [ ] S3 Bucket criado e público
- [ ] CloudFront distribuição criada

### GitHub
- [ ] Todos os secrets configurados
- [ ] Environments (development e production) criados
- [ ] Chaves SSH copiadas para servidores
- [ ] Workflows funcionando

### Servidores
- [ ] Docker instalado em ambos EC2
- [ ] Aplicação clonada e rodando
- [ ] Banco de dados migrado
- [ ] Superusuário criado
- [ ] Health check respondendo
- [ ] Backups configurados

### Testes
- [ ] Deploy DEV automático funciona
- [ ] Deploy PROD com aprovação funciona
- [ ] Rollback funciona
- [ ] Aplicação acessível via navegador
- [ ] Upload de arquivos funciona (S3)
- [ ] CDN servindo arquivos (CloudFront)

---

## 💰 Custos Estimados (Mensal)

```
FREE TIER (Primeiro ano):
- EC2 t2.micro: GRÁTIS (750h/mês)
- RDS db.t3.micro: GRÁTIS (750h/mês)
- S3: GRÁTIS (5GB)
- CloudFront: GRÁTIS (50GB transferência)

APÓS FREE TIER:
- EC2 t2.small (DEV): ~$17/mês
- EC2 t2.medium (PROD): ~$34/mês
- RDS db.t3.small: ~$25/mês
- S3 (20GB): ~$0.50/mês
- CloudFront (100GB): ~$8/mês
- Total: ~$85/mês

PRODUÇÃO REAL:
- EC2 t3.large (PROD): ~$68/mês
- RDS db.t3.medium: ~$50/mês
- Load Balancer: ~$16/mês
- Total: ~$150-200/mês
```

---

## 📞 Próximos Passos

1. **Configurar Domínio:**
   - Comprar domínio (Route 53 ou outro)
   - Apontar para IPs dos EC2
   - Configurar SSL (Let's Encrypt)

2. **Melhorias:**
   - Adicionar Load Balancer
   - Configurar Auto Scaling
   - Adicionar CloudWatch para monitoramento
   - Configurar backups automáticos

3. **Segurança:**
   - Habilitar MFA na conta AWS
   - Rotacionar access keys periodicamente
   - Configurar AWS WAF
   - Habilitar CloudTrail

---

**Pronto! Sua infraestrutura AWS + CI/CD está completa! 🎉**
