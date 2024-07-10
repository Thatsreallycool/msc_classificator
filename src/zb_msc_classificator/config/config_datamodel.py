from pydantic import BaseModel, validator
from enum import Enum

import os


class FilterDocuments(BaseModel):
    publication_year_start: int = None
    state: str = None


class Language(Enum):
    english = 'en'


class TrainingSource(Enum):
    elastic_live = "elastic_live"
    elastic_snapshot = "elastic_snapshot"
    csv = "csv"


class ApiConfig(BaseModel):
    root_path: str = None

    @validator("root_path", always=True)
    def no_slash_at_end(cls, path):
        if path is not None:
            if path.endswith("/"):
                raise ValueError("root_path may not end with /")
            else:
                return path
        else:
            return None


class Elastic(BaseModel):
    es_host: str = None
    es_port: str = None
    es_api_key: str = None
    ca_certs: str = None
    index_name: str = None


class FilePaths(BaseModel):
    data_set: str = None
    keywords_allowed: str = None
    lemmatizer: str = None
    map: str = None
    stopwords_denied: str = None


class AdminConfig(BaseModel):
    api_config: ApiConfig = ApiConfig()
    config_filename: str = "config.ini"
    elastic: Elastic = Elastic()
    file_paths: FilePaths = FilePaths()
    zbmath_path: str = "/etc/zbmath-api/"



