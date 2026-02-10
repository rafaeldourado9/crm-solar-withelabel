#!/bin/bash

# Script de monitoramento com fallback automático
LOG_FILE="/var/log/crm-solar-monitor.log"
MAX_FAILURES=3
FAILURE_COUNT=0

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

check_health() {
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health/)
    echo $response
}

restart_services() {
    log "⚠️  Reiniciando serviços..."
    cd /opt/crm-solar
    docker-compose -f docker-compose.dev.yml restart backend
    sleep 10
    log "✅ Serviços reiniciados"
}

log "🔍 Iniciando monitoramento..."

while true; do
    status=$(check_health)
    
    if [ "$status" != "200" ]; then
        FAILURE_COUNT=$((FAILURE_COUNT + 1))
        log "❌ Health check falhou (${FAILURE_COUNT}/${MAX_FAILURES}): HTTP $status"
        
        if [ $FAILURE_COUNT -ge $MAX_FAILURES ]; then
            log "🚨 Limite de falhas atingido. Executando fallback..."
            restart_services
            FAILURE_COUNT=0
        fi
    else
        if [ $FAILURE_COUNT -gt 0 ]; then
            log "✅ Sistema recuperado"
        fi
        FAILURE_COUNT=0
    fi
    
    sleep 30
done
