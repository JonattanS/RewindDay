@echo off
REM Setup script para herramientas de video (Windows)
REM Ejecutar como Admin

echo 🎬 RewindDay - Setup de Herramientas de Video
echo ============================================

REM Verificar admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Requiere permisos de Admin
    pause
    exit /b 1
)

REM ========================
REM 1. Verificar Chocolatey
REM ========================

where choco >nul 2>&1
if %errorLevel% neq 0 (
    echo 📥 Instalando Chocolatey...
    @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.ServicePointManager).SecurityProtocol = 3072; iex(New-Object Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    echo ✅ Chocolatey instalado
) else (
    echo ✅ Chocolatey ya está instalado
)

REM ========================
REM 2. FFmpeg
REM ========================

echo 📥 Instalando FFmpeg...
choco install ffmpeg -y
echo ✅ FFmpeg instalado

REM ========================
REM 3. Ollama
REM ========================

echo 📥 Descargando Ollama...
powershell -Command "(New-Object System.Net.ServicePointManager).SecurityProtocol = 3072; Invoke-WebRequest -Uri 'https://ollama.ai/download/windows' -OutFile 'OllamaSetup.exe'"
echo ✅ Ejecutor OllamaSetup.exe (cuando termine, presiona Enter)"
pause

REM ========================
REM 4. Python Dependencies
REM ========================

echo 📥 Instalando dependencias Python...

cd apps\ai
pip install -r requirements.txt

echo ✅ Dependencias instaladas

REM ========================
REM Finish
REM ========================

echo.
echo 🎉 Setup completado!
echo.
echo Próximos pasos:
echo 1. Abre PowerShell y ejecuta: ollama serve
echo 2. En otra ventana, descarga Stable Diffusion:
echo    git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
echo    cd stable-diffusion-webui
echo    webui.bat
echo 3. Inicia el servicio: python apps/ai/app/main.py
echo 4. Prueba: curl http://localhost:8000/health
echo.
pause
