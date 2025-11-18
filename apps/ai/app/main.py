from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import os
from typing import List, Optional
import json
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== CONFIGURACIÓN ====================
app = FastAPI(
    title="RewindDay AI Service",
    description="API para reconstruir un día del pasado usando razonamiento de IA",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de Ollama
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "deepseek-r1:8b")

# Normalizar URL
if "/api" in OLLAMA_API_URL:
    OLLAMA_BASE = OLLAMA_API_URL.split("/api")[0].rstrip("/")
else:
    OLLAMA_BASE = OLLAMA_API_URL.rstrip("/")

print(f"[INIT] Conectando a Ollama en: {OLLAMA_BASE}")
print(f"[INIT] Modelo: {MODEL_NAME}")

# ==================== MODELOS PYDANTIC ====================

class DayEvent(BaseModel):
    """Evento individual del día"""
    time: str
    description: str
    location: Optional[str] = None
    emotional_intensity: Optional[int] = None

class CapsuleData(BaseModel):
    """Datos de la cápsula digital del día"""
    date: str
    events: List[DayEvent]
    mood_notes: str
    key_memories: List[str]

class ReconstructionRequest(BaseModel):
    """Request para reconstruir un día"""
    capsule_data: CapsuleData
    focus_areas: Optional[List[str]] = None
    reasoning_enabled: bool = True
    language: Optional[str] = "es"

class ReconstructionResponse(BaseModel):
    """Response con la reconstrucción del día"""
    date: str
    reconstructed_narrative: str
    thinking_process: str
    key_insights: List[str]
    confidence_score: float

# ==================== ENDPOINTS ====================

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Bienvenido a RewindDay AI Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "reconstruct": "/capsule/reconstruct",
            "generate_video": "/capsule/generate-video",
            "download_video": "/capsule/download-video/{date}"
        }
    }

@app.get("/health")
def health_check():
    """Verifica que Ollama está disponible"""
    try:
        response = requests.get(
            f"{OLLAMA_BASE}/api/tags",
            timeout=15
        )
        
        available = response.status_code == 200
        data = response.json() if available else {}
        models = data.get("models", [])
        
        return {
            "status": "healthy" if available else "degraded",
            "ollama_available": available,
            "model": MODEL_NAME,
            "ollama_url": OLLAMA_BASE,
            "available_models": [m.get("name") for m in models] if models else [],
            "models_count": len(models)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "model": MODEL_NAME,
            "ollama_url": OLLAMA_BASE
        }

