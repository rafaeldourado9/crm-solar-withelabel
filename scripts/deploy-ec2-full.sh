#!/bin/bash
set -e

echo "🚀 Deploy CRM Solar - EC2 Completo com Docker"
echo "=============================================="

# Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt-get update -qq
sudo apt-get upgrade -y -qq

# Instalar Docker
if ! command -v docker &> /dev/null; then
    echo "🐳 Instalando Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo systemctl enable docker
    sudo systemctl start docker
    sudo usermod -aG docker ubuntu
    rm get-docker.sh
else
    echo "✅ Docker já instalado"
fi

# Instalar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "🐳 Instalando Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
else
    echo "✅ Docker Compose já instalado"
fi

# Instalar Git
sudo apt-get install -y git

# Clonar repositório
REPO_DIR="/opt/crm-solar"
if [ ! -d "$REPO_DIR" ]; then
    echo "📥 Clonando repositório..."
    sudo git clone https://github.com/YOUR_REPO/SunOps---SaaS.git $REPO_DIR
else
    echo "🔄 Atualizando repositório..."
    cd $REPO_DIR
    sudo git pull origin main
fi

cd $REPO_DIR

# Criar .env para produção (PostgreSQL no Docker)
echo "⚙️  Configurando variáveis de ambiente..."
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

SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
EOF

# Parar containers antigos
echo "🛑 Parando containers antigos..."
sudo docker-compose down || true

# Limpar volumes antigos (opcional)
# sudo docker volume prune -f

# Subir todos os serviços
echo "🚀 Iniciando todos os serviços..."
sudo docker-compose up -d --build

# Aguardar serviços iniciarem
echo "⏳ Aguardando serviços iniciarem (30s)..."
sleep 30

# Executar migrações
echo "🗄️  Executando migrações..."
sudo docker-compose exec -T backend python manage.py migrate

# Verificar equipamentos
echo "📦 Verificando equipamentos..."
sudo docker-compose exec -T backend python verificar_equipamentos.py

# Coletar arquivos estáticos
echo "📦 Coletando arquivos estáticos..."
sudo docker-compose exec -T backend python manage.py collectstatic --noinput

# Criar superuser
echo "👤 Criando superuser..."
sudo docker-compose exec -T backend python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@crm.com', 'Admin@123456')
    print('✅ Superuser criado: admin/Admin@123456')
else:
    print('✅ Superuser já existe')
PYEOF

# Configurar monitoramento
echo "📊 Configurando monitoramento..."
sudo cp scripts/crm-solar-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable crm-solar-monitor
sudo systemctl start crm-solar-monitor

# Status final
echo ""
echo "=============================================="
echo "✅ Deploy concluído com sucesso!"
echo "=============================================="
echo ""
echo "📊 Status dos containers:"
sudo docker-compose ps
echo ""
echo "🌐 Acesse:"
echo "   Frontend: http://$(curl -s ifconfig.me)"
echo "   Admin: http://$(curl -s ifconfig.me)/admin"
echo "   Health: http://$(curl -s ifconfig.me)/health/"
echo ""
echo "👤 Credenciais:"
echo "   User: admin"
echo "   Pass: Admin@123456"
echo ""
echo "📝 Comandos úteis:"
echo "   Logs: sudo docker-compose logs -f"
echo "   Restart: sudo docker-compose restart"
echo "   Stop: sudo docker-compose down"
echo ""
