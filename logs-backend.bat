@echo off
echo Logs do backend:
echo.
docker-compose logs backend --tail=50
pause
