# ⚡ DEPLOY AWS EM 10 MINUTOS

## 1️⃣ CRIAR RDS (3 min)
```bash
# AWS Console > RDS > Create Database
- Engine: PostgreSQL 15
- Template: Free tier
- DB instance: db.t3.micro
- DB name: crm_solar_dev
- Master username: postgres
- Master password: [ANOTE AQUI]
- Public access: NO
- Security group: [ANOTE O ID]
```

## 2️⃣ CRIAR EC2 SPOT (2 min)
```bash
# AWS Console > EC2 > Launch Instance
- Name: crm-solar-dev
- AMI: Ubuntu 22.04 LTS
- Instance type: t3.medium
- Request Spot Instance: YES
- Key pair: [Criar ou usar existente]
- Security Group:
  * SSH (22) - Seu IP
  * HTTP (80) - 0.0.0.0/0
  * HTTPS (443) - 0.0.0.0/0
```

## 3️⃣ CONFIGURAR SECURITY GROUPS (1 min)
```bash
# RDS Security Group > Inbound Rules
- Type: PostgreSQL (5432)
- Source: EC2 Security Group ID
```

## 4️⃣ CONECTAR E INSTALAR (4 min)
```bash
# SSH na EC2
ssh -i sua-chave.pem ubuntu@SEU-EC2-IP

# Executar comandos
sudo apt update && sudo apt install -y docker.io docker-compose git
sudo systemctl start docker
sudo systemctl enable docker

# Clonar repo
git clone -b dev https://github.com/SEU-USUARIO/SunOps---SaaS.git /opt/crm-solar
cd /opt/crm-solar

# Criar .env.dev
cat > .env.dev << EOF
SECRET_KEY=$(openssl rand -base64 32)
DEBUG=False
ALLOWED_HOSTS=SEU-EC2-IP

DB_NAME=crm_solar_dev
DB_USER=postgres
DB_PASSWORD=SUA-SENHA-RDS
DB_HOST=SEU-RDS-ENDPOINT.rds.amazonaws.com
DB_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379

CORS_ORIGINS=http://SEU-EC2-IP
EOF

# Deploy
sudo docker-compose -f docker-compose.dev.yml up -d --build

# Aguardar 2 min e executar
sudo docker-compose -f docker-compose.dev.yml exec -T backend python manage.py migrate
sudo docker-compose -f docker-compose.dev.yml exec -T backend python verificar_equipamentos.py
sudo docker-compose -f docker-compose.dev.yml exec -T backend python manage.py createsuperuser

# Configurar monitoramento automático
sudo cp scripts/crm-solar-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable crm-solar-monitor
sudo systemctl start crm-solar-monitor
```

## 🆘 MONITORAMENTO
```bash
# Ver logs do monitor
sudo journalctl -u crm-solar-monitor -f

# Status do monitor
sudo systemctl status crm-solar-monitor

# Health check manual
curl http://localhost/health/
```

## ✅ ACESSAR
```
http://SEU-EC2-IP
http://SEU-EC2-IP/admin
```

## 🆘 SE DER ERRO
```bash
# Ver logs
sudo docker-compose -f docker-compose.dev.yml logs -f

# Reiniciar
sudo docker-compose -f docker-compose.dev.yml restart
```

## 📋 CHECKLIST
- [ ] RDS criado e acessível
- [ ] EC2 rodando
- [ ] Security Groups configurados
- [ ] .env.dev com credenciais corretas
- [ ] Containers rodando
- [ ] Migrações aplicadas
- [ ] Equipamentos carregados
- [ ] Superuser criado
