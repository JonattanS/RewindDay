from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ReconstructedEvent(BaseModel):
    """Evento reconstruido del día"""
    time: str = Field(..., description="Hora del evento (HH:MM)")
    description: str = Field(..., description="Descripción del evento")
    category: str = Field(..., description="Categoría: personal, work, social, etc.")
    importance: int = Field(..., ge=1, le=5, description="Importancia del 1 al 5")

class CapsuleReconstruction(BaseModel):
    """Reconstrucción completa de un día"""
    summary: str = Field(..., description="Resumen general del día")
    highlights: List[str] = Field(..., description="Momentos destacados")
    mood: str = Field(..., description="Estado de ánimo general")
    weather: Optional[str] = Field(None, description="Clima del día")
    events: List[ReconstructedEvent] = Field(..., description="Eventos del día")
    ai_insights: str = Field(..., description="Insights generados por IA")
    generated_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Fecha de generación"
    )

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class VideoScene(BaseModel):
    """Escena de video"""
    number: int
    title: str
    description: str
    narration: str
    duration: int
    mood: str

class VideoScript(BaseModel):
    """Script completo de video"""
    title: str
    scenes: List[VideoScene]

class VideoGenerationRequest(BaseModel):
    """Request para generar video"""
    title: str = Field(..., min_length=5, max_length=255)
    context: str = Field(..., min_length=20, max_length=2000)
    style: Optional[str] = "cinematic"  # professional, cinematic, documentary

class VideoGenerationResponse(BaseModel):
    """Response de generación"""
    id: str
    title: str
    status: str  # queued, generating, completed, failed
    progress: int = 0
    video_url: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime

class VideoStatus(BaseModel):
    """Estado de generación"""
    id: str
    status: str
    progress: int
    message: str
