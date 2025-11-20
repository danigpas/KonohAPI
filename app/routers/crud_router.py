from dataclasses import dataclass
from typing import Generic, Type, TypeVar
from sqlmodel import SQLModel, select
from fastapi import APIRouter, Body, Depends, HTTPException, status
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
@dataclass
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

    
def create_crud_router(config: CRUDConfig[DbModelType, CreateSchemaType, ReadSchemaType, UpdateSchemaType]) -> APIRouter:
    """
    Factoría que crea y devuelve un APIRouter con los 5 endpoints CRUD básicos.
    """
    router = APIRouter(prefix=config.path_prefix, tags=[config.tag])

    # --- Endpoint 1: GET ALL ---
    @router.get('', response_model=List[ReadSchemaType], status_code=status.HTTP_200_OK)
    async def get_all_items(*, db: AsyncSession = Depends(get_session)):
        """
        Obtiene todos los elementos del modelo especificado
        """
        result = await db.execute(select(config.db_model))
        return result.scalars().all()
        

    # --- Endpoint 2: GET BY ID ---
    @router.get('/{item_id}', response_model=ReadSchemaType, status_code= status.HTTP_200_OK)
    async def get_item_by_id(*, db: AsyncSession = Depends(get_session), item_id: int):
        """
        Obtiene un elemento mediante su id
        """
        item = await search_model_by_id(config.db_model, item_id, db)
        return item

    # --- Endpoint 3: CREATE (POST) ---
    @router.post('',response_model=ReadSchemaType,status_code=status.HTTP_201_CREATED)
    async def create_item(*, db: AsyncSession = Depends(get_session), item_in : CreateSchemaType = Body(...)):
        """
        Crea un nuevo elemento
        """
        #Convertimos nuestro objeto en un modelo de BD
        db_item = config.db_model.model_validate(item_in.model_dump())   
        
        #Lo registramos en la BD
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item
    
    # --- Endpoint 4 : UPDATE (PUT)---
    @router.put('/{item_id}',response_model=ReadSchemaType,status_code=status.HTTP_200_OK)
    async def update_item_put(*, db : AsyncSession = Depends(get_session), new_item_data : CreateSchemaType, item_id : int):
        # Convertimos el personaje a dict para recorrerlo en el update elemento a elemento
        clean_character_data = new_item_data.model_dump()

        # Y con el dict limpio lo actualizamos en la BD
        character_to_update = await update_model(DBModel=config.db_model,new_db_model_data=clean_character_data,element_id=item_id,db=db)

        # 8. Devolver el personaje creado
        return character_to_update

    # --- Endpoint 5 : PARTIAL UPDATE (PATCH) ---
    @router.patch('/{item_id}',response_model=ReadSchemaType,status_code=status.HTTP_200_OK)
    async def update_item_patch(*, db : AsyncSession = Depends(get_session), new_item_data : UpdateSchemaType, item_id : int):
        # Convertimos el personaje a dict para recorrerlo en el update elemento a elemento
        clean_character_data = new_item_data.model_dump(exclude_unset=True)

        # Y con el dict limpio lo actualizamos en la BD
        character_to_update = await update_model(DBModel=config.db_model,new_db_model_data=clean_character_data,element_id=item_id,db=db)

        # 8. Devolver el personaje creado
        return character_to_update

    # --- Endpoint 6 : DELETE ---
    @router.delete('/{item_id}', status_code= status.HTTP_204_NO_CONTENT)
    async def delete_item(*, db : AsyncSession = Depends(get_session), item_id : int):
        to_delete = await search_model_by_id(DBModel=config.db_model,element_id=item_id,db=db)
        #  Una vez que tenemos el personaje, lo eliminamos de la BD
        await db.delete(to_delete)
        await db.commit()
    
    return router