from fastapi import APIRouter,status, Depends, HTTPException
from sqlmodel import select

from ..utils.db_utilities import search_model_by_id, update_model
from ..models.schemas import CharacterCreate, CharacterRead, CharacterUpdate
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_session
from ..models.db_models import Character
from .crud_router import create_crud_router, CRUDConfig

#Definimos la configuracion de personajes
character_config = CRUDConfig(
    db_model = Character,
    create_schema = CharacterCreate,
    read_schema = CharacterRead,
    update_schema = CharacterUpdate,
    path_prefix = "/characters",
    tag = "Characters"
)

#Definimos el router de characters
router = create_crud_router(config=character_config)

#TODO : Implementar un endpoint para aprender jutsus
