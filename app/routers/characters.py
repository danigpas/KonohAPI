from fastapi import APIRouter,status, Depends, HTTPException
from sqlmodel import select

from ..utils.db_utilities import search_model_by_id, update_model
from ..models.schemas import CharacterCreate, CharacterRead, CharacterUpdate
from typing import Dict, List
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


@router.get('/{character_id}', response_model=CharacterRead, status_code= status.HTTP_200_OK)
async def get_character_by_id(character_id : int, session : AsyncSession = Depends(get_session)) -> CharacterRead :
    """
    Recupera un personaje en base a su id

    Returns:
        CharacterRead
    """

    character = await search_model_by_id(Character,character_id,session)
    
    # 4. Convertir la respuesta a Pydantic y retornarla
    return CharacterRead.model_validate(character)


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



@router.delete('/{character_id}', status_code= status.HTTP_204_NO_CONTENT)
async def delete_character_by_id(character_id : int, session : AsyncSession = Depends(get_session)) :
    """
    Recupera un personaje en base a su id y lo elimina de la BD.
    """

    character_to_delete = await search_model_by_id(Character,character_id,session)

    #  Una vez que tenemos el personaje, lo eliminamos de la BD
    await session.delete(character_to_delete)
    await session.commit()


@router.put('/{character_id}',response_model=CharacterRead,status_code=status.HTTP_200_OK)
async def update_character(character_id : int ,character_data : CharacterCreate, session : AsyncSession = Depends(get_session)) -> CharacterRead:
    """
    Busca un personaje en la BD y lo actualiza con todos los datos dados.
    
    Pasos:

    """
    # Convertimos el personaje a dict para recorrerlo en el update elemento a elemento
    clean_character_data = character_data.model_dump()

    # Y con el dict limpio lo actualizamos en la BD
    character_to_update = await update_model(DBModel=Character,new_db_model_data=clean_character_data,element_id=character_id,db=session)

    # 8. Devolver el personaje creado
    return CharacterRead.model_validate(character_to_update)


@router.patch('/{character_id}',response_model=CharacterRead,status_code=status.HTTP_200_OK)
async def update_character_value(character_id : int ,character_new_value : CharacterUpdate, session : AsyncSession = Depends(get_session)) -> CharacterRead:
    """
    Busca un personaje en la BD y actualiza solamente el dato pasado por el cliente.
    """

    # Al ser un patch primero limpiamos los campos que no nos ha pasado el usuario, para no sobreescribirlos a None
    clean_character_data = character_new_value.model_dump(exclude_unset=True)
    
    # Y con el dict limpio lo actualizamos en la BD
    character_to_update = await update_model(DBModel=Character,new_db_model_data=clean_character_data,element_id=character_id,db=session)
    
    # 8. Devolvemos el personaje creado
    return CharacterRead.model_validate(character_to_update)