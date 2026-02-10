@echo off
echo Aplicando migracoes...
docker-compose exec backend python manage.py migrate
echo.
echo Migracoes aplicadas com sucesso!
pause
