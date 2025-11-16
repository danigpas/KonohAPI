from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class CharacterCreate(BaseModel):
    name: str
    full_name: Optional[str] = None
    external_id: Optional[str] = None
    rank: Optional[str] = None
    clan_id: Optional[int] = None
    biography : Optional[str] = None
    image_url : Optional[str] = None

class CharacterRead(BaseModel):
    """Personaje tal como se devuelve de la BD"""
    model_config = ConfigDict(from_attributes=True)  # ← IMPORTANTE
    id: int
    name: str
    full_name: Optional[str]
    rank: Optional[str]
    clan_id: Optional[int]
    biography : Optional[str]
    image_url : Optional[str]