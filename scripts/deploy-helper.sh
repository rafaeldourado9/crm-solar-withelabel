#!/bin/bash

# ========================================
# COMANDOS ÚTEIS - CRM SOLAR CI/CD
# ========================================

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ========================================
# FUNÇÕES DE DEPLOY
# ========================================

deploy_dev() {
    echo -e "${YELLOW}🚀 Iniciando deploy para DEV...${NC}"
    git checkout dev
    git pull origin dev
    git push origin dev
    echo -e "${GREEN}✅ Push realizado! Acompanhe em: https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/actions${NC}"
}

deploy_prod() {
    echo -e "${YELLOW}🚀 Iniciando deploy para PROD...${NC}"
    echo -e "${RED}⚠️  ATENÇÃO: Deploy para produção requer aprovação manual!${NC}"
    git checkout prod
    git pull origin prod
    git merge dev
    git push origin prod
    echo -e "${GREEN}✅ Push realizado! Aprove em: https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/actions${NC}"
}

# ========================================
# FUNÇÕES DE MONITORAMENTO
# ========================================

check_dev() {
    echo -e "${YELLOW}🔍 Verificando servidor DEV...${NC}"
    ssh $DEV_USER@$DEV_HOST "cd /opt/crm-solar && docker-compose -f docker-compose.prod.yml ps"
    echo ""
    echo -e "${YELLOW}Health Check:${NC}"
    curl -s http://$DEV_HOST:8000/health/ | jq '.' || echo -e "${RED}❌ Health check falhou${NC}"
}

check_prod() {
    echo -e "${YELLOW}🔍 Verificando servidor PROD...${NC}"
    ssh $PROD_USER@$PROD_HOST "cd /opt/crm-solar && docker-compose -f docker-compose.prod.yml ps"
    echo ""
    echo -e "${YELLOW}Health Check:${NC}"
    curl -s http://$PROD_HOST:8000/health/ | jq '.' || echo -e "${RED}❌ Health check falhou${NC}"
}

logs_dev() {
    echo -e "${YELLOW}📋 Logs do servidor DEV...${NC}"
    ssh $DEV_USER@$DEV_HOST "cd /opt/crm-solar && docker-compose -f docker-compose.prod.yml logs --tail=100 -f"
}

logs_prod() {
    echo -e "${YELLOW}📋 Logs do servidor PROD...${NC}"
    ssh $PROD_USER@$PROD_HOST "cd /opt/crm-solar && docker-compose -f docker-compose.prod.yml logs --tail=100 -f"
}

# ========================================
# FUNÇÕES DE BACKUP
# ========================================

backup_dev() {
    echo -e "${YELLOW}💾 Criando backup do DEV...${NC}"
    ssh $DEV_USER@$DEV_HOST "cd /opt/crm-solar && docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U postgres crm_solar > .backup/db_manual_$(date +%Y%m%d_%H%M%S).sql"
    echo -e "${GREEN}✅ Backup criado!${NC}"
}

backup_prod() {
    echo -e "${YELLOW}💾 Criando backup do PROD...${NC}"
    ssh $PROD_USER@$PROD_HOST "cd /opt/crm-solar && docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U postgres crm_solar > .backup/db_manual_$(date +%Y%m%d_%H%M%S).sql"
    echo -e "${GREEN}✅ Backup criado!${NC}"
}

list_backups_dev() {
    echo -e "${YELLOW}📦 Backups disponíveis no DEV:${NC}"
    ssh $DEV_USER@$DEV_HOST "ls -lh /opt/crm-solar/.backup/"
}

list_backups_prod() {
    echo -e "${YELLOW}📦 Backups disponíveis no PROD:${NC}"
    ssh $PROD_USER@$PROD_HOST "ls -lh /opt/crm-solar/.backup/"
}

# ========================================
# FUNÇÕES DE ROLLBACK
# ========================================

rollback_dev() {
    echo -e "${RED}⏮️  Executando rollback no DEV...${NC}"
    ssh $DEV_USER@$DEV_HOST "cd /opt/crm-solar && ./scripts/rollback.sh"
}

rollback_prod() {
    echo -e "${RED}⚠️  ATENÇÃO: Rollback em PRODUÇÃO!${NC}"
    read -p "Tem certeza? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
        ssh $PROD_USER@$PROD_HOST "cd /opt/crm-solar && ./scripts/rollback.sh"
    else
        echo -e "${YELLOW}Rollback cancelado${NC}"
    fi
}

# ========================================
# FUNÇÕES DE MANUTENÇÃO
# ========================================

restart_dev() {
    echo -e "${YELLOW}🔄 Reiniciando serviços no DEV...${NC}"
    ssh $DEV_USER@$DEV_HOST "cd /opt/crm-solar && docker-compose -f docker-compose.prod.yml restart"
    echo -e "${GREEN}✅ Serviços reiniciados!${NC}"
}

