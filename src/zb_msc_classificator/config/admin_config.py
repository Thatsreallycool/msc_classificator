from pydantic import BaseModel, validator


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
    ca_certs: str = None
    es_api_key: str = None
    es_host: str = None
    es_port: str = None
    index_name: str = None
    meta_index: str = None


class FilePaths(BaseModel):
    data_set: str = None
    keywords_allowed: str = None
    map: str = None


class AdminConfig(BaseModel):
    api_config: ApiConfig = ApiConfig()
    config_filename: str = "config.ini"
    elastic: Elastic = Elastic()
    file_paths: FilePaths = FilePaths()
    zbmath_path: str = "/etc/zbmath-api/"

