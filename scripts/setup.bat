@echo off
echo ========================================
echo    CRM SOLAR - Inicializacao Rapida
echo ========================================
echo.

echo [1/4] Instalando dependencias do backend...
cd backend
pip install -r requirements.txt
echo.

echo [2/4] Criando banco de dados...
python manage.py migrate
echo.

echo [3/4] Instalando dependencias do frontend...
cd ..\frontend
call npm install
echo.

echo [4/4] Pronto!
echo.
echo ========================================
echo Para iniciar o sistema:
echo.
echo Backend:  cd backend ^&^& python manage.py runserver
echo Frontend: cd frontend ^&^& npm run dev
echo.
echo Acesse: http://localhost:5173
echo ========================================
pause
