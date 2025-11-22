from fastapi import APIRouter,status, Depends, HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload
from ..utils.db_utilities import search_model_by_id, update_model
from ..models.schemas import ClanCreate,ClanRead,ClanUpdate
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_session
from ..models.db_models import Clan
from .crud_router import create_crud_router, CRUDConfig

#Definimos la configuracion de personajes
clan_config = CRUDConfig(
    db_model = Clan,
    create_schema = ClanCreate,
    read_schema = ClanRead,
    update_schema = ClanUpdate,
    path_prefix = "/clans",
    tag = "Clans"
)

#Definimos el router de characters
router = create_crud_router(config=clan_config)

# AÑADIMOS esto al router existente para sobrescribir o extender
@router.get("/{clan_id}/{with_members}", response_model=ClanRead)
async def get_clan_with_members(clan_id: int, db: AsyncSession = Depends(get_session),with_members: bool = False):
    # Usamos selectinload para traer los miembros en la misma consulta de forma eficiente
    query = select(Clan).where(Clan.id == clan_id).options(selectinload(Clan.members) if with_members else None)
    result = await db.execute(query)
    clan = result.scalars().first()
    
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    return clan