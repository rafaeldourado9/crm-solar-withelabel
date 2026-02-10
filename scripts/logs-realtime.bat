@echo off
echo Logs do backend em tempo real:
echo Pressione Ctrl+C para sair
echo.
docker-compose logs -f backend
