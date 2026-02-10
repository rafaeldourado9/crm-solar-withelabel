# Deploy AWS - CRM Solar

## 🎯 Arquitetura DEV (1 Cliente)

```
EC2 Spot (t3.medium)
├── Docker Compose
│   ├── Backend (Django + Gunicorn)
│   ├── Frontend (React + Nginx)
│   └── Nginx (Reverse Proxy)
└── RDS PostgreSQL (db.t3.micro)
```

## 📋 Pré-requisitos

1. Conta AWS configurada
2. Chave SSH criada
3. Security Groups configurados
4. RDS PostgreSQL criado

## 🚀 Deploy Rápido

### 1. Criar RDS PostgreSQL

```bash
# Via AWS Console ou CLI
aws rds create-db-instance \
  --db-instance-identifier crm-solar-dev \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username postgres \
  --master-user-password YOUR_PASSWORD \
  --allocated-storage 20 \
  --backup-retention-period 7 \
  --publicly-accessible false
```

### 2. Criar EC2 Spot Instance

```bash
# Ubuntu 22.04 LTS
# t3.medium (2 vCPU, 4GB RAM)
# Security Group: 80, 443, 22
```

### 3. Conectar e Instalar

```bash
# SSH na instância
ssh -i your-key.pem ubuntu@your-ec2-ip

# Baixar e executar script
sudo su
curl -fsSL https://raw.githubusercontent.com/YOUR_REPO/main/scripts/deploy-dev.sh -o deploy-dev.sh
chmod +x deploy-dev.sh
./deploy-dev.sh
```

### 4. Configurar .env.dev

```bash
cd /opt/crm-solar
nano .env.dev
```

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-ec2-ip,your-domain.com

DB_NAME=crm_solar_dev
DB_USER=postgres
DB_PASSWORD=your-rds-password
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379

CORS_ORIGINS=http://your-ec2-ip,https://your-domain.com

# Segurança
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### 5. Reiniciar

```bash
cd /opt/crm-solar
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d
```

## 🔒 Security Groups

### EC2 Security Group
```
Inbound:
- 80 (HTTP) - 0.0.0.0/0
- 443 (HTTPS) - 0.0.0.0/0
- 22 (SSH) - YOUR_IP/32

Outbound:
- All traffic
```

### RDS Security Group
```
Inbound:
- 5432 (PostgreSQL) - EC2_SECURITY_GROUP

Outbound:
- All traffic
```

## 📊 Monitoramento

```bash
# Logs em tempo real
docker-compose -f docker-compose.dev.yml logs -f

# Status
docker-compose -f docker-compose.dev.yml ps

# Uso de recursos
docker stats
```

## 🔄 Atualização

```bash
cd /opt/crm-solar
git pull origin dev
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml build --no-cache
docker-compose -f docker-compose.dev.yml up -d
```

## 💰 Custos Estimados (1 Cliente)

- EC2 Spot t3.medium: ~$15/mês
- RDS db.t3.micro: ~$15/mês
- Storage (20GB): ~$2/mês
- **Total: ~$32/mês**

## 🆘 Troubleshooting

### Backend não inicia
```bash
docker-compose -f docker-compose.dev.yml logs backend
docker-compose -f docker-compose.dev.yml exec backend python manage.py check
```

### Erro de conexão RDS
```bash
# Testar conexão
docker-compose -f docker-compose.dev.yml exec backend python manage.py dbshell
```

### Timeout nas requisições
```bash
# Verificar timeouts
grep -r "timeout" nginx/
grep -r "TIMEOUT" backend/config/settings.py
```

## 📝 Checklist Pós-Deploy

- [ ] Aplicação acessível via HTTP
- [ ] Login funcionando
- [ ] Dashboard carregando
- [ ] Backup RDS configurado
- [ ] Logs sendo gerados
- [ ] Rate limiting ativo
- [ ] SSL/TLS (se domínio configurado)
