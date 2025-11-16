from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone

class CharacterJutsuLink(SQLModel, table=True):
    character_id: Optional[int] = Field(default=None, foreign_key="character.id", primary_key=True)
    jutsu_id: Optional[int] = Field(default=None, foreign_key="jutsu.id", primary_key=True)
    learned_in_episode: Optional[int] = None

class Clan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    members: List["Character"] = Relationship(back_populates="clan")

class Jutsu(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: Optional[str] = None
    rank: Optional[str] = None
    users: List["Character"] = Relationship(back_populates="jutsus", link_model=CharacterJutsuLink)

class Character(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: Optional[str] = None
    name: str
    full_name: Optional[str] = None
    rank: Optional[str] = None
    clan_id: Optional[int] = Field(default=None, foreign_key="clan.id")
    clan: Optional[Clan] = Relationship(back_populates="members")
    jutsus: List[Jutsu] = Relationship(back_populates="users", link_model=CharacterJutsuLink)
    biography: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory = lambda : datetime.now(timezone.utc))