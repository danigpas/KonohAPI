from pydantic import BaseModel
from typing import Optional, List

class CharacterCreate(BaseModel):
    name: str
    full_name: Optional[str] = None
    external_id: Optional[str] = None
    rank: Optional[str] = None
    clan_id: Optional[int] = None

class CharacterRead(BaseModel):
    id: int
    name: str
    full_name: Optional[str]
    rank: Optional[str]
    clan_id: Optional[int]