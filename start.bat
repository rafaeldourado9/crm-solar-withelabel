@echo off
echo Iniciando CRM Solar...
echo.

start "Backend Django" cmd /k "cd backend && python manage.py runserver"
timeout /t 3 /nobreak > nul

start "Frontend React" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo CRM Solar iniciado!
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo Admin:    http://localhost:8000/admin
echo ========================================
