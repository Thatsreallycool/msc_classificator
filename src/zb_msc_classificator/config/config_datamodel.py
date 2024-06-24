from pydantic import BaseModel, validator
from enum import Enum


class Language(Enum):
    english = 'en'


class TrainingSource(Enum):
    elastic_live = "elastic_live"
    elastic_snapshot = "elastic_snapshot"
    csv = "csv"


class DataFolder(BaseModel):
    load_from: str = None
    save_to: str = None


class FilePathInput(BaseModel):
    stopwords: str = None
    csv_training_data: str = None
    test_data: str = None
    mrmscs: str = None


class FilePathOutput(BaseModel):
    map: str = None
    data_elastic: str = None
    prediction_text: str = None
    prediction_keyword: str = None
    prediction_refs: str = None


class Elastic(BaseModel):
    es_host: str = None
    es_port: str = None
    es_api_key: str = None
    ca_certs: str = None
    index_name: str = None


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


class AdminConfig(BaseModel):
    config_filename: str = "config.ini"
    zbmath_path: str = "/etc/zbmath-api/"
    data_folder: DataFolder = DataFolder()
    filepath_input: FilePathInput = FilePathInput()
    filepath_output: FilePathOutput = FilePathOutput()
    elastic: Elastic = Elastic()
    api_config: ApiConfig = ApiConfig()

