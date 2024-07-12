from pydantic import BaseModel, ValidationError, validator, \
    FilePath, DirectoryPath
import os

import nltk
from zb_msc_classificator.tools import Toolbox
import zb_msc_classificator as zbc
from zb_msc_classificator.config.config_datamodel \
    import TrainingSource, Language, FilterDocuments
from zb_msc_classificator.config.admin_config \
    import AdminConfig, FilePaths, Elastic, ApiConfig

from typing import List


class ConfigGeneral(BaseModel):
    admin_config: AdminConfig = AdminConfig()
    language: Language = Language.english

    @validator("admin_config", always=True)
    def confirm_consistency(cls, cfg_data):
        filepath_options = [
            f"{cfg_data.zbmath_path}{cfg_data.config_filename}",
            f"../../../{cfg_data.config_filename}",
            f"../../{cfg_data.config_filename}",
            f"../{cfg_data.config_filename}",
            cfg_data.config_filename
        ]
        viable_paths = [
            True if os.path.isfile(item)
            else False
            for item in filepath_options
        ]
        if any(viable_paths):
            config_filepath = filepath_options[viable_paths.index(True)]
        else:
            raise FileNotFoundError("config.ini not found!")
        admin_cfg = Toolbox().read_ini_file(file_path=config_filepath)

        filepaths = {
            k: f"{admin_cfg['FILEPATHS']['data_folder']}{v}"
            for k, v in admin_cfg["FILEPATHS"].items()
            if not k == 'data_folder'
        }

        return AdminConfig(
            api_config=ApiConfig(**admin_cfg["API"]),
            elastic=Elastic(**admin_cfg["ELASTIC"]),
            file_paths=FilePaths(**filepaths)
        )


class ConfigMap(ConfigGeneral):
    store_data: bool = False
    data_size: int = None
    filter_documents: FilterDocuments = FilterDocuments()

    @validator("data_size", always=True)
    def int_gt0(cls, number):
        minimum_jump = 10000
        if number is None:
            return minimum_jump
        elif number <= 0:
            return minimum_jump
        elif number > 0:
            return number
        else:
            raise ValueError(
                "data size addendum for datablob must be bigger than zero"
            )


class ConfigGenerate(ConfigGeneral):
    training_source: TrainingSource = None
    store_map: bool = False


class ConfigClassify(ConfigGeneral):
    nr_msc_cutoff: int = 10

    @validator("nr_msc_cutoff")
    def msc_cutoff_pos_int(cls, val):
        if val < 1:
            raise ValueError("must be positive")
        return val


class ConfigEvaluate(ConfigGeneral):
    pass


class ConfigEntityLinking(ConfigGeneral):
    map_file: str = None
    ngram_lengths: List[int] = [2, 3]
    sparql_link: str = "https://query.wikidata.org/sparql"

    @validator("ngram_lengths", always=True)
    def check_positivity(cls, cfg_data):
        if all(
            [
                True if item > 0
                else False
                for item in cfg_data
            ]
        ):
            return cfg_data
        else:
            raise ValueError("values must always be int pos")


class ConfigHarmonize(ConfigGeneral):
    use_stopwords: bool = True
    custom_stopwords_filepath: str = "/data/stopwords.txt"
    nltk_directory: str = "/nltk_data"

    @validator("use_stopwords", always=True)
    def check_for_nltk_data_path(cls, use_stopwords):
        if use_stopwords:
            package_path = os.path.dirname(zbc.__file__)
            nltk.data.path = [f"{package_path}/../nltk_data"]
        return use_stopwords

    @validator("custom_stopwords_filepath", always=True)
    def prefix_project_path(cls, custom_path):
        return f"{os.path.dirname(zbc.__file__)}/..{custom_path}"
