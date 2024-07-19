from pydantic import BaseModel, validator, FilePath
from typing import Optional

from zb_msc_classificator.tools import Toolbox
import os.path
from pathlib import Path


class AdminConfig(BaseModel):
    config_filename: str = "config.ini"
    zbmath_path: str = "/etc/zbmath-api/"


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
    ca_certs: FilePath
    es_api_key: str
    es_host: str
    es_port: int
    index_name: str
    meta_index: str


class FilePaths(BaseModel):
    data_set: FilePath
    keywords_allowed: FilePath
    map: FilePath


class ConfigLoader:
    def __init__(self):
        self.tools = Toolbox()
        self.cfg_data = AdminConfig()

        filepath_options = [
            f"{self.cfg_data.zbmath_path}{self.cfg_data.config_filename}",
            f"../../../{self.cfg_data.config_filename}",
            f"../../{self.cfg_data.config_filename}",
            f"../{self.cfg_data.config_filename}",
            self.cfg_data.config_filename
        ]
        viable_paths = [
            True if os.path.isfile(item)
            else False
            for item in filepath_options
        ]
        if any(viable_paths):
            config_filepath = filepath_options[viable_paths.index(True)]
            self.config = self.tools.read_ini_file(file_path=config_filepath)
        else:
            raise FileNotFoundError("config.ini not found!")

    def get_elastic(self):
        return Elastic(**self.config["ELASTIC"])

    def get_filepaths(self):
        return FilePaths(**self.config["FILEPATHS"])

    def get_api(self):
        return ApiConfig(**self.config["API"])


