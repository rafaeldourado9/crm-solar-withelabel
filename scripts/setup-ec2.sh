#!/bin/bash

# Script de Setup Automático para EC2
# Uso: ./setup-ec2.sh [dev|prod]

set -e

ENVIRONMENT=$1

if [ "$ENVIRONMENT" != "dev" ] && [ "$ENVIRONMENT" != "prod" ]; then
    echo "❌ Uso: ./setup-ec2.sh [dev|prod]"
    exit 1
fi

echo "🚀 Configurando servidor $ENVIRONMENT..."

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Atualizar sistema
echo -e "${YELLOW}📦 Atualizando sistema...${NC}"
sudo apt-get update
sudo apt-get upgrade -y

# Instalar Docker
echo -e "${YELLOW}🐳 Instalando Docker...${NC}"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker ubuntu
    echo -e "${GREEN}✅ Docker instalado${NC}"
else
    echo -e "${GREEN}✅ Docker já instalado${NC}"
fi

# Instalar Docker Compose
echo -e "${YELLOW}🐳 Instalando Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✅ Docker Compose instalado${NC}"
else
    echo -e "${GREEN}✅ Docker Compose já instalado${NC}"
fi

# Instalar ferramentas úteis
echo -e "${YELLOW}🔧 Instalando ferramentas...${NC}"
sudo apt-get install -y git curl htop vim jq

# Criar estrutura de diretórios
echo -e "${YELLOW}📁 Criando estrutura de diretórios...${NC}"
sudo mkdir -p /opt/crm-solar/.backup
sudo chown -R ubuntu:ubuntu /opt/crm-solar

# Configurar firewall
echo -e "${YELLOW}🔥 Configurando firewall...${NC}"
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp
sudo ufw --force enable

# Configurar swap (para servidores pequenos)
echo -e "${YELLOW}💾 Configurando swap...${NC}"
if [ ! -f /swapfile ]; then
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo -e "${GREEN}✅ Swap configurado${NC}"
fi

# Configurar limites do sistema
echo -e "${YELLOW}⚙️  Configurando limites do sistema...${NC}"
cat << EOF | sudo tee -a /etc/security/limits.conf
* soft nofile 65536
* hard nofile 65536
* soft nproc 65536
* hard nproc 65536
EOF

# Otimizar kernel
echo -e "${YELLOW}⚙️  Otimizando kernel...${NC}"
cat << EOF | sudo tee -a /etc/sysctl.conf
vm.swappiness=10
vm.vfs_cache_pressure=50
net.core.somaxconn=1024
net.ipv4.tcp_max_syn_backlog=2048
EOF
sudo sysctl -p

# Clonar repositório
echo -e "${YELLOW}📥 Clonando repositório...${NC}"
cd /opt/crm-solar

if [ ! -d ".git" ]; then
    read -p "URL do repositório GitHub: " REPO_URL
    git clone "$REPO_URL" .
    git checkout "$ENVIRONMENT"
    echo -e "${GREEN}✅ Repositório clonado${NC}"
else
    echo -e "${GREEN}✅ Repositório já existe${NC}"
    git checkout "$ENVIRONMENT"
    git pull origin "$ENVIRONMENT"
fi

# Criar .env interativo
echo -e "${YELLOW}📝 Configurando variáveis de ambiente...${NC}"

if [ ! -f ".env" ]; then
    echo "Vamos configurar o arquivo .env..."
    
    read -p "Django Secret Key (deixe vazio para gerar): " SECRET_KEY
    if [ -z "$SECRET_KEY" ]; then
        SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
    fi
    
    read -p "RDS Endpoint (ex: xxx.rds.amazonaws.com): " DB_HOST
    read -sp "RDS Password: " DB_PASSWORD
    echo ""
    read -p "IP Público deste servidor: " SERVER_IP
    read -p "S3 Bucket Name: " S3_BUCKET
    read -p "CloudFront Domain: " CLOUDFRONT_DOMAIN
    read -p "AWS Access Key ID: " AWS_ACCESS_KEY_ID
    read -sp "AWS Secret Access Key: " AWS_SECRET_ACCESS_KEY
    echo ""
    
    cat > .env << EOF
# Django
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=$SERVER_IP,localhost

# Database (RDS)
DB_NAME=crm_solar
DB_USER=postgres
DB_PASSWORD=$DB_PASSWORD
DB_HOST=$DB_HOST
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# CORS
CORS_ORIGINS=http://$SERVER_IP

# S3
AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME=$S3_BUCKET
AWS_S3_REGION_NAME=us-east-1

# CloudFront
CLOUDFRONT_DOMAIN=$CLOUDFRONT_DOMAIN

# GitHub
GITHUB_REPOSITORY=seu-usuario/SunOps---SaaS
IMAGE_TAG=${ENVIRONMENT}-latest
EOF
    
    echo -e "${GREEN}✅ Arquivo .env criado${NC}"
else
    echo -e "${YELLOW}⚠️  Arquivo .env já existe, pulando...${NC}"
fi

# Iniciar aplicação
echo -e "${YELLOW}🚀 Iniciando aplicação...${NC}"
docker-compose -f docker-compose.prod.yml up -d

# Aguardar containers
echo -e "${YELLOW}⏳ Aguardando containers iniciarem...${NC}"
sleep 30

# Executar migrações
echo -e "${YELLOW}🔄 Executando migrações...${NC}"
docker-compose -f docker-compose.prod.yml exec -T backend python manage.py migrate

# Coletar arquivos estáticos
echo -e "${YELLOW}📦 Coletando arquivos estáticos...${NC}"
docker-compose -f docker-compose.prod.yml exec -T backend python manage.py collectstatic --no-input

# Verificar saúde
echo -e "${YELLOW}🔍 Verificando saúde da aplicação...${NC}"
sleep 10

if curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Aplicação está saudável!${NC}"
else
    echo -e "${RED}❌ Aplicação não está respondendo${NC}"
    echo "Verificando logs..."
    docker-compose -f docker-compose.prod.yml logs --tail=50
    exit 1
fi

# Configurar cron para limpeza
echo -e "${YELLOW}⏰ Configurando tarefas agendadas...${NC}"
(crontab -l 2>/dev/null; echo "0 2 * * * cd /opt/crm-solar && docker system prune -af > /dev/null 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "0 3 * * * cd /opt/crm-solar && docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U postgres crm_solar > .backup/db_auto_\$(date +\%Y\%m\%d).sql") | crontab -

# Resumo
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   ✅ SETUP CONCLUÍDO COM SUCESSO!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "📊 Status dos serviços:"
docker-compose -f docker-compose.prod.yml ps
echo ""
echo "🌐 Acesse a aplicação:"
echo "   Frontend: http://$SERVER_IP"
echo "   Backend:  http://$SERVER_IP:8000"
echo "   Admin:    http://$SERVER_IP:8000/admin"
echo ""
echo "📝 Próximos passos:"
echo "   1. Criar superusuário: docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser"
echo "   2. Configurar domínio (opcional)"
echo "   3. Configurar SSL com Let's Encrypt"
echo ""
echo "📋 Comandos úteis:"
echo "   Ver logs:     docker-compose -f docker-compose.prod.yml logs -f"
echo "   Reiniciar:    docker-compose -f docker-compose.prod.yml restart"
echo "   Parar:        docker-compose -f docker-compose.prod.yml down"
echo "   Backup:       docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U postgres crm_solar > backup.sql"
echo ""
