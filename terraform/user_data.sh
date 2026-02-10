#!/bin/bash
set -e

# Logs
exec > >(tee /var/log/user-data.log)
exec 2>&1

echo "🚀 Iniciando deploy CRM Solar..."

# Atualizar sistema
apt-get update
apt-get upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
systemctl enable docker
systemctl start docker

# Instalar Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Clonar repositório
cd /opt
git clone -b dev https://github.com/YOUR_USERNAME/SunOps---SaaS.git crm-solar
cd crm-solar

# Criar .env.dev
cat > .env.dev << EOF
SECRET_KEY=$(openssl rand -base64 32)
DEBUG=False
ALLOWED_HOSTS=*

DB_NAME=crm_solar_${environment}
DB_USER=postgres
DB_PASSWORD=${db_password}
DB_HOST=${db_host}
DB_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379

CORS_ORIGINS=http://$(curl -s ifconfig.me)

SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
EOF

# Deploy
docker-compose -f docker-compose.dev.yml up -d --build

# Aguardar backend iniciar
sleep 30

# Executar migrações
docker-compose -f docker-compose.dev.yml exec -T backend python manage.py migrate
docker-compose -f docker-compose.dev.yml exec -T backend python verificar_equipamentos.py
docker-compose -f docker-compose.dev.yml exec -T backend python manage.py collectstatic --noinput

# Criar superuser
docker-compose -f docker-compose.dev.yml exec -T backend python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@sunops.com', 'Admin@123456')
PYEOF

# Configurar monitoramento
cp scripts/crm-solar-monitor.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable crm-solar-monitor
systemctl start crm-solar-monitor

echo "✅ Deploy concluído!"
echo "🌐 Acesse: http://$(curl -s ifconfig.me)"
