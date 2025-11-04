from datetime import datetime
from typing import Optional

def validate_date_format(date_str: str) -> bool:
    """
    Validar formato de fecha YYYY-MM-DD
    
    Args:
        date_str: Cadena con la fecha
        
    Returns:
        bool: True si el formato es válido
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_past_date(date_str: str) -> bool:
    """
    Verificar si una fecha es del pasado
    
    Args:
        date_str: Cadena con la fecha
        
    Returns:
        bool: True si es una fecha pasada
    """
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date < datetime.now()
    except ValueError:
        return False
