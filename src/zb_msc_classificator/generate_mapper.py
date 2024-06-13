from zb_msc_classificator.tools import Serialize, dump, Toolbox
from zb_msc_classificator.config.config_datamodel import TrainingSource
from zb_msc_classificator.harmonize import Harmonizer
import pandas
import os

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan


class MapElastic:
    def __init__(self, config):
        self.config = config
        self.tools = Toolbox()
        myquery = {
            "query": {
                'function_score': {
                    'query': {
                        'bool': {
                            'must': {
                                'range': {
                                    'de': {'gte': 0, 'lte': 8000000}
                                }
                            }
                        }
                    },
                    'field_value_factor': {'field': 'score_linear'}
                }
            }
        }

        self.data = self.get_data(
            elastic_credentials=self.get_elastic_credentials(),
            query=myquery,
            index=self.config.admin_config.elastic.index_name
        )
        self.store_to_disk(
            filepath=self.config.admin_config.filepath_output.map_from_elastic
        )

    def get_elastic_credentials(self):
        return Elasticsearch(
            hosts=[
                f"{self.config.admin_config.elastic.es_host}:"
                f"{self.config.admin_config.elastic.es_port}"
            ],
            api_key=self.config.admin_config.elastic.es_api_key,
            ca_certs=self.config.admin_config.elastic.ca_certs
        )

    def get_data(self, elastic_credentials, query, index):
        results = scan(
            client=elastic_credentials,
            query=query,
            index=index
        )

        return [
            (
                self.tools.list_of_dicts_to_list(
                    list_of_dicts=item['_source']['keywords'],
                    key_of_dict='text'
                ),
                self.tools.list_of_dicts_to_list(
                    list_of_dicts=item['_source']['msc'],
                    key_of_dict='code'
                )
            )
            for item in results
            if 'keywords' in item['_source'] and 'msc' in item['_source']
        ]

    def store_to_disk(self, filepath):
        """
        TODO: placeholder method until such time support decides how to store this file
        :param filepath: filepath for storing file
        :return: bool for success
        """
        if filepath is not None:
            with open(filepath, "w") as file_write:
                file_write.write(self.tools.compress(self.data))
            return True
        else:
            raise FileNotFoundError("admin_config map_from_elastic missing!")


class GenerateMap:
    def __init__(self, config):
        self.config = config
        self.tools = Toolbox()

        self.training_data = self.get_training_data()
        self.map = self.execute()
        if self.config.store:
            self.done = self.store()

    def get_training_data(self):
        if self.config.training_source == TrainingSource.disk:
            return Harmonizer().transform_csv_to_list_of_tuples(
                csv_data=self.load_from_disk(
                    filepath=self.config.admin_config.filepath_input.training_data,
                    columns=['msc', 'keyword'],
                    delimiter=','
                )
            )
        elif self.config.training_source == TrainingSource.elastic:
            return self.load_from_elastic(
                elastic_file=self.config.admin_config.filepath_output.map_from_elastic
            )
        else:
            return None

    @staticmethod
    def load_from_disk(
            filepath: str,
            columns: list,
            delimiter: str
    ):
        """

        :param filepath: local filepath
        :param columns: which columns shoul be loaded
        :param delimiter: csv delimiter
        :return: pandas dataframe
        """
        return pandas.read_csv(
            filepath,
            delimiter=delimiter,
            usecols=columns
        )

    def load_from_elastic(self, elastic_file):
        """
        TODO: place holder method for when support decided how to store this
        file
        get catenation of keywords and msc codes from elastic search
        :return: list of tuple (list(keywords), list(msc codes))
        """
        with open(
            elastic_file,
            "r"
        ) as file_reader:
            elastic_data = file_reader.read()

        return self.tools.uncompress(elastic_data)

    def execute(self):
        map = self.tools.nested_dict(layers=2, data_type=int)

        for km_tuple in self.training_data:
            keyword_list, msc_list = km_tuple
            for keyword in keyword_list:
                for msc in msc_list:
                    map[keyword][msc] += 1
        return map

    def store(self):
        with open(self.config.admin_config.filepath_output.map, 'w') as f:
            dump(self.map, f, cls=Serialize)
        return os.path.isfile(self.config.admin_config.filepath_output.map)