@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   CRM Solar - Commit Atomico
echo ========================================
echo.

REM Verificar se há mudanças
git status --short > nul 2>&1
if errorlevel 1 (
    echo Git nao inicializado. Execute: git init
    pause
    exit /b
)

for /f %%i in ('git status --short') do set HAS_CHANGES=1

if not defined HAS_CHANGES (
    echo Nenhuma mudanca para commitar.
    pause
    exit /b
)

echo Mudancas detectadas:
git status --short
echo.

REM Menu de tipos de commit
echo Selecione o tipo de commit:
echo.
echo [1] feat     - Nova funcionalidade
echo [2] fix      - Correcao de bug
echo [3] docs     - Documentacao
echo [4] style    - Formatacao
echo [5] refactor - Refatoracao
echo [6] test     - Testes
echo [7] chore    - Manutencao
echo.

set /p TIPO="Digite o numero (1-7): "

if "%TIPO%"=="1" set COMMIT_TYPE=feat
if "%TIPO%"=="2" set COMMIT_TYPE=fix
if "%TIPO%"=="3" set COMMIT_TYPE=docs
if "%TIPO%"=="4" set COMMIT_TYPE=style
if "%TIPO%"=="5" set COMMIT_TYPE=refactor
if "%TIPO%"=="6" set COMMIT_TYPE=test
if "%TIPO%"=="7" set COMMIT_TYPE=chore

if not defined COMMIT_TYPE (
    echo Opcao invalida!
    pause
    exit /b
)

echo.
REM Escopo
echo Selecione o escopo:
echo.
echo [1] auth         - Autenticacao
echo [2] clientes     - Gestao de clientes
echo [3] dashboard    - Dashboard
echo [4] orcamentos   - Orcamentos
echo [5] calculadora  - Calculadora solar
echo [6] premissas    - Premissas/Config
echo [7] propostas    - Propostas
echo [8] contratos    - Contratos
echo [9] api          - API/Backend
echo [0] frontend     - Frontend
echo.

set /p ESCOPO_NUM="Digite o numero: "

if "%ESCOPO_NUM%"=="1" set ESCOPO=auth
if "%ESCOPO_NUM%"=="2" set ESCOPO=clientes
if "%ESCOPO_NUM%"=="3" set ESCOPO=dashboard
if "%ESCOPO_NUM%"=="4" set ESCOPO=orcamentos
if "%ESCOPO_NUM%"=="5" set ESCOPO=calculadora
if "%ESCOPO_NUM%"=="6" set ESCOPO=premissas
if "%ESCOPO_NUM%"=="7" set ESCOPO=propostas
if "%ESCOPO_NUM%"=="8" set ESCOPO=contratos
if "%ESCOPO_NUM%"=="9" set ESCOPO=api
if "%ESCOPO_NUM%"=="0" set ESCOPO=frontend

if not defined ESCOPO (
    echo Opcao invalida!
    pause
    exit /b
)

echo.
set /p MENSAGEM="Digite a mensagem do commit: "

if "%MENSAGEM%"=="" (
    echo Mensagem nao pode ser vazia!
    pause
    exit /b
)

REM Montar mensagem final
set COMMIT_MSG=%COMMIT_TYPE%(%ESCOPO%): %MENSAGEM%

echo.
echo ========================================
echo Commit a ser criado:
echo %COMMIT_MSG%
echo ========================================
echo.

set /p CONFIRMA="Confirmar? (S/N): "

if /i not "%CONFIRMA%"=="S" (
    echo Commit cancelado.
    pause
    exit /b
)

REM Executar git add e commit
git add .
git commit -m "%COMMIT_MSG%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Commit criado com sucesso!
    echo ========================================
    echo.
    set /p PUSH="Deseja fazer push? (S/N): "
    
    if /i "!PUSH!"=="S" (
        git push
        if !ERRORLEVEL! EQU 0 (
            echo Push realizado!
        ) else (
            echo Erro ao fazer push.
        )
    )
) else (
    echo Erro ao criar commit.
)

echo.
pause
