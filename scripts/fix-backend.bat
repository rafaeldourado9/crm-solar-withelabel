@echo off
echo ========================================
echo Verificando status dos containers...
echo ========================================
docker-compose ps
echo.
echo ========================================
echo Aplicando migracoes...
echo ========================================
docker-compose exec backend python manage.py migrate
echo.
echo ========================================
echo Reiniciando backend...
echo ========================================
docker-compose restart backend
echo.
echo ========================================
echo Aguardando backend iniciar (10s)...
echo ========================================
timeout /t 10 /nobreak
echo.
echo ========================================
echo Status final:
echo ========================================
docker-compose ps
echo.
echo Pronto! Teste novamente no navegador.
pause
