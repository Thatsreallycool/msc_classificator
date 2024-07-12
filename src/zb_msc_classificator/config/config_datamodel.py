from pydantic import BaseModel, validator
from enum import Enum


class FilterDocuments(BaseModel):
    publication_year_start: int = 2000
    state: str = "j"


class Language(Enum):
    english = 'en'


class TrainingSource(Enum):
    csv = "csv"
    elastic_live = "elastic_live"
    elastic_snapshot = "elastic_snapshot"




