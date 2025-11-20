from sqlmodel import SQLModel
from typing import Optional

class CharacterCreate(SQLModel):
    name: str
    full_name: Optional[str] = None
    external_id: Optional[str] = None
    rank: Optional[str] = None
    clan_id: Optional[int] = None
    biography : Optional[str] = None
    image_url : Optional[str] = None

class CharacterRead(SQLModel):
    """Personaje tal como se devuelve de la BD"""
    id: int
    name: str
    full_name: Optional[str]
    rank: Optional[str]
    clan_id: Optional[int]
    biography : Optional[str]
    image_url : Optional[str]

class CharacterUpdate(SQLModel):
    name: Optional[str] = None
    full_name: Optional[str] = None
    rank: Optional[str] = None
    clan_id: Optional[int] = None
    biography: Optional[str] = None
    image_url: Optional[str] = None

# Clan Schemas
class ClanCreate(SQLModel):
    name: str
    description: Optional[str] = None

class ClanRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None

class ClanUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None

# Jutsu Schemas
class JutsuCreate(SQLModel):
    name: str
    type: Optional[str] = None
    rank: Optional[str] = None

class JutsuRead(SQLModel):
    id: int
    name: str
    type: Optional[str] = None
    rank: Optional[str] = None

class JutsuUpdate(SQLModel):
    name: Optional[str] = None
    type: Optional[str] = None
    rank: Optional[str] = None