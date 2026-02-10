@echo off
echo ========================================
echo Testes Rapidos - CRM Solar
echo ========================================
echo.

echo [1/5] Testando backend...
docker-compose exec -T backend python manage.py check
if %errorlevel% neq 0 (
    echo ERRO: Backend com problemas
    exit /b 1
)
echo OK: Backend funcionando
echo.

echo [2/5] Testando migrações...
docker-compose exec -T backend python manage.py showmigrations | findstr "\[ \]"
if %errorlevel% equ 0 (
    echo AVISO: Existem migrações pendentes
) else (
    echo OK: Migrações aplicadas
)
echo.

echo [3/5] Testando autenticação...
curl -s -X POST http://localhost/api/auth/login/ -H "Content-Type: application/json" -d "{\"username\":\"wrong\",\"password\":\"wrong\"}" | findstr "error"
if %errorlevel% equ 0 (
    echo OK: Autenticação protegida
) else (
    echo ERRO: Autenticação não está protegida
)
echo.

echo [4/5] Testando headers de segurança...
curl -s -I http://localhost/api/clientes/ | findstr "X-Content-Type-Options"
if %errorlevel% equ 0 (
    echo OK: Headers de segurança presentes
) else (
    echo AVISO: Headers de segurança ausentes
)
echo.

echo [5/5] Testando timeout...
echo Fazendo requisição ao dashboard...
curl -s -w "Tempo: %%{time_total}s\n" http://localhost/api/dashboard/kpis/ -o nul
echo.

echo ========================================
echo Testes concluidos!
echo ========================================
