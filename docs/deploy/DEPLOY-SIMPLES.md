# DEPLOY SIMPLES - SEM AWS CLI

## Você tem:
- Instance ID: i-07a9e55abd9e8a7be
- Região: us-east-1

## PASSO 1: Obter IP do EC2

Acesse: https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#Instances:instanceId=i-07a9e55abd9e8a7be

Copie o **Public IPv4 address**

## PASSO 2: Liberar portas

1. Na mesma página, clique na aba **Security**
2. Clique no **Security group**
3. Clique em **Edit inbound rules**
4. Adicione:
   - Type: HTTP, Port: 80, Source: 0.0.0.0/0
   - Type: HTTPS, Port: 443, Source: 0.0.0.0/0
   - Type: SSH, Port: 22, Source: 0.0.0.0/0
5. Salve

## PASSO 3: Conectar via SSH

Você precisa da chave .pem da instância.

```bash
ssh -i sua-chave.pem ubuntu@SEU-IP-AQUI
```

## PASSO 4: Deploy no EC2

Cole estes comandos no terminal SSH:

```bash
# Atualizar sistema
sudo apt-get update
sudo apt-get install -y git curl

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clonar repositório
sudo git clone https://github.com/SEU-USUARIO/SunOps---SaaS.git /opt/crm-solar
cd /opt/crm-solar

# Criar .env
sudo tee .env > /dev/null << EOF
SECRET_KEY=$(openssl rand -base64 32)
DEBUG=False
ALLOWED_HOSTS=*
DB_NAME=crm_solar
DB_USER=postgres
DB_PASSWORD=$(openssl rand -base64 16)
DB_HOST=db
DB_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
CORS_ORIGINS=http://$(curl -s ifconfig.me)
EOF

# Deploy
sudo docker-compose up -d --build

# Aguardar 30 segundos
sleep 30

# Migrações
sudo docker-compose exec -T backend python manage.py migrate
sudo docker-compose exec -T backend python verificar_equipamentos.py

# Criar admin
sudo docker-compose exec -T backend python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@crm.com', 'Admin@123456')
PYEOF

echo "Deploy concluído!"
```

## PASSO 5: Acessar

```
http://SEU-IP
http://SEU-IP/admin

User: admin
Pass: Admin@123456
```

## Tempo total: ~10 minutos
