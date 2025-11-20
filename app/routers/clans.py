from fastapi import APIRouter,status, Depends, HTTPException
from sqlmodel import select

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

