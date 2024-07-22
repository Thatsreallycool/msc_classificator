from pydantic import BaseModel, validator
from enum import Enum
from typing import Optional


class FilterDocuments(BaseModel):
    publication_year_start: Optional[int] = 2000
    state: Optional[str] = "j"


class Language(Enum):
    english = 'en'


class TrainingSource(Enum):
    csv = "csv"
    elastic_live = "elastic_live"
    elastic_snapshot = "elastic_snapshot"




