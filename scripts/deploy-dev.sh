#!/bin/bash
set -e

echo "🚀 Deploy CRM Solar - DEV Environment"
echo "======================================"

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Execute como root: sudo bash deploy-dev.sh"
    exit 1
fi

# 1. Atualizar sistema
echo "📦 Atualizando sistema..."
apt-get update -qq
apt-get upgrade -y -qq

# 2. Instalar Docker
if ! command -v docker &> /dev/null; then
    echo "🐳 Instalando Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl enable docker
    systemctl start docker
else
    echo "✅ Docker já instalado"
fi

# 3. Instalar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "🐳 Instalando Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    echo "✅ Docker Compose já instalado"
fi

# 4. Clonar repositório
REPO_DIR="/opt/crm-solar"
if [ ! -d "$REPO_DIR" ]; then
    echo "📥 Clonando repositório..."
    git clone -b dev https://github.com/YOUR_USERNAME/crm-solar.git $REPO_DIR
else
    echo "🔄 Atualizando repositório..."
    cd $REPO_DIR
    git fetch origin dev
    git reset --hard origin/dev
fi

cd $REPO_DIR

# 5. Configurar variáveis de ambiente
if [ ! -f ".env.dev" ]; then
    echo "⚙️  Configurando .env.dev..."
    cp .env.dev.example .env.dev
    echo "⚠️  ATENÇÃO: Edite o arquivo .env.dev com suas credenciais!"
    echo "   nano .env.dev"
    exit 1
fi

# 6. Parar containers antigos
echo "🛑 Parando containers antigos..."
docker-compose -f docker-compose.dev.yml down || true

# 7. Build e start
echo "🏗️  Construindo imagens..."
docker-compose -f docker-compose.dev.yml build --no-cache

echo "🚀 Iniciando containers..."
docker-compose -f docker-compose.dev.yml up -d

# 8. Aguardar backend iniciar
echo "⏳ Aguardando backend iniciar..."
sleep 10

# 9. Executar migrações
echo "🗄️  Executando migrações..."
docker-compose -f docker-compose.dev.yml exec -T backend python manage.py migrate

# 10. Verificar e carregar equipamentos
echo "📦 Verificando equipamentos..."
docker-compose -f docker-compose.dev.yml exec -T backend python verificar_equipamentos.py

# 11. Coletar arquivos estáticos
echo "📦 Coletando arquivos estáticos..."
docker-compose -f docker-compose.dev.yml exec -T backend python manage.py collectstatic --noinput

# 12. Criar superuser (se não existir)
echo "👤 Criando superuser..."
docker-compose -f docker-compose.dev.yml exec -T backend python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser criado: admin/admin123')
else:
    print('✅ Superuser já existe')
EOF

# 12. Verificar status
echo ""
echo "✅ Deploy concluído!"
echo ""
echo "📊 Status dos containers:"
docker-compose -f docker-compose.dev.yml ps
echo ""
echo "🌐 Acesse:"
echo "   Frontend: http://$(curl -s ifconfig.me)"
echo "   Admin: http://$(curl -s ifconfig.me)/admin"
echo ""
echo "📝 Logs:"
echo "   docker-compose -f docker-compose.dev.yml logs -f"