restart_prod() {
    echo -e "${RED}⚠️  Reiniciando serviços no PROD...${NC}"
    read -p "Tem certeza? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
        ssh $PROD_USER@$PROD_HOST "cd /opt/crm-solar && docker-compose -f docker-compose.prod.yml restart"
        echo -e "${GREEN}✅ Serviços reiniciados!${NC}"
    else
        echo -e "${YELLOW}Reinício cancelado${NC}"
    fi
}

clean_images_dev() {
    echo -e "${YELLOW}🧹 Limpando imagens antigas no DEV...${NC}"
    ssh $DEV_USER@$DEV_HOST "docker image prune -af"
    echo -e "${GREEN}✅ Limpeza concluída!${NC}"
}

clean_images_prod() {
    echo -e "${YELLOW}🧹 Limpando imagens antigas no PROD...${NC}"
    ssh $PROD_USER@$PROD_HOST "docker image prune -af"
    echo -e "${GREEN}✅ Limpeza concluída!${NC}"
}

# ========================================
# FUNÇÕES DE DESENVOLVIMENTO
# ========================================

create_feature() {
    if [ -z "$1" ]; then
        echo -e "${RED}❌ Uso: create_feature nome-da-feature${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}🌿 Criando branch feature/$1...${NC}"
    git checkout dev
    git pull origin dev
    git checkout -b "feature/$1"
    echo -e "${GREEN}✅ Branch criada! Faça suas alterações e depois: git push origin feature/$1${NC}"
}

merge_to_dev() {
    echo -e "${YELLOW}🔀 Fazendo merge para dev...${NC}"
    CURRENT_BRANCH=$(git branch --show-current)
    git checkout dev
    git pull origin dev
    git merge "$CURRENT_BRANCH"
    git push origin dev
    echo -e "${GREEN}✅ Merge concluído! Deploy automático iniciado.${NC}"
}

# ========================================
# MENU INTERATIVO
# ========================================

show_menu() {
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}   CRM SOLAR - COMANDOS ÚTEIS${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "DEPLOY:"
    echo "  1) Deploy DEV (automático)"
    echo "  2) Deploy PROD (com aprovação)"
    echo ""
    echo "MONITORAMENTO:"
    echo "  3) Status DEV"
    echo "  4) Status PROD"
    echo "  5) Logs DEV"
    echo "  6) Logs PROD"
    echo ""
    echo "BACKUP:"
    echo "  7) Criar backup DEV"
    echo "  8) Criar backup PROD"
    echo "  9) Listar backups DEV"
    echo " 10) Listar backups PROD"
    echo ""
    echo "ROLLBACK:"
    echo " 11) Rollback DEV"
    echo " 12) Rollback PROD"
    echo ""
    echo "MANUTENÇÃO:"
    echo " 13) Reiniciar DEV"
    echo " 14) Reiniciar PROD"
    echo " 15) Limpar imagens DEV"
    echo " 16) Limpar imagens PROD"
    echo ""
    echo "DESENVOLVIMENTO:"
    echo " 17) Criar feature branch"
    echo " 18) Merge para dev"
    echo ""
    echo "  0) Sair"
    echo ""
    read -p "Escolha uma opção: " choice
    
    case $choice in
        1) deploy_dev ;;
        2) deploy_prod ;;
        3) check_dev ;;
        4) check_prod ;;
        5) logs_dev ;;
        6) logs_prod ;;
        7) backup_dev ;;
        8) backup_prod ;;
        9) list_backups_dev ;;
        10) list_backups_prod ;;
        11) rollback_dev ;;
        12) rollback_prod ;;
        13) restart_dev ;;
        14) restart_prod ;;
        15) clean_images_dev ;;
        16) clean_images_prod ;;
        17) read -p "Nome da feature: " fname; create_feature "$fname" ;;
        18) merge_to_dev ;;
        0) exit 0 ;;
        *) echo -e "${RED}Opção inválida${NC}" ;;
    esac
    
    show_menu
}

# ========================================
# CONFIGURAÇÃO
# ========================================

# Carregar variáveis de ambiente se existir
if [ -f ".env.deploy" ]; then
    source .env.deploy
else
    echo -e "${YELLOW}⚠️  Arquivo .env.deploy não encontrado${NC}"
    echo "Crie um arquivo .env.deploy com:"
    echo "DEV_USER=ubuntu"
    echo "DEV_HOST=seu-ip-dev"
    echo "PROD_USER=ubuntu"
    echo "PROD_HOST=seu-ip-prod"
    echo ""
fi

# ========================================
# EXECUÇÃO
# ========================================

# Se chamado com argumento, executa função diretamente
if [ -n "$1" ]; then
    $@
else
    # Senão, mostra menu interativo
    show_menu
fi
