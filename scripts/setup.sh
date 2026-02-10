#!/bin/bash

# Script de Setup Rápido - AWS EC2
# Execute: curl -fsSL https://raw.githubusercontent.com/seu-repo/main/scripts/setup.sh | bash

set -e

echo "🚀 Iniciando setup do CRM Solar..."

# Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt-get update
sudo apt-get upgrade -y

# Instalar Docker
echo "🐳 Instalando Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
rm get-docker.sh

# Instalar Docker Compose
echo "🔧 Instalando Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Instalar AWS CLI
echo "☁️ Instalando AWS CLI..."
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt-get install -y unzip
unzip awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip

# Instalar Certbot (SSL)
echo "🔐 Instalando Certbot..."
sudo apt-get install -y certbot

# Criar estrutura de diretórios
echo "📁 Criando diretórios..."
mkdir -p /home/ubuntu/sunops/{backend,frontend,nginx,backups,scripts}
cd /home/ubuntu/sunops

# Configurar firewall
echo "🔥 Configurando firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Configurar swap (para t3.micro)
echo "💾 Configurando swap..."
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Otimizações de performance
echo "⚡ Otimizando sistema..."
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'net.core.somaxconn=1024' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

echo "✅ Setup concluído!"
echo ""
echo "Próximos passos:"
echo "1. Configure o AWS CLI: aws configure"
echo "2. Clone o repositório: git clone https://github.com/seu-repo/sunops.git ."
echo "3. Configure .env: cp .env.example .env.prod && nano .env.prod"
echo "4. Gere SSL: sudo certbot certonly --standalone -d seu-dominio.com"
echo "5. Suba a aplicação: docker-compose -f docker-compose.prod.yml up -d"
echo ""
echo "🎉 Pronto para deploy!"
