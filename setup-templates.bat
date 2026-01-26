@echo off
echo ========================================
echo Aplicando migracoes de templates...
echo ========================================
docker-compose exec backend python manage.py migrate templates
echo.
echo ========================================
echo Instalando dependencias...
echo ========================================
docker-compose exec backend pip install python-docx matplotlib google-generativeai
echo.
echo ========================================
echo Reiniciando backend...
echo ========================================
docker-compose restart backend
echo.
echo ========================================
echo Aguardando 10 segundos...
echo ========================================
timeout /t 10 /nobreak
echo.
echo Pronto! Teste novamente.
pause
