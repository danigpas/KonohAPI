from dataclasses import dataclass
from typing import Generic, Type, TypeVar
from sqlmodel import SQLModel, select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any

from ..db.session import get_session
from ..utils.db_utilities import search_model_by_id, update_model


# 1. Definimos nuestros marcadores de posición de tipo (TypeVars)
DbModelType = TypeVar("DbModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)

# 2. Hacemos que CRUDConfig sea una clase genérica
class CRUDConfig(Generic[DbModelType, CreateSchemaType, ReadSchemaType, UpdateSchemaType]):
    """
    Clase de configuración genérica para la factoría de routers CRUD.
    """
    db_model: Type[DbModelType]
    create_schema: Type[CreateSchemaType]
    read_schema: Type[ReadSchemaType]
    update_schema: Type[UpdateSchemaType]
    path_prefix: str
    tag: str

    
async def create_crud_router(config: CRUDConfig[DbModelType, CreateSchemaType, ReadSchemaType, UpdateSchemaType]) -> APIRouter:
    """
    Factoría que crea y devuelve un APIRouter con los 5 endpoints CRUD básicos.
    """
    router = APIRouter(prefix=config.path_prefix, tags=[config.tag])

    # --- Endpoint 1: GET ALL ---
    async def get_all_items(*, db: AsyncSession = Depends(get_session)):
        
        result = await db.execute(select(config.db_model))
        result = result.scalars().all()
        return [config.read_schema.model_validate(char) for char in result]

    # --- Endpoint 2: GET BY ID ---
    async def get_item_by_id(*, db: AsyncSession = Depends(get_session), item_id: int):
        # Usas tu utilidad genérica
        item = await search_model_by_id(config.db_model, item_id, db)
        return item

    # --- Endpoint 3: CREATE ---
    async def create_item(*, db: AsyncSession = Depends(get_session), new_item_data : CreateSchemaType, item_id : int):
        return 'hola'
    
    # --- Endpoint 4 : UPDATE ---
    async def update_item(*, db : AsyncSession = Depends(get_session), new_item_data : UpdateSchemaType, item_id : int):
        # Convertimos el personaje a dict para recorrerlo en el update elemento a elemento
        clean_character_data = new_item_data.model_dump()

        # Y con el dict limpio lo actualizamos en la BD
        character_to_update = await update_model(DBModel=config.db_model,new_db_model_data=clean_character_data,element_id=item_id,db=db)

        # 8. Devolver el personaje creado
        return config.read_schema.model_validate(character_to_update)

    # --- Endpoint 5 : PATCH ---
    async def update_part_of_item(*, db : AsyncSession = Depends(get_session), new_item_data : UpdateSchemaType, item_id : int):
        # Convertimos el personaje a dict para recorrerlo en el update elemento a elemento
        clean_character_data = new_item_data.model_dump(exclude_unset=True)

        # Y con el dict limpio lo actualizamos en la BD
        character_to_update = await update_model(DBModel=config.db_model,new_db_model_data=clean_character_data,element_id=item_id,db=db)

        # 8. Devolver el personaje creado
        return config.read_schema.model_validate(character_to_update)

    # ... y así sucesivamente para POST, PUT, y PATCH
    # La lógica interna será una copia de la que ya tienes en characters.py,
    # pero reemplazando 'models.Character' por 'config.db_model',
    # 'schemas.CharacterCreate' por 'config.create_schema', etc.

    return router