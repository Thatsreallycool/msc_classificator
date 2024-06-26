from pydantic import BaseModel, ValidationError, validator
import os
from zb_msc_classificator import read_ini
from zb_msc_classificator.config.config_datamodel \
    import AdminConfig, FilePaths, \
    TrainingSource, Elastic, Language, ApiConfig

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
        admin_cfg = read_ini(file_path=config_filepath)

        return AdminConfig(
            api_config=ApiConfig(**admin_cfg["API"]),
            elastic=Elastic(**admin_cfg["ELASTIC"]),
            file_paths=FilePaths(**admin_cfg["FILE PATHS"])
        )


class ConfigMap(ConfigGeneral):
    store_data: bool = False
    data_size: int = None

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