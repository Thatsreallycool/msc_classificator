from pydantic import BaseModel, validator, FilePath
from typing import Optional


class ApiConfig(BaseModel):
    root_path: Optional[str] = None

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
    ca_certs: Optional[str] = None
    es_api_key: Optional[str] = None
    es_host: Optional[str] = None
    es_port: Optional[str] = None
    index_name: Optional[str] = None
    meta_index: Optional[str] = None


class FilePaths(BaseModel):
    data_set: Optional[str] = None
    keywords_allowed: Optional[str] = None
    map: Optional[str] = None


class AdminConfig(BaseModel):
    api_config: ApiConfig = ApiConfig()
    config_filename: str = "config.ini"
    elastic: Elastic = Elastic()
    file_paths: FilePaths = FilePaths()
    zbmath_path: str = "/etc/zbmath-api/"

