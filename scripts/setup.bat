@echo off
echo ========================================
echo RewindDay - Setup Script (Windows)
echo ========================================
echo.

REM Verificar que Node.js está instalado
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js no está instalado
    echo Por favor instala Node.js desde https://nodejs.org/
    pause
    exit /b 1
)

REM Verificar que Python está instalado
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python no está instalado
    echo Por favor instala Python 3.11+ desde https://www.python.org/
    pause
    exit /b 1
)

REM Verificar que Docker está instalado
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker no está instalado
    echo Por favor instala Docker Desktop desde https://www.docker.com/
    pause
    exit /b 1
)

echo [1/5] Creando archivos .env...
if not exist .env (
    copy .env.example .env
    echo [OK] .env creado
) else (
    echo [SKIP] .env ya existe
)

if not exist apps\mobile\.env (
    copy apps\mobile\.env.example apps\mobile\.env
    echo [OK] apps\mobile\.env creado
) else (
    echo [SKIP] apps\mobile\.env ya existe
)

if not exist apps\api\.env (
    copy apps\api\.env.example apps\api\.env
    echo [OK] apps\api\.env creado
) else (
    echo [SKIP] apps\api\.env ya existe
)

if not exist apps\ai\.env (
    copy apps\ai\.env.example apps\ai\.env
    echo [OK] apps\ai\.env creado
) else (
    echo [SKIP] apps\ai\.env ya existe
)

echo.
echo [2/5] Instalando dependencias de la app móvil...
cd apps\mobile
call npm install
cd ..\..

echo.
echo [3/5] Instalando dependencias del API...
cd apps\api
call npm install
cd ..\..

echo.
echo [4/5] Instalando dependencias del servicio de IA...
cd apps\ai
pip install -r requirements.txt
cd ..\..

echo.
echo [5/5] Levantando servicios con Docker...
docker-compose up -d

echo.
echo ========================================
echo [COMPLETO] Setup finalizado exitosamente
echo ========================================
echo.
echo Servicios disponibles:
echo   - API: http://localhost:3000
echo   - AI Service: http://localhost:8000
echo   - PostgreSQL: localhost:5432
echo.
echo Para iniciar la app móvil:
echo   cd apps\mobile
echo   npx expo start
echo.
pause
