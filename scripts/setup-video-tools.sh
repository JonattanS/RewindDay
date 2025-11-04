#!/bin/bash

# Setup script para herramientas de video (Mac/Linux)
# Ejecutar: bash scripts/setup-video-tools.sh

set -e

echo "🎬 RewindDay - Setup de Herramientas de Video"
echo "=============================================="

# Verificar OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    echo "❌ SO no soportado"
    exit 1
fi

echo "📱 Sistema: $OS"

# ========================
# 1. FFmpeg
# ========================

echo "📥 Instalando FFmpeg..."

if [[ "$OS" == "linux" ]]; then
    sudo apt update
    sudo apt install -y ffmpeg
elif [[ "$OS" == "macos" ]]; then
    brew install ffmpeg
fi

echo "✅ FFmpeg instalado"

# ========================
# 2. Ollama
# ========================

echo "📥 Instalando Ollama..."

if [[ "$OS" == "macos" ]]; then
    curl -fsSL https://ollama.ai/install.sh | sh
else
    curl -fsSL https://ollama.ai/install.sh | sh
fi

echo "✅ Ollama instalado"
echo "⏳ Bajando modelo Mistral (esto puede tomar 10 minutos)..."

ollama pull mistral

echo "✅ Mistral descargado"

# ========================
# 3. Stable Diffusion WebUI
# ========================

echo "📥 Clonando Stable Diffusion WebUI..."

if [ ! -d "stable-diffusion-webui" ]; then
    git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
    cd stable-diffusion-webui
    
    echo "⏳ Primera ejecución (descarga ~5GB)..."
    if [[ "$OS" == "macos" ]]; then
        bash webui.sh &
    else
        bash webui.sh &
    fi
    
    echo "✅ Stable Diffusion WebUI iniciado (http://localhost:7860)"
    cd ..
fi

# ========================
# 4. Piper TTS
# ========================

echo "📥 Instalando Piper TTS..."

pip install piper-tts

echo "⏳ Descargando modelo de voz español..."

piper-tts --download-dir . --voice es_MX-female-medium

echo "✅ Piper TTS instalado"

# ========================
# 5. Python Dependencies
# ========================

echo "📥 Instalando dependencias Python..."

cd apps/ai
pip install -r requirements.txt

echo "✅ Dependencias instaladas"

# ========================
# Finish
# ========================

echo ""
echo "🎉 Setup completado!"
echo ""
echo "Próximos pasos:"
echo "1. Asegúrate que Ollama está corriendo: ollama serve"
echo "2. Asegúrate que Stable Diffusion está corriendo: http://localhost:7860"
echo "3. Inicia el servicio: python apps/ai/app/main.py"
echo "4. Prueba: curl http://localhost:8000/health"
echo ""
