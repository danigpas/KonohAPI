from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

class Settings:
    """
    Centraliza todas las configuraciones de la aplicación.
    Lee variables de .env y las valida.
    """
    # Base de datos
    DATABASE_URL : str = os.getenv('DATABASE_URL','')
    # Validaciones
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL no está configurada en .env")


# Crear una instancia global para usar en toda la app
settings = Settings()