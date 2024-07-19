from pydantic import BaseModel, validator, PositiveInt
import os

import nltk

import zb_msc_classificator as zbc
from zb_msc_classificator.config.config_datamodel \
    import TrainingSource, Language, FilterDocuments
from zb_msc_classificator.config.admin_config \
    import AdminConfig, FilePaths, Elastic, ApiConfig, ConfigLoader

from typing import List

config_loader = ConfigLoader()


class ConfigGeneral(BaseModel):
    api_config: ApiConfig = config_loader.get_api()
    elastic: Elastic = config_loader.get_elastic()
    file_paths: FilePaths = config_loader.get_filepaths()
    language: Language = Language.english


class ConfigMap(ConfigGeneral):
    data_size: int = 50000
    diff_only: bool = True
    filter_documents: FilterDocuments = FilterDocuments()
    store_data: bool = False

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
    training_source: TrainingSource = TrainingSource.elastic_snapshot
    store_map: bool = False


class ConfigClassify(ConfigGeneral):
    nr_msc_cutoff: PositiveInt = 10


class ConfigEvaluate(ConfigGeneral):
    pass


class ConfigEntityLinking(ConfigGeneral):
    ngram_lengths: List[PositiveInt] = [2, 3]
    sparql_link: str = "https://query.wikidata.org/sparql"


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

