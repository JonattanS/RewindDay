@echo off
REM Setup simplificado para herramientas de video (Windows)
REM Ejecutar como Admin
REM "click derecho" en PowerShell o CMD → "Run as administrator"

setlocal enabledelayedexpansion

echo.
echo 🎬 RewindDay - Setup Video Tools (Simplificado)
echo ================================================
echo.

REM Verificar admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ DEBE ejecutarse como ADMINISTRADOR
    echo.
    echo Click derecho en PowerShell o CMD
    echo "Run as administrator"
    pause
    exit /b 1
)

echo ✅ Permisos de Admin OK
echo.

REM ========================
REM Paso 1: Instalar Ollama
REM ========================

echo [1/5] 📥 Descargando Ollama...
echo.

REM Verificar si ya está instalado
where ollama >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Ollama ya está instalado
) else (
    echo Descargando Ollama desde https://ollama.ai/download
    echo Por favor:
    echo 1. Abre https://ollama.ai/download en tu navegador
    echo 2. Descarga e instala Ollama
    echo 3. Presiona Enter aquí cuando termines
    pause
)

echo.

REM ========================
REM Paso 2: Verificar FFmpeg
REM ========================

echo [2/5] 🎬 Verificando FFmpeg...

where ffmpeg >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ FFmpeg ya está instalado
) else (
    echo ❌ FFmpeg NO está instalado
    echo.
    echo Para instalar:
    echo 1. Descarga: https://ffmpeg.org/download.html
    echo 2. Extrae en C:\ffmpeg
    echo 3. Añade C:\ffmpeg\bin a PATH
    echo.
    echo O instala con Chocolatey:
    echo    choco install ffmpeg
    echo.
    pause
)

echo.

REM ========================
REM Paso 3: Descargar Stable Diffusion
REM ========================

echo [3/5] 🎨 Descargando Stable Diffusion...

if not exist "stable-diffusion-webui" (
    echo Clonando repositorio...
    git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
    if %errorLevel% neq 0 (
        echo ❌ Error clonando. Verifica que Git está instalado
        pause
        exit /b 1
    )
    echo ✅ Stable Diffusion descargado
) else (
    echo ✅ Stable Diffusion ya existe
)

echo.

REM ========================
REM Paso 4: Instalar Piper TTS
REM ========================

echo [4/5] 🎤 Instalando Piper TTS...

pip show piper-tts >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Piper TTS ya está instalado
) else (
    echo Instalando Piper TTS...
    pip install piper-tts
    if %errorLevel% neq 0 (
        echo ❌ Error instalando Piper
    )
)

echo.

REM ========================
REM Paso 5: Instalar Python deps
REM ========================

echo [5/5] 📦 Instalando dependencias Python...

cd apps\ai

REM Crear requirements simplificado (sin Pillow que causa problemas)
echo Creando requirements.txt simplificado...

(
echo fastapi==0.115.5
echo uvicorn==0.32.1
echo pydantic==2.10.3
echo pydantic-settings==2.6.1
echo python-dotenv==1.0.1
echo httpx==0.28.1
echo requests==2.31.0
echo moviepy==1.0.3
echo soundfile==0.12.1
echo pydub==0.25.1
echo numpy==1.24.3
echo opencv-python==4.8.0.76
echo scipy==1.11.4
echo torch==2.1.0
echo torchaudio==0.17.0
echo audiocraft==1.0.0
) > requirements_temp.txt

echo Instalando packages...
pip install -r requirements_temp.txt --prefer-binary

if %errorLevel% neq 0 (
    echo ⚠️  Algunos packages pueden haber fallado
    echo Intenta instalar manualmente:
    echo pip install torch --prefer-binary
    echo pip install audiocraft --prefer-binary
)

del requirements_temp.txt

cd ..\..

echo.
echo ================================================
echo 🎉 Setup completado!
echo ================================================
echo.
echo ✅ Próximos pasos:
echo.
echo 1️⃣  Abre 2 PowerShell como Admin
echo.
echo 2️⃣  En PowerShell 1 - Iniciar Ollama:
echo     ollama serve
echo.
echo 3️⃣  En PowerShell 2 - Iniciar Stable Diffusion:
echo     cd stable-diffusion-webui
echo     webui.bat
echo     (Espera a que se abra http://localhost:7860)
echo.
echo 4️⃣  En PowerShell 3 - Iniciar servicio IA:
echo     cd apps\ai
echo     python -m app.main
echo.
echo 5️⃣  En PowerShell 4 - Iniciar API:
echo     cd apps\api
echo     npm run dev
echo.
echo 6️⃣  Verificar en navegador:
echo     http://localhost:8000/health
echo     http://localhost:8000/api/tools/check
echo.
echo ================================================
pause
