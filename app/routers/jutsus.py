from fastapi import APIRouter,status, Depends, HTTPException
from sqlmodel import select

from ..utils.db_utilities import search_model_by_id, update_model
from ..models.schemas import JutsuCreate, JutsuRead, JutsuUpdate
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_session
from ..models.db_models import Jutsu
from .crud_router import create_crud_router, CRUDConfig

#Definimos la configuracion de personajes
jutsu_config = CRUDConfig(
    db_model = Jutsu,
    create_schema = JutsuCreate,
    read_schema = JutsuRead,
    update_schema = JutsuUpdate,
    path_prefix = "/jutsus",
    tag = "Jutsus"
)

#Definimos el router de characters
router = create_crud_router(config=jutsu_config)

