#!/bin/bash

echo "==================================="
echo "SunOps - Diagnóstico do Sistema"
echo "==================================="
echo ""

# Verificar se o backend está rodando
echo "1. Verificando Backend..."
if curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; then
    echo "✅ Backend está rodando"
    curl -s http://localhost:8000/api/v1/health | jq .
else
    echo "❌ Backend NÃO está rodando na porta 8000"
    echo "   Execute: cd backend && uvicorn src.main:app --reload"
fi
echo ""

# Verificar se o frontend está rodando
echo "2. Verificando Frontend..."
if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo "✅ Frontend está rodando"
else
    echo "❌ Frontend NÃO está rodando na porta 5173"
    echo "   Execute: cd frontend && npm run dev"
fi
echo ""

# Verificar arquivos .env
echo "3. Verificando arquivos .env..."
if [ -f "backend/.env" ]; then
    echo "✅ backend/.env existe"
else
    echo "❌ backend/.env NÃO existe"
    echo "   Execute: cp backend/.env.example backend/.env"
fi

if [ -f "frontend/.env" ]; then
    echo "✅ frontend/.env existe"
else
    echo "❌ frontend/.env NÃO existe"
    echo "   Execute: cp frontend/.env.example frontend/.env"
fi
echo ""

# Verificar banco de dados
echo "4. Verificando Banco de Dados..."
if [ -f "backend/test.db" ]; then
    echo "✅ Banco de dados existe"
else
    echo "❌ Banco de dados NÃO existe"
    echo "   Execute: cd backend && alembic upgrade head && python seed.py"
fi
echo ""

# Verificar dependências
echo "5. Verificando Dependências..."
if [ -d "backend/venv" ] || [ -d "backend/.venv" ]; then
    echo "✅ Virtual environment do backend existe"
else
    echo "⚠️  Virtual environment do backend não encontrado"
    echo "   Execute: cd backend && python -m venv venv && source venv/bin/activate && pip install -e ."
fi

if [ -d "frontend/node_modules" ]; then
    echo "✅ node_modules do frontend existe"
else
    echo "❌ node_modules do frontend NÃO existe"
    echo "   Execute: cd frontend && npm install"
fi
echo ""

echo "==================================="
echo "Diagnóstico Completo"
echo "==================================="
