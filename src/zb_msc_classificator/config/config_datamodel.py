from pydantic import BaseModel
from enum import Enum


class TrainingSource(Enum):
    disk = "disk"
    elastic = "elastic"


class DataFolder(BaseModel):
    load_from: str = None
    save_to: str = None


class FilePathInput(BaseModel):
    stopwords: str = None
    training_data: str = None
    test_data: str = None
    mrmscs: str = None


class FilePathOutput(BaseModel):
    map: str = None
    prediction_text: str = None
    prediction_keyword: str = None
    prediction_refs: str = None


class AdminConfig(BaseModel):
    config_filename: str = "config.ini"
    zbmath_path: str = "/etc/zbmath-api/"
    data_folder: DataFolder = DataFolder()
    filepath_input: FilePathInput = FilePathInput()
    filepath_output: FilePathOutput = FilePathOutput()
