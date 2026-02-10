@echo off
echo ========================================
echo Verificando Equipamentos - CRM Solar
echo ========================================
echo.

docker-compose exec -T backend python verificar_equipamentos.py

echo.
echo ========================================
pause
