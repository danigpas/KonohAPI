from fastapi import APIRouter,status
from ..models.schemas import CharacterCreate, CharacterRead
from typing import List

router = APIRouter(prefix='/characters',tags=['characters'])

@router.get('/',response_model=List[CharacterRead],status_code=status.HTTP_200_OK)
async def list_all_characters():
    characters_list = [{'id':1,'name': 'naruto','full_name':'naruto uzumaki','rank': '1','clan_id': 4},
                       {'id':2,'name': 'sasuke','full_name':'sasuke uchiha','rank': '2','clan_id': 1

    }]
    return characters_list