#!/bin/bash

# Script de Rollback Automático
# Uso: ./rollback.sh [commit_sha]

set -e

BACKUP_DIR="/home/ubuntu/sunops/backups"
COMPOSE_FILE="docker-compose.prod.yml"

echo "🔄 Iniciando rollback..."

# Backup de emergência
echo "💾 Criando backup de emergência..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker-compose -f $COMPOSE_FILE exec -T backend python manage.py dumpdata > "$BACKUP_DIR/rollback_$TIMESTAMP.json"

# Parar containers
echo "⏸️ Parando containers..."
docker-compose -f $COMPOSE_FILE down

if [ -z "$1" ]; then
    # Rollback para versão anterior (última tag)
    echo "⏮️ Rollback para versão anterior..."
    
    # Pegar última versão do backup
    LAST_BACKUP=$(ls -t $BACKUP_DIR/db_*.json | head -1)
    
    if [ -z "$LAST_BACKUP" ]; then
        echo "❌ Nenhum backup encontrado!"
        exit 1
    fi
    
    echo "📦 Restaurando backup: $LAST_BACKUP"
    
    # Subir containers
    docker-compose -f $COMPOSE_FILE up -d
    
    # Aguardar banco
    sleep 10
    
    # Restaurar backup
    docker-compose -f $COMPOSE_FILE exec -T backend python manage.py flush --noinput
    docker-compose -f $COMPOSE_FILE exec -T backend python manage.py loaddata "$LAST_BACKUP"
else
    # Rollback para commit específico
    COMMIT_SHA=$1
    echo "⏮️ Rollback para commit: $COMMIT_SHA"
    
    # Pull das imagens específicas
    docker pull ghcr.io/seu-usuario/sunops/backend:$COMMIT_SHA
    docker pull ghcr.io/seu-usuario/sunops/frontend:$COMMIT_SHA
    
    # Tag como latest
    docker tag ghcr.io/seu-usuario/sunops/backend:$COMMIT_SHA ghcr.io/seu-usuario/sunops/backend:latest
    docker tag ghcr.io/seu-usuario/sunops/frontend:$COMMIT_SHA ghcr.io/seu-usuario/sunops/frontend:latest
    
    # Subir containers
    docker-compose -f $COMPOSE_FILE up -d
fi

# Health check
echo "🏥 Verificando saúde da aplicação..."
sleep 15

if curl -f http://localhost/health/ > /dev/null 2>&1; then
    echo "✅ Rollback concluído com sucesso!"
    echo "📊 Status: Aplicação rodando normalmente"
else
    echo "❌ Rollback falhou! Aplicação não está respondendo"
    exit 1
fi

# Limpar imagens antigas
echo "🧹 Limpando imagens antigas..."
docker image prune -f

echo "🎉 Rollback finalizado!"
