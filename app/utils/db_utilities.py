from sqlmodel import select,SQLModel
from fastapi import HTTPException, status
from typing import TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession

model_type = TypeVar("model_type",bound=SQLModel)

async def search_model_by_id(DBModel : Type[model_type] , element_id : int, db : AsyncSession) -> model_type :
    """
    Obtiene un elemento de la base de datos por su ID.
    Lanza HTTPException 404 si no se encuentra.
    """
    # Hacemos un get que esta depurado para buscar en base a la PK de la tabla (la cual deberemos de pasar como element_id)
    element = await db.get(DBModel,element_id)
    
    # Manejo del 404
    if not element:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Error, resultado del modelo {DBModel} no encontrado con el id : {element_id}')
    
    return element