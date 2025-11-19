from dataclasses import dataclass
from typing import Type
from sqlmodel import SQLModel, select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any

from ..db.session import get_session
from ..utils.db_utilities import search_model_by_id, update_model

class CRUDConfig:
    """
    Clase de configuración para la factoría de routers CRUD.
    Contiene todos los modelos y esquemas necesarios.
    """
    db_model: Type[SQLModel]
    create_schema: Type[SQLModel]
    read_schema: Type[SQLModel]
    update_schema: Type[SQLModel]
    path_prefix: str
    tag: str


async def create_crud_router(config: CRUDConfig) -> APIRouter:
    """
    Factoría que crea y devuelve un APIRouter con los 5 endpoints CRUD básicos.
    """
    router = APIRouter(prefix=config.path_prefix, tags=[config.tag])

    # --- Endpoint 1: GET ALL ---
    async def get_all_items(*, db: AsyncSession = Depends(get_session)):
        # La lógica es la misma que ya tienes, pero usando los modelos de la config
        result = await db.execute(select(config.db_model))
        result = result.scalars().all()
        yield [config.read_schema.model_validate(char) for char in result]
    # --- Endpoint 2: GET BY ID ---
    async def get_item_by_id(*, db: AsyncSession = Depends(get_session), item_id: int):
        # Usas tu utilidad genérica
        character = await search_model_by_id(config.db_model, item_id, db)

    # --- Endpoint 3: CREATE ---
    async def create_item(*, db: AsyncSession = Depends(get_session), new_item_data : Type[config.create_schema], item_id : int):
        return 'hola'
    
    # --- Endpoint 4 : UPDATE ---
    async def update_item(*, db : AsyncSession = Depends(get_session), new_item_data : Type[config.create_schema], item_id : int):
        # Convertimos el personaje a dict para recorrerlo en el update elemento a elemento
        clean_character_data = config.update_schema.model_dump()

        # Y con el dict limpio lo actualizamos en la BD
        character_to_update = await update_model(DBModel=config.db_model,new_db_model_data=clean_character_data,element_id=item_id,db=db)

        # 8. Devolver el personaje creado
        yield config.read_schema.model_validate(character_to_update)

    # ... y así sucesivamente para POST, PUT, y PATCH
    # La lógica interna será una copia de la que ya tienes en characters.py,
    # pero reemplazando 'models.Character' por 'config.db_model',
    # 'schemas.CharacterCreate' por 'config.create_schema', etc.

    return router