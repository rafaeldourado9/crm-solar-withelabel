#!/bin/bash

# Script de Rollback Automático
# Uso: ./rollback.sh [timestamp_backup]

set -e

BACKUP_DIR="/opt/crm-solar/.backup"
COMPOSE_FILE="docker-compose.prod.yml"

echo "🔄 Iniciando processo de rollback..."

# Verificar se está no diretório correto
if [ ! -f "$COMPOSE_FILE" ]; then
    echo "❌ Erro: docker-compose.prod.yml não encontrado"
    echo "Execute este script de /opt/crm-solar"
    exit 1
fi

# Parar serviços atuais
echo "⏸️  Parando serviços atuais..."
docker-compose -f "$COMPOSE_FILE" down

# Restaurar imagens Docker
if [ -f "$BACKUP_DIR/last_images.txt" ]; then
    echo "📦 Restaurando imagens Docker anteriores..."
    while IFS= read -r image; do
        echo "  → Pulling: $image"
        docker pull "$image" || echo "  ⚠️  Falha ao baixar: $image"
    done < "$BACKUP_DIR/last_images.txt"
else
    echo "⚠️  Arquivo de backup de imagens não encontrado"
fi

# Restaurar banco de dados
if [ -n "$1" ]; then
    BACKUP_FILE="$BACKUP_DIR/db_$1.sql"
else
    BACKUP_FILE=$(ls -t "$BACKUP_DIR"/db_*.sql 2>/dev/null | head -n 1)
fi

if [ -f "$BACKUP_FILE" ]; then
    echo "💾 Restaurando banco de dados de: $(basename $BACKUP_FILE)"
    
    # Subir apenas o banco
    docker-compose -f "$COMPOSE_FILE" up -d db
    sleep 5
    
    # Restaurar backup
    docker-compose -f "$COMPOSE_FILE" exec -T db psql -U postgres crm_solar < "$BACKUP_FILE"
    echo "✅ Banco de dados restaurado"
else
    echo "⚠️  Nenhum backup de banco encontrado, pulando restauração"
fi

# Subir todos os serviços
echo "🚀 Iniciando serviços..."
docker-compose -f "$COMPOSE_FILE" up -d

# Aguardar serviços
echo "⏳ Aguardando serviços iniciarem..."
sleep 15

# Executar migrações (caso necessário)
echo "🔄 Executando migrações..."
docker-compose -f "$COMPOSE_FILE" exec -T backend python manage.py migrate || true

# Verificar saúde
echo "🔍 Verificando saúde dos serviços..."
for i in {1..30}; do
    if curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
        echo "✅ Rollback concluído com sucesso!"
        echo ""
        echo "📊 Status dos serviços:"
        docker-compose -f "$COMPOSE_FILE" ps
        exit 0
    fi
    echo "  Tentativa $i/30..."
    sleep 2
done

echo "❌ Rollback falhou: serviços não responderam ao health check"
echo "📋 Logs dos serviços:"
docker-compose -f "$COMPOSE_FILE" logs --tail=50
exit 1
