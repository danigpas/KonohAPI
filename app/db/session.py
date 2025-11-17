from app.config.settings import settings
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DATABASE_URL: str = settings.DATABASE_URL

# Crear el engine asíncrono
# El engine es el "gerente" de conexiones a la BD
# echo=False significa que NO muestra las queries en la terminal
# (cámbialo a True si quieres ver qué queries ejecuta)
engine = create_async_engine(
    DATABASE_URL,  # ← URL de settings
    echo=False,
    future=True
)

# Crear la factory de sesiones asíncronas
# Esta "factory" es como una máquina que produce sesiones nuevas cuando las necesites
async_session = async_sessionmaker(
    engine,                    # ← usa el engine creado arriba
    class_=AsyncSession,       # ← produce sesiones asíncronas
    expire_on_commit=False,    # ← los datos siguen siendo válidos después de commit
    autoflush=False            # ← no guarda automáticamente (tú controlas cuándo hacer commit)
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Proporciona una sesión asíncrona a los endpoints.
    
    FastAPI automáticamente:
    1. Llama esta función.
    2. Te da la sesión.
    3. Cuando terminas, cierra la sesión.
    """
    async with async_session() as session: # Al usar una clausula with nos aseguramos que la session se maneja correctamente y libera la memoria al finalizar su ejecucion
        try:
            yield session  # ← proporciona la sesión al endpoint
        except Exception:
            await session.rollback() # Si hay un error se deshacen los cambios
            raise #Se relanza la excepcion para que FastAPI la maneje
        
