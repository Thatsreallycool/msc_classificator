from zb_msc_classificator.tools import Toolbox
from zb_msc_classificator.harmonize import Harmonizer
from zb_msc_classificator.config.definition import \
    ConfigHarmonize, ConfigMap, ConfigGenerate, ConfigGeneral

from zb_msc_classificator.config.config_datamodel import TrainingSource
import os

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

from zbqueryparser import QueryParser

from datetime import datetime


class MapElastic:
    """
    input: either local csv file, or elastic search connector
    output: dict {de: {keywords: [...] , mscs: [...]}}

    future extensions can include other metadata information in connection to
    this datablob
    """
    def __init__(
            self,
            config: ConfigMap = ConfigMap(
                store_data=True
            )
    ):
        """
        set up for downloading data from elastic search and storing excerpt
        onto local file
        :param config: expects ConfigGenerate()
        """
        self.config = config
        self.tools = Toolbox()
        self.es = self.get_elastic_credentials()

        self.previous_dataset_exists = self.check_for_datablob()
        if self.previous_dataset_exists:
            self.data = self.tools.load_data(
                filepath=self.config.file_paths.data_set
            )
        else:
            self.data = {}

        self.latest_id = self.get_latest_id()
        self.query = self.get_query(
            zbmath_query=self.get_zbmath_query()
        )

    def execute(self):
        """
        1. get data from elastic
        2. update potentially existing data set
        3. (optional) store data set to disk
        :return: none, if storing data is activated, data blob will be saved
        to disk
        """
        new_data = self.get_data(
            elastic_credentials=self.es,
            query=self.query,
            index=self.config.elastic.index_name
        )
        if len(new_data.keys()) == 0:
            print("found no new items. Try bigger data_size!")
        else:
            self.data.update(new_data)
            print(f"items collected: {len(self.data.keys())}")
            if self.config.store_data:
                self.tools.store_data(
                    filepath=self.config.file_paths.data_set,
                    data=self.data
                )

    def check_for_datablob(self):
        """
        if data set is already in place, just add to existing data set
        :return:
        """
        if os.path.isfile(
            self.config.file_paths.data_set
        ) and os.stat(
            self.config.file_paths.data_set
        ).st_size > 0:
            return True
        else:
            return False

    def get_latest_id(self):
        """
        for adding new data, we need to find a footpoint from which we may
        start the elastic search.
        Assumption: new de-numbers are always higher than old ones
        :return:
        """
        if self.previous_dataset_exists:
            return max(
                [
                    int(de)
                    for de in self.data.keys()
                ]
            )
        else:
            return 0

    def get_query(self, zbmath_query: str):
        """
        :return: query for elastic search
        """
        elastic_query = QueryParser(
            es=self.es,
            es_index_meta=self.config.elastic.meta_index
        ).compile(
            index=self.config.elastic.index_name,
            user_query=zbmath_query
        )
        elastic_query.pop("from", None)
        elastic_query.pop("size", None)

        return elastic_query

    def get_zbmath_query(self):
        zbmath_queries = []
        if self.config.filter_documents.publication_year_start is not None:
            zbmath_queries.append(
                f"py:{self.config.filter_documents.publication_year_start}-"
                f"{datetime.now().year}"
            )
        if self.config.filter_documents.state is not None:
            zbmath_queries.append(
                f"st:{self.config.filter_documents.state}"
            )
        if self.config.diff_only:
            zbmath_queries.append(
                f"de:{self.latest_id}-{self.latest_id+self.config.data_size}"
            )
        if len(zbmath_queries):
            return " & ".join(zbmath_queries)
        else:
            raise ValueError("no query defined!")

    def get_elastic_credentials(self):
        """
        std credentials for elastic search, need at least reading credentials
        :return: Elastic Search init object
        """
        return Elasticsearch(
            hosts=[
                f"{self.config.elastic.es_host}:"
                f"{self.config.elastic.es_port}"
            ],
            api_key=self.config.elastic.es_api_key,
            ca_certs=self.config.elastic.ca_certs
        )

    def get_data(self, elastic_credentials, query, index):
        """
        get data from elastic search index. if more data needed, add to this
        dict

        :param elastic_credentials: Elastic Search init object
        :param query: search query for elastic search
        :param index: name of ES index
        :return: dict: {de: {'keywords': [...], 'mscs': [...]}}
        """
        results = scan(
            client=elastic_credentials,
            query=query,
            index=index
        )

        return {
            item["_id"]:
                {
                    'keywords': self.tools.list_of_dicts_to_list(
                        list_of_dicts=item['_source']['keywords'],
                        key_of_dict='text'
                    ),
                    'mscs': self.tools.list_of_dicts_to_list(
                        list_of_dicts=item['_source']['msc'],
                        key_of_dict='code'
                    )
                }
            for item in results
            if 'keywords' in item['_source'] and 'msc' in item['_source']
        }


class GenerateMap:
    """
    generates dict {<keyword>: {<msc code>: <int>, ...}, {...}, ... }
    """
    def __init__(self, config: ConfigGenerate = ConfigGenerate()):
        """
        set up for get data from local disk and store map onto local disk
        :param config:
        """
        self.config = config
        self.tools = Toolbox()
        self.harmonize = Harmonizer(
            config=ConfigHarmonize(
                use_stopwords=True
            )
        )

        self.training_data = self.get_training_data()

    def execute(self):
        lin_map = self.tools.nested_dict(
            layers=2,
            data_type=int
        )

        for km_tuple in self.training_data:
            keyword_list, msc_list = km_tuple

            for keyword in keyword_list:
                for msc in msc_list:
                    lin_map[keyword][msc] += 1

        if self.config.store_map:
            self.tools.store_data(
                filepath=self.config.file_paths.map,
                data=lin_map
            )

        return lin_map

    def get_training_data(self):
        if self.config.training_source == TrainingSource.csv:
            filepath = self.config.file_paths.data_set
            if not filepath.endswith(".csv"):
                raise ValueError(f"Training source was chosen to be csv, but "
                                 f"filepath is {filepath}")
            else:
                return self.harmonize.transform_csv_to_list_of_tuples(
                    csv_data=self.tools.load_data(
                        filepath=filepath,
                        csv_columns=['msc', 'keyword'],
                        csv_delimiter=','
                    )
                )
        elif self.config.training_source == TrainingSource.elastic_snapshot:
            filepath = self.config.file_paths.data_set
            data = self.tools.load_data(filepath=filepath)
            return [
                (
                    self.harmonization_protocol(data=item["keywords"]),
                    item["mscs"]
                )
                for item in data.values()
            ]
        elif self.config.training_source == TrainingSource.elastic_live:
            map_elastic = MapElastic(config=self.config)
            map_elastic.execute()
            data = map_elastic.data
            return [
                (item["keywords"], item["mscs"])
                for item in data.values()
            ]
        else:
            return None

    def harmonization_protocol(self, data: list):
        return [
            ' '.join(
                self.harmonize.lemmatization(
                    token_list=self.harmonize.remove_accents(
                        string_to_clean=self.harmonize.remove_stopwords(
                            text=self.harmonize.canonicalize(
                                text=item
                            ),
                            position_in_text=-1
                        )
                    ).split()
                )
            )
            for item in data
        ]
