@echo off
echo Instalando dependencias no Docker...
docker-compose exec backend pip install python-docx matplotlib google-generativeai
echo.
echo Reiniciando backend...
docker-compose restart backend
echo.
echo Pronto! Sistema de IA configurado.
pause
