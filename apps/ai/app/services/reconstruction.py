from typing import Optional
from datetime import datetime, timedelta
import random
import logging

from app.models.capsule import CapsuleReconstruction, ReconstructedEvent

logger = logging.getLogger(__name__)

class ReconstructionService:
    """
    Servicio para reconstruir días del pasado usando IA.
    
    NOTA: Esta es una implementación de ejemplo/demo.
    En producción, aquí integrarías con:
    - OpenAI GPT para análisis de lenguaje natural
    - APIs de redes sociales para obtener posts del día
    - Google Calendar API para eventos
    - APIs de clima histórico
    - Fotos y ubicaciones del día
    """
    
    def __init__(self):
        self.moods = [
            "Feliz y energético",
            "Reflexivo y tranquilo",
            "Motivado y productivo",
            "Relajado y social",
            "Nostálgico y pensativo"
        ]
        
        self.weather_conditions = [
            "Soleado ☀️",
            "Nublado ☁️",
            "Lluvioso 🌧️",
            "Parcialmente nublado ⛅",
            "Despejado 🌤️"
        ]
        
        self.event_categories = {
            "work": ["Reunión importante", "Proyecto completado", "Llamada de trabajo"],
            "personal": ["Ejercicio matutino", "Lectura", "Meditación"],
            "social": ["Café con amigos", "Cena familiar", "Videollamada"],
            "entertainment": ["Película", "Serie", "Videojuegos"],
            "learning": ["Curso online", "Tutorial", "Podcast educativo"]
        }
    
    async def reconstruct_day(
        self,
        date: str,
        title: str,
        description: Optional[str] = None
    ) -> CapsuleReconstruction:
        """
        Reconstruir un día del pasado.
        
        Args:
            date: Fecha en formato YYYY-MM-DD
            title: Título de la cápsula
            description: Descripción opcional
            
        Returns:
            CapsuleReconstruction: Reconstrucción completa del día
        """
        logger.info(f"Starting reconstruction for {date}: {title}")
        
        # Validar fecha
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Formato de fecha inválido. Usa YYYY-MM-DD")
        
        # Verificar que no sea una fecha futura
        if target_date > datetime.now():
            raise ValueError("No se puede reconstruir una fecha futura")
        
        # Generar reconstrucción
        # NOTA: Aquí es donde integrarías con GPT, APIs, etc.
        events = self._generate_events(target_date, description)
        highlights = self._generate_highlights(events, title)
        mood = random.choice(self.moods)
        weather = random.choice(self.weather_conditions)
        summary = self._generate_summary(date, title, mood, len(events))
        ai_insights = self._generate_insights(events, mood)
        
        reconstruction = CapsuleReconstruction(
            summary=summary,
            highlights=highlights,
            mood=mood,
            weather=weather,
            events=events,
            ai_insights=ai_insights
        )
        
        logger.info(f"Successfully reconstructed day: {date}")
        return reconstruction
    
    def _generate_events(
        self,
        date: datetime,
        description: Optional[str]
    ) -> list[ReconstructedEvent]:
        """Generar eventos del día (DEMO - reemplazar con IA real)"""
        events = []
        
        # Generar 4-8 eventos del día
        num_events = random.randint(4, 8)
        start_hour = 8
        
        for i in range(num_events):
            hour = start_hour + (i * 2)
            minute = random.choice([0, 15, 30, 45])
            time = f"{hour:02d}:{minute:02d}"
            
            category = random.choice(list(self.event_categories.keys()))
            event_desc = random.choice(self.event_categories[category])
            
            # Si hay descripción, incorporarla en el primer evento
            if i == 0 and description:
                event_desc = f"{event_desc}: {description}"
            
            events.append(ReconstructedEvent(
                time=time,
                description=event_desc,
                category=category,
                importance=random.randint(2, 5)
            ))
        
        return events
    
    def _generate_highlights(
        self,
        events: list[ReconstructedEvent],
        title: str
    ) -> list[str]:
        """Generar momentos destacados"""
        # Tomar los eventos más importantes
        important_events = sorted(events, key=lambda e: e.importance, reverse=True)[:3]
        
        highlights = [f"{title} - Un día memorable"]
        highlights.extend([
            f"{event.description} a las {event.time}"
            for event in important_events
        ])
        
        return highlights
    
    def _generate_summary(
        self,
        date: str,
        title: str,
        mood: str,
        num_events: int
    ) -> str:
        """Generar resumen del día"""
        return (
            f"El {date} fue un día especial marcado por '{title}'. "
            f"Tu estado de ánimo general fue {mood.lower()}, "
            f"y registramos {num_events} eventos significativos a lo largo del día. "
            f"Fue un día lleno de actividades y momentos memorables."
        )
    
    def _generate_insights(
        self,
        events: list[ReconstructedEvent],
        mood: str
    ) -> str:
        """Generar insights de IA"""
        work_events = len([e for e in events if e.category == "work"])
        social_events = len([e for e in events if e.category == "social"])
        
        insights = [
            f"Tu día estuvo equilibrado con {work_events} eventos de trabajo "
            f"y {social_events} momentos sociales.",
            f"El estado de ánimo '{mood}' sugiere que fue un día positivo y productivo.",
            "Los eventos de mayor importancia ocurrieron durante las horas centrales del día."
        ]
        
        return " ".join(insights)
