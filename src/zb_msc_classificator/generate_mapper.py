from zb_msc_classificator.tools import Toolbox
from zb_msc_classificator.harmonize import Harmonizer
from zb_msc_classificator.config.definition import ConfigHarmonize

from zb_msc_classificator.config.config_datamodel import TrainingSource
import os

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan


class MapElastic:
    """
    input: either local csv file, or elastic search connector
    output: dict {de: {keywords: [...] , mscs: [...]}}

    future extensions can include other metadata information in connection to
    this datablob
    """
    def __init__(self, config):
        """
        set up for downloading data from elastic search and storing excerpt
        onto local file
        :param config: expects ConfigGenerate()
        """
        self.config = config
        self.tools = Toolbox()

        self.previous_dataset_exists = self.check_for_datablob()
        if self.previous_dataset_exists:
            self.data = self.tools.load_data(
                filepath=self.config.admin_config.file_paths.data_stored
            )
            print(f"items: {len(self.data.keys())}")
        else:
            self.data = {}

        self.latest_id = self.get_latest_id()
        self.query = self.get_query(
            data_size=config.data_size
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
            elastic_credentials=self.get_elastic_credentials(),
            query=self.query,
            index=self.config.admin_config.elastic.index_name
        )
        if len(new_data.keys()) == 0:
            print("found no new items. Try bigger data_size!")
        else:
            self.data.update(new_data)
            if self.config.store_data:
                self.tools.store_data(
                    filepath=self.config.admin_config.file_paths.data_stored,
                    data=self.data
                )

    def check_for_datablob(self):
        """
        if data set is already in place, just add to existing data set
        :return:
        """
        if os.path.isfile(
            self.config.admin_config.file_paths.data_stored
        ):
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

    def get_query(self, data_size: int):
        """
        de range query
        :param data_size: how big is the intervall window
        (latest stored de, latest stored de+data_size]
        :return: query for elastic search
        """
        if not isinstance(data_size, int):
            raise ValueError(f"cant get any data, "
                             f"if data_size is set to {data_size}!")
        up = self.latest_id + data_size
        return {
            "query": {
                'function_score': {
                    'query': {
                        'bool': {
                            'must': {
                                'range': {
                                    'de': {
                                        'gt': self.latest_id,
                                        'lte': up
                                    }
                                }
                            }
                        }
                    },
                    'field_value_factor': {
                        'field': 'score_linear'
                    }
                }
            }
        }

    def get_elastic_credentials(self):
        """
        std credentials for elastic search, need at least reading credentials
        :return: Elastic Search init object
        """
        return Elasticsearch(
            hosts=[
                f"{self.config.admin_config.elastic.es_host}:"
                f"{self.config.admin_config.elastic.es_port}"
            ],
            api_key=self.config.admin_config.elastic.es_api_key,
            ca_certs=self.config.admin_config.elastic.ca_certs
        )

    def get_data(self, elastic_credentials, query, index):
        """
        get data from elastic search index

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
    def __init__(self, config):
        """
        set up for get data from local disk and store map onto local disk
        :param config:
        """
        self.config = config
        self.tools = Toolbox()
        self.harmonize = Harmonizer(
            config=ConfigHarmonize(use_stopwords=False)
        )

        self.training_data = self.get_training_data()

    def execute(self):
        lin_map = self.tools.nested_dict(layers=2, data_type=int)

        for km_tuple in self.training_data:
            keyword_list, msc_list = km_tuple

            for keyword in keyword_list:
                for msc in msc_list:
                    lin_map[keyword][msc] += 1

        if self.config.store_map:
            self.tools.store_data(
                filepath=self.config.admin_config.file_paths.map_stored,
                data=lin_map
            )

        return lin_map

    def get_training_data(self):
        if self.config.training_source == TrainingSource.csv:
            filepath = self.config.admin_config.file_paths.data_stored
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
            filepath = self.config.admin_config.file_paths.data_stored
            if filepath.endswith(('.pickle', '.gz')):
                data = self.tools.load_data(filepath=filepath)
                return [
                    (
                        self.harmonization_protocol(data=item["keywords"]),
                        item["mscs"]
                    )
                    for item in data.values()
                ]
            else:
                raise ValueError(f"training source was chosen to be a "
                                 f"snapshot from elastic, but filename was: "
                                 f"{filepath}. Should be either gz or pickle.")
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
            self.harmonize.canonicalize(
                text=item
            )
            for item in data
        ]
