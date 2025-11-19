from sqlmodel import select,SQLModel
from fastapi import HTTPException, status
from typing import TypeVar, Type, Dict, Any
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

async def update_model(DBModel : Type[model_type] ,new_db_model_data : Dict[str,Any], element_id : int, db : AsyncSession) -> model_type:
    """
    Busca un elemento en la BD y actualiza todo el elemento o solo una parte, segun el valor de patch.
    """
    # Buscamos el personaje con la id pasada por el usuario

    character_to_update = await search_model_by_id(DBModel,element_id,db)

    # 4. Recorremos los datos obtenidos de la BD y los modificados por los pasados por el usuario
    
    for key,value in new_db_model_data.items():
        setattr(character_to_update,key,value)

    # 5. Agregar la sesion
    db.add(character_to_update)

    # 6. Guardar en la BD (commit)
    await db.commit()

    # 7. Refrescar el objeto para obtener el ID generado por la BD
    await db.refresh(character_to_update)

    # 8. Devolver el personaje creado
    return character_to_update