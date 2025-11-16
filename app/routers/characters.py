from fastapi import APIRouter,status, Depends, HTTPException
from sqlalchemy import select
from ..models.schemas import CharacterCreate, CharacterRead
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_session
from ..models.db_models import Character

router = APIRouter(prefix='/characters',tags=['characters'])

@router.get('', response_model=List[CharacterRead], status_code=status.HTTP_200_OK)
async def list_all_characters(session: AsyncSession = Depends(get_session)) -> List[CharacterRead]:
    """
    Recupera todos los personajes de la base de datos.
    
    Returns:
        List[CharacterRead]: Lista de personajes con sus datos básicos.
    """
    # Construir y ejecutar la consulta SELECT
    query = select(Character)
    result = await session.execute(query)
    characters = result.scalars().all()
    
    # Convertir objetos ORM a esquemas Pydantic
    return [CharacterRead.model_validate(char) for char in characters]



@router.post('',response_model=CharacterRead,status_code=status.HTTP_201_CREATED)
async def create_character(character_data : CharacterCreate, session : AsyncSession = Depends(get_session)) -> CharacterRead:
    """
    Crea un nuevo personaje en la BD.
    
    Pasos:
    1. Recibe character_data (CharacterCreate).
    2. Crea instancia de Character.
    3. La añade a la sesión.
    4. Hace commit.
    5. Devuelve CharacterRead con el id asignado.
    """
    # 1. Crear la instancia de Character a partir de los datos recibidos
    new_character = Character(
        name = character_data.name,
        full_name= character_data.full_name,
        rank= character_data.rank,
        clan_id= character_data.clan_id,
        biography= character_data.biography,
        image_url= character_data.image_url
    )

    # 2. Agregar la sesion
    session.add(new_character)

    # 3. Guardar en la BD (commit)
    await session.commit()

    # 4. Refrescar el objeto para obtener el ID generado por la BD
    await session.refresh(new_character)

    # 5. Devolver el personaje creado
    return CharacterRead.model_validate(new_character)