@app.post("/capsule/reconstruct", response_model=ReconstructionResponse)
def reconstruct_capsule(request: ReconstructionRequest):
    """
    Reconstruye un día del pasado usando razonamiento de IA con Ollama.
    """
    
    try:
        capsule = request.capsule_data
        
        # Formatear eventos
        events_text = "\n".join([
            f"- {e.time}: {e.description} "
            f"(Ubicación: {e.location if e.location else 'N/A'}, "
            f"Intensidad: {e.emotional_intensity if e.emotional_intensity else 'N/A'}/10)"
            for e in capsule.events
        ])
        
        # Formatear áreas de enfoque
        focus_text = ""
        if request.focus_areas:
            focus_text = f"\n\nÁreas de enfoque:\n" + "\n".join(
                [f"- {area}" for area in request.focus_areas]
            )
        
        # Construir el prompt
        system_prompt = """Eres un experto en análisis psicológico y narrativa. 
Tu tarea es reconstruir una narrativa coherente de un día específico basándote en eventos, 
emociones y memorias fragmentadas.

INSTRUCCIONES:
1. Analiza patrones y conexiones entre eventos
2. Identifica el flujo emocional del día
3. Encuentra momentos pivotes
4. Proporciona insights profundos
5. Responde en español

Sé empático pero analítico."""
        
        user_prompt = f"""INFORMACIÓN DEL DÍA:

Fecha: {capsule.date}

EVENTOS:
{events_text}

NOTAS DE HUMOR:
{capsule.mood_notes}

MEMORIAS CLAVE:
{', '.join(capsule.key_memories)}
{focus_text}

Por favor reconstruye y analiza este día. Proporciona:
1. Narrativa coherente
2. Patrones identificados
3. Momentos pivotes
4. Reflexión emocional
5. Conclusión"""
        
        # Llamar a Ollama
        full_text = f"{system_prompt}\n\nUser: {user_prompt}\n\nAssistant:"
        
        logger.info(f"[REQUEST] Enviando a Ollama: {capsule.date}")
        
        response = requests.post(
            f"{OLLAMA_BASE}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": full_text,
                "stream": False,
                "temperature": 0.7,
            },
            timeout=900
        )
        
        response.raise_for_status()
        result = response.json()
        
        full_response = result.get("response", "")
        
        if not full_response:
            raise Exception("Respuesta vacía de Ollama")
        
        # Procesar insights
        lines = full_response.split("\n")
        key_insights = [
            line.strip("- ").strip() 
            for line in lines 
            if line.strip().startswith("-") and len(line.strip()) > 5
        ]
        key_insights = key_insights[:5] if key_insights else ["Análisis completado"]
        
        # Calcular confidence
        confidence_score = min(1.0, len(full_response) / 2000)
        
        logger.info(f"[SUCCESS] Reconstrucción completada. Score: {confidence_score:.2f}")
        
        return ReconstructionResponse(
            date=capsule.date,
            reconstructed_narrative=full_response,
            thinking_process=full_response[:500],
            key_insights=key_insights,
            confidence_score=confidence_score
        )
        
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=408,
            detail="Timeout: El modelo está tardando demasiado"
        )
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(
            status_code=503,
            detail=f"No se puede conectar a Ollama en {OLLAMA_BASE}: {str(e)}"
        )
    except Exception as e:
        logger.error(f"[ERROR] {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )

@app.post("/capsule/reconstruct/simple")
def simple_reconstruct(capsule_data: CapsuleData):
    """Versión simplificada"""
    
    try:
        events_text = "\n".join([
            f"- {e.time}: {e.description}"
            for e in capsule_data.events
        ])
        
        prompt = f"""Analiza brevemente este día ({capsule_data.date}):

Eventos: 
{events_text}

Notas: {capsule_data.mood_notes}

Proporciona un resumen de 3-4 párrafos."""
        
        response = requests.post(
            f"{OLLAMA_BASE}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
            },
            timeout=900
        )
        
        response.raise_for_status()
        result = response.json()
        
        return {
            "date": capsule_data.date,
            "summary": result.get("response", ""),
            "mode": "simple"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/capsule/generate-video")
def generate_video_from_capsule(request: ReconstructionRequest):
    """
    Genera un video MP4 a partir de la narrativa reconstruida.
    VERSIÓN SIMPLIFICADA Y ROBUSTA
    """
    
    try:
        logger.info("[VIDEO] Iniciando generación de video...")
        
        # Importar aquí para evitar dependencias si no se usan
        try:
            from PIL import Image, ImageDraw, ImageFont
            import numpy as np
            from pathlib import Path
        except ImportError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Falta dependencia: {str(e)}. Instala Pillow: pip install Pillow"
            )
        
        # 1. Primero reconstruir la narrativa
        logger.info("[VIDEO] Reconstruyendo narrativa...")
        reconstruction = reconstruct_capsule(request)
        
        # 2. Extraer datos
        narrative = reconstruction.reconstructed_narrative
        insights = reconstruction.key_insights
        date = reconstruction.date
        
        logger.info("[VIDEO] Narrativa obtenida. Creando slides...")
        
        # 3. Dividir narrativa en secciones
        sections = narrative.split("###")
        sections = [s.strip() for s in sections if s.strip()][:5]  # Máximo 5 secciones
        
        # 4. Crear imágenes (en lugar de video complejo)
        output_dir = Path("/tmp")
        output_dir.mkdir(exist_ok=True)
        
        slides = []
        
        # Slide 1: Título
        img = create_simple_text_image(
            f"Tu Día: {date}",
            width=1280,
            height=720,
            fontsize=80,
            bg_color=(26, 26, 46),
            text_color=(255, 255, 255)
        )
        slide_path = output_dir / f"slide_0_{date}.png"
        img.save(str(slide_path))
        slides.append(str(slide_path))
        logger.info(f"[VIDEO] Slide 1 creada: {slide_path}")
        
        # Slides de narrativa
        for i, section in enumerate(sections):
            text = section[:250]  # Limitar caracteres
            img = create_simple_text_image(
                text,
                width=1280,
                height=720,
                fontsize=35,
                bg_color=(22, 33, 62),
                text_color=(255, 255, 255)
            )
            slide_path = output_dir / f"slide_{i+1}_{date}.png"
            img.save(str(slide_path))
            slides.append(str(slide_path))
            logger.info(f"[VIDEO] Slide {i+2} creada")
        
        # Slide final: Insights
        insights_text = "\n".join([f"• {ins[:100]}" for ins in insights[:3]])
        img = create_simple_text_image(
            f"Insights Clave:\n\n{insights_text}",
            width=1280,
            height=720,
            fontsize=30,
            bg_color=(15, 52, 96),
            text_color=(255, 255, 0)
        )
        slide_path = output_dir / f"slide_final_{date}.png"
        img.save(str(slide_path))
        slides.append(str(slide_path))
        logger.info("[VIDEO] Slide final creada")
        
        # 5. Crear video con ImageIO (más confiable que MoviePy)
        logger.info("[VIDEO] Compilando video...")
        
        try:
            import imageio
            
            output_video = str(output_dir / f"rewindday_{date}.mp4")
            
            # Usar imageio-ffmpeg
            writer = imageio.get_writer(output_video, fps=0.2)  # 1 imagen cada 5 segundos
            
            # Agregar cada slide múltiples veces para duración
            for slide_path in slides:
                img_array = imageio.imread(slide_path)
                for _ in range(1):  # 5 segundos por slide a 0.2 fps
                    writer.append_data(img_array)
            
            writer.close()
            
            logger.info(f"[VIDEO] Video creado: {output_video}")
            
            # 6. Verificar que el archivo existe
            if not os.path.exists(output_video):
                raise Exception("El archivo de video no se creó")
            
            file_size = os.path.getsize(output_video)
            
            return {
                "date": date,
                "video_path": output_video,
                "file_size_mb": round(file_size / (1024*1024), 2),
                "slides_count": len(slides),
                "message": "Video generado exitosamente",
                "download_url": f"/capsule/download-video/{date}"
            }
        
        except ImportError:
            logger.warning("[VIDEO] ImageIO no disponible, usando alternativa...")
            
            # Alternativa: retornar las imágenes
            return {
                "date": date,
                "video_path": None,
                "slides": slides,
                "slides_count": len(slides),
                "message": "Slides generadas (video no disponible - instala imageio-ffmpeg)",
                "instruction": "Instala: pip install imageio-ffmpeg"
            }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERROR] Error generando video: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error generando video: {str(e)}"
        )

def create_simple_text_image(text, width=1280, height=720, fontsize=40, 
                             bg_color=(0, 0, 0), text_color=(255, 255, 255)):
    """
    Crea una imagen simple con texto centrado.
    VERSIÓN ROBUSTA SIN ERRORES DE TUPLA
    """
    from PIL import Image, ImageDraw, ImageFont
    
    # Crear imagen
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Cargar fuente
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontsize)
    except:
        try:
            font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", fontsize)
        except:
            font = ImageFont.load_default()
    
    # Dividir texto en líneas
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = " ".join(current_line + [word])
        # Usar textbbox correctamente
        bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = bbox[2] - bbox[0]
        
        if text_width < width - 100:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(" ".join(current_line))
    
    # Dibujar líneas centradas
    line_height = fontsize + 10
    total_height = len(lines) * line_height
    y_start = (height - total_height) // 2
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (width - line_width) // 2
        y = y_start + i * line_height
        
        draw.text((x, y), line, fill=text_color, font=font)
    
    return img

@app.get("/capsule/download-video/{date}")
def download_video(date: str):
    """Descargar video generado"""
    try:
        video_path = f"/tmp/rewindday_{date}.mp4"
        
        if not os.path.exists(video_path):
            raise HTTPException(404, f"Video no encontrado para la fecha: {date}")
        
        return FileResponse(
            video_path,
            media_type="video/mp4",
            filename=f"rewindday_{date}.mp4"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error descargando video: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )