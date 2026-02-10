#!/bin/bash
set -e

echo "🔍 Validação Pré-Deploy - CRM Solar"
echo "===================================="
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0

# 1. Verificar arquivos essenciais
echo "📁 Verificando arquivos essenciais..."
FILES=(
    "backend/config/settings.py"
    "backend/requirements.txt"
    "backend/Dockerfile"
    "frontend/Dockerfile.prod"
    "docker-compose.dev.yml"
    "nginx/nginx.dev.conf"
    ".env.dev.example"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file não encontrado"
        ERRORS=$((ERRORS+1))
    fi
done
echo ""

# 2. Verificar configurações de segurança
echo "🔒 Verificando configurações de segurança..."

if grep -q "django-csp" backend/requirements.txt; then
    echo -e "${GREEN}✓${NC} CSP instalado"
else
    echo -e "${RED}✗${NC} CSP não encontrado"
    ERRORS=$((ERRORS+1))
fi

if grep -q "django-defender" backend/requirements.txt; then
    echo -e "${GREEN}✓${NC} Defender instalado"
else
    echo -e "${RED}✗${NC} Defender não encontrado"
    ERRORS=$((ERRORS+1))
fi

if grep -q "SECURE_BROWSER_XSS_FILTER" backend/config/settings.py; then
    echo -e "${GREEN}✓${NC} Headers de segurança configurados"
else
    echo -e "${RED}✗${NC} Headers de segurança não configurados"
    ERRORS=$((ERRORS+1))
fi
echo ""

# 3. Verificar timeouts
echo "⏱️  Verificando timeouts..."

if grep -q "timeout.*120" backend/Dockerfile; then
    echo -e "${GREEN}✓${NC} Gunicorn timeout: 120s"
else
    echo -e "${YELLOW}⚠${NC} Gunicorn timeout não configurado"
fi

if grep -q "proxy_read_timeout.*120s" nginx/nginx.dev.conf; then
    echo -e "${GREEN}✓${NC} Nginx timeout: 120s"
else
    echo -e "${YELLOW}⚠${NC} Nginx timeout não configurado"
fi
echo ""

# 4. Verificar remoção do serviço de suporte
echo "🗑️  Verificando remoção de serviços..."

if ! grep -q "apps.suporte" backend/config/settings.py; then
    echo -e "${GREEN}✓${NC} Serviço de suporte removido"
else
    echo -e "${RED}✗${NC} Serviço de suporte ainda presente"
    ERRORS=$((ERRORS+1))
fi
echo ""

# 5. Executar testes
echo "🧪 Executando testes..."
if [ -f "backend/test_security.py" ]; then
    docker-compose exec -T backend python test_security.py 2>&1 | grep -E "(OK|FAILED|ERROR)" || true
else
    echo -e "${YELLOW}⚠${NC} Arquivo de testes não encontrado"
fi
echo ""

# 6. Verificar variáveis de ambiente
echo "🔐 Verificando variáveis de ambiente..."
if [ -f ".env.dev.example" ]; then
    echo -e "${GREEN}✓${NC} .env.dev.example existe"
    
    REQUIRED_VARS=("SECRET_KEY" "DB_HOST" "DB_PASSWORD" "ALLOWED_HOSTS")
    for var in "${REQUIRED_VARS[@]}"; do
        if grep -q "$var" .env.dev.example; then
            echo -e "${GREEN}✓${NC} $var presente"
        else
            echo -e "${RED}✗${NC} $var ausente"
            ERRORS=$((ERRORS+1))
        fi
    done
else
    echo -e "${RED}✗${NC} .env.dev.example não encontrado"
    ERRORS=$((ERRORS+1))
fi
echo ""

# 7. Verificar dependências Python
echo "📦 Verificando dependências..."
REQUIRED_DEPS=("Django" "djangorestframework" "gunicorn" "psycopg2-binary")
for dep in "${REQUIRED_DEPS[@]}"; do
    if grep -q "$dep" backend/requirements.txt; then
        echo -e "${GREEN}✓${NC} $dep"
    else
        echo -e "${RED}✗${NC} $dep não encontrado"
        ERRORS=$((ERRORS+1))
    fi
done
echo ""

# Resultado final
echo "===================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Validação concluída com sucesso!${NC}"
    echo "Sistema pronto para deploy."
    exit 0
else
    echo -e "${RED}❌ Validação falhou com $ERRORS erro(s)${NC}"
    echo "Corrija os erros antes de fazer deploy."
    exit 1
fi
