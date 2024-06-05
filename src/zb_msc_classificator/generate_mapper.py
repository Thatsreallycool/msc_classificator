from zb_msc_classificator.tools import Serialize, dump, Toolbox
from zb_msc_classificator.config.config_datamodel import TrainingSource
from zb_msc_classificator.harmonize import Harmonizer
import pandas
import os

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan


class MapElastic:
    def __init__(self, config):
        self.tools = Toolbox()
        myquery = {
            "query": {
                'function_score': {
                    'query': {
                        'bool': {
                            'must': {
                                'range': {
                                    'de': {'gte': 0, 'lte': 200000}
                                }
                            }
                        }
                    },
                    'field_value_factor': {'field': 'score_linear'}
                }
            }
        }

        data = self.get_data(
            elastic_credentials=self.get_elastic_credentials(),
            query=myquery,
            index=self.config.admin_config.elastic.index_name
        )
        self.store_to_disk(
            data=data
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

    def store_to_disk(self):
        pass


class GenerateMap:
    def __init__(self, config):
        self.config = config
        self.training_data = self.get_training_data()
        self.tools = Toolbox()
        #self.map = self.execute()
        if self.config.store:
            self.done = self.store()

    def get_training_data(self):
        if self.config.training_source == TrainingSource.disk:
            return self.load_from_disk(
                filepath=self.config.admin_config.filepath_input.training_data,
                columns=['msc', 'keyword'],
                delimiter=','
            )
        elif self.config.training_source == TrainingSource.elastic:
            return self.load_from_elastic()
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

    def load_from_elastic(self):
        """
        get catenation of keywords and msc codes from elastic search
        :return: list of tuple (list(keywords), list(msc codes))
        """




    def execute(self):

        map = self.tools.nested_dict(layers=2, data_type=int)
        harmonize = Harmonizer()
        for row in self.training_data.itertuples():
            msc_list = self.tools.str_spaces_to_list(
                string=harmonize.clean_csv_data(
                    string_to_clean=row.msc
                ),
                delimiter=", "
            )
            keyword_list = self.tools.str_spaces_to_list(
                string=harmonize.clean_csv_data(
                    string_to_clean=row.keyword
                ),
                delimiter=","
            )
            keyword_list = [
                harmonize.remove_special_char(item)
                for item in keyword_list
            ]

            for keyword in keyword_list:
                if keyword == '':
                    continue
                for msc in msc_list:
                    map[keyword][msc] += 1

        return map

    def store(self):
        with open(self.config.admin_config.filepath_output.map, 'w') as f:
            dump(self.map, f, cls=Serialize)
        return os.path.isfile(self.config.admin_config.filepath_output.map)