from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import asyncio
import uuid
from datetime import datetime
from pathlib import Path

from app.config import settings
from app.models.capsule import (
    VideoGenerationRequest,
    VideoGenerationResponse,
    VideoStatus
)
from app.services.video_generator import VideoGenerator
from app.utils.ffmpeg_handler import FFmpegHandler

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="RewindDay AI Service",
    description="Generación de videos con IA gratuita",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servicio
video_generator = VideoGenerator(videos_dir="videos")

# Estado de trabajos
generation_jobs = {}

# ========================
# HEALTH CHECK
# ========================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    
    # Verificar FFmpeg
    ffmpeg_ok = FFmpegHandler.check_ffmpeg_installed()
    
    # Verificar Ollama
    ollama_ok = False
    try:
        import requests
        resp = requests.get("http://localhost:11434/api/tags", timeout=2)
        ollama_ok = resp.status_code == 200
    except:
        ollama_ok = False
    
    return {
        "service": "RewindDay AI",
        "status": "ok" if ffmpeg_ok and ollama_ok else "warning",
        "ffmpeg": "✅" if ffmpeg_ok else "❌",
        "ollama": "✅" if ollama_ok else "❌",
        "timestamp": datetime.now().isoformat()
    }

# ========================
# GENERACIÓN DE VIDEOS
# ========================

@app.post("/api/videos/generate", response_model=VideoGenerationResponse)
async def generate_video(
    request: VideoGenerationRequest,
    background_tasks: BackgroundTasks
):
    """
    Inicia generación de video
    Retorna inmediatamente con ID del job
    """
    
    try:
        # Generar ID único
        video_id = str(uuid.uuid4())
        
        # Guardar job state
        generation_jobs[video_id] = {
            "status": "queued",
            "progress": 0,
            "message": "Video en cola",
            "created_at": datetime.now()
        }
        
        # Ejecutar generación en background
        background_tasks.add_task(
            generate_video_background,
            video_id,
            request.title,
            request.context
        )
        
        logger.info(f"Video queued: {video_id}")
        
        return VideoGenerationResponse(
            id=video_id,
            title=request.title,
            status="queued",
            progress=0,
            created_at=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def generate_video_background(video_id: str, title: str, context: str):
    """
    Genera video en background
    """
    try:
        generation_jobs[video_id]["status"] = "generating"
        generation_jobs[video_id]["progress"] = 10
        
        # Generar video
        result = await video_generator.generate_full_video(
            video_id,
            context,
            title
        )
        
        # Actualizar estado
        if result["status"] == "completed":
            generation_jobs[video_id] = {
                "status": "completed",
                "progress": 100,
                "video_url": result["video_url"],
                "message": "Video completado",
                "created_at": generation_jobs[video_id]["created_at"]
            }
        else:
            generation_jobs[video_id] = {
                "status": "failed",
                "progress": 0,
                "error": result.get("error"),
                "message": "Error en generación",
                "created_at": generation_jobs[video_id]["created_at"]
            }
            
    except Exception as e:
        logger.error(f"Error generating video: {e}")
        generation_jobs[video_id] = {
            "status": "failed",
            "progress": 0,
            "error": str(e),
            "message": f"Error: {str(e)}",
            "created_at": generation_jobs[video_id]["created_at"]
        }

# ========================
# OBTENER ESTADO
# ========================

@app.get("/api/videos/{video_id}/status", response_model=VideoStatus)
async def get_video_status(video_id: str):
    """
    Obtiene estado de generación
    """
    
    if video_id not in generation_jobs:
        raise HTTPException(status_code=404, detail="Video not found")
    
    job = generation_jobs[video_id]
    
    return VideoStatus(
        id=video_id,
        status=job["status"],
        progress=job["progress"],
        message=job["message"]
    )

# ========================
# DESCARGAR VIDEO
# ========================

@app.get("/api/videos/{video_id}/download")
async def download_video(video_id: str):
    """
    Descarga video generado
    """
    
    video_path = Path("videos") / f"{video_id}.mp4"
    
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    
    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=f"{video_id}.mp4"
    )

# ========================
# LISTAR VIDEOS
# ========================

@app.get("/api/videos")
async def list_videos():
    """
    Lista todos los videos generados
    """
    
    videos_dir = Path("videos")
    videos = []
    
    for video_file in videos_dir.glob("*.mp4"):
        video_id = video_file.stem
        job = generation_jobs.get(video_id, {})
        
        videos.append({
            "id": video_id,
            "filename": video_file.name,
            "size_mb": video_file.stat().st_size / (1024 * 1024),
            "status": job.get("status", "unknown"),
            "created_at": job.get("created_at")
        })
    
    return {"videos": videos, "total": len(videos)}

# ========================
# ELIMINAR VIDEO
# ========================

@app.delete("/api/videos/{video_id}")
async def delete_video(video_id: str):
    """
    Elimina video generado
    """
    
    video_path = Path("videos") / f"{video_id}.mp4"
    
    if video_path.exists():
        video_path.unlink()
        if video_id in generation_jobs:
            del generation_jobs[video_id]
        return {"message": "Video deleted"}
    
    raise HTTPException(status_code=404, detail="Video not found")

# ========================
# HERRAMIENTAS
# ========================

@app.get("/api/tools/check")
async def check_tools():
    """
    Verifica que todas las herramientas estén instaladas
    """
    
    checks = {
        "ffmpeg": FFmpegHandler.check_ffmpeg_installed(),
        "ollama": False,
        "piper": False,
        "musicgen": False
    }
    
    # Verificar Ollama
    try:
        import requests
        resp = requests.get("http://localhost:11434/api/tags", timeout=2)
        checks["ollama"] = resp.status_code == 200
    except:
        checks["ollama"] = False
    
    # Verificar Piper
    try:
        subprocess.run(["piper", "--version"], capture_output=True, check=True)
        checks["piper"] = True
    except:
        checks["piper"] = False
    
    # Verificar MusicGen
    try:
        from audiocraft.models import MusicGen
        checks["musicgen"] = True
    except:
        checks["musicgen"] = False
    
    all_ok = all(checks.values())
    
    return {
        "status": "ok" if all_ok else "warning",
        "checks": checks,
        "message": "All tools ready" if all_ok else "Some tools missing"
    }

# ========================
# ROOT
# ========================

@app.get("/")
async def root():
    return {
        "service": "RewindDay AI Service",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )
