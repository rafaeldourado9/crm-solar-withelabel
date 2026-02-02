@echo off
echo ============================================
echo TESTANDO GERACAO DE ORCAMENTO COM TEMPLATE
echo ============================================
echo.

docker-compose exec backend python testar_geracao_orcamento.py

echo.
echo ============================================
pause
