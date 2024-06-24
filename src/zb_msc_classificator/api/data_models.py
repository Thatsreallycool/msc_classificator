from pydantic import BaseModel
from typing import List


class Text(BaseModel):
    text: str = None


class EntityData(BaseModel):
    entity: str = None
    span: List = []
    link: str = None