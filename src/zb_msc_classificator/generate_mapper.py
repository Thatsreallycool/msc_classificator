from zb_msc_classificator.tools import Serialize, dump, Toolbox
from zb_msc_classificator.config.config_datamodel import TrainingSource
from zb_msc_classificator.harmonize import Harmonizer
import pandas
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
        self.config = config
        self.tools = Toolbox()

        self.previous_dataset_exists = self.check_for_datablob()
        if self.previous_dataset_exists:
            self.data = self.load_from_disk(
                filepath=self.config.admin_config.filepath_output.data_elastic
            )
            print(f"items: {len(self.data.keys())}")
        else:
            self.data = {}

        self.latest_id = self.get_latest_id()
        self.query = self.get_query(
            data_size=config.data_size
        )

    def execute(self):
        new_data = self.get_data(
            elastic_credentials=self.get_elastic_credentials(),
            query=self.query,
            index=self.config.admin_config.elastic.index_name
        )
        if len(new_data.keys()) == 0:
            print("found no new items. Try bigger data_size!")
        else:
            self.data.update(
                new_data
            )

            if self.config.store_data_elastic:
                self.store_to_disk(
                    filepath=self.config.admin_config.filepath_output.data_elastic
                )

    def check_for_datablob(self):
        if os.path.isfile(
            self.config.admin_config.filepath_output.data_elastic
        ):
            return True
        else:
            return False

    def load_from_disk(self, filepath):
        """
        TODO: placeholder method until such time support decides how to
        store this

        :param filepath: filepath of formerly stored datablob
        """
        if self.previous_dataset_exists:
            with open(filepath, "r") as file_read:
                raw_data = file_read.read()
            return self.tools.uncompress(pickled_data=raw_data)
        else:
            return None

    def get_latest_id(self):
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
        return Elasticsearch(
            hosts=[
                f"{self.config.admin_config.elastic.es_host}:"
                f"{self.config.admin_config.elastic.es_port}"
            ],
            api_key=self.config.admin_config.elastic.es_api_key,
            ca_certs=self.config.admin_config.elastic.ca_certs
        )

    def get_data(self, elastic_credentials, query, index):
        print(
            elastic_credentials.count(
                index=index,
                body=query
            )
        )
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

    def get_training_data(self):
        if self.config.training_source == TrainingSource.csv:
            return Harmonizer().transform_csv_to_list_of_tuples(
                csv_data=self.load_from_disk(
                    filepath=self.config.admin_config.filepath_input
                        .csv_training_data,
                    columns=['msc', 'keyword'],
                    delimiter=','
                )
            )
        elif self.config.training_source == TrainingSource.elastic_snapshot:
            data = self.load_from_elastic(
                elastic_file=self.config.admin_config.filepath_output.data_elastic
            )
            return [
                (item["keywords"], item["mscs"])
                for item in data.values()
            ]
        elif self.config.training_source == TrainingSource.elastic_live:
            data = MapElastic(config=self.config).data
            return [
                (item["keywords"], item["mscs"])
                for item in data.values()
            ]
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
        lin_map = self.tools.nested_dict(layers=2, data_type=int)

        for km_tuple in self.training_data:
            keyword_list, msc_list = km_tuple
            for keyword in keyword_list:
                for msc in msc_list:
                    lin_map[keyword][msc] += 1

        if self.config.store_map:
            self.store(lin_map=lin_map)

        return lin_map

    def store(self, lin_map):
        self.tools.zip_store(
            filepath=self.config.admin_config.filepath_output.map_zipped,
            json_data=lin_map
        )