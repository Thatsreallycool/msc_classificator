import json
from json import JSONEncoder, dump
from typing import Any, Iterator
from collections import defaultdict

import pandas as pd

import base64
import zlib
import pickle

import gzip


class Serialize(JSONEncoder):
    def iterencode(self, o: Any, _one_shot: bool = ...) -> Iterator[str]:
        if isinstance(o, defaultdict):
            for k, v in o.items():
                if isinstance(v, defaultdict):
                    o[k] = {
                        label: count
                        for label, count in sorted(
                            v.items(),
                            key=lambda x: x[1],
                            reverse=True
                        )
                    }
        return super().iterencode(o, _one_shot)


class Toolbox:
    def nested_dict(
            self,
            layers: int,
            data_type: type
    ):
        """

        :param layers: nr of levels in nested dict
        :param data_type: default type of content if key doesnt exist
        :return: nested default dict of n levels
        """
        if layers == 1:
            return defaultdict(data_type)
        else:
            return defaultdict(lambda: self.nested_dict(layers - 1, data_type))

    @staticmethod
    def str_spaces_to_list(string: str, delimiter: str):
        return string.split(delimiter)

    @staticmethod
    def list_of_dicts_to_list(list_of_dicts, key_of_dict):
        """
        [{key:val1},{key:val2},...] -> [val1,val2,...]
        :param list_of_dicts: a list of dicts containing the same subkey
        :param key_of_dict: the key of all dicts
        :return: a list of the values
        """
        return [item[key_of_dict] for item in list_of_dicts]

    @staticmethod
    def compress(data):
        return base64.b64encode(
            zlib.compress(
                pickle.dumps(data, protocol=4)
            )
        ).decode()

    @staticmethod
    def uncompress(pickled_data):
        return pickle.loads(
            zlib.decompress(
                base64.b64decode(
                    pickled_data.encode()
                )
            )
        )

    @staticmethod
    def load_json(filename: str):
        with open(filename, 'r') as f:
            return json.load(f)

    @staticmethod
    def store_json(filename: str, dict2store: dict):
        with open(filename, 'w') as f:
            dump(dict2store, f, cls=Serialize)
        return True

    @staticmethod
    def load_csv_data(filename: str, delimiter=','):
        return pd.read_csv(filename, delimiter=delimiter)

    def transform_csv_to_dict(
            self,
            filename: str,
            delimiter: str,
            idx_name: str,
            column_names: list
    ):
        data = self.load_csv_data(filename=filename, delimiter=delimiter)
        data_dict = {}
        for row in range(len(data)):
            if any(
                [
                    isinstance(data[item][row], float)
                    for item in column_names
                ]
            ):
                continue

            idx = str(data[idx_name][row])
            data_dict.update({idx: {}})
            #print(len(data))
            for item in column_names:
                try:
                    data_dict[idx].update({item: eval(data[item][row])})
                except (SyntaxError, NameError):
                    data_dict[idx].update({item: data[item][row]})

        return data_dict

    @staticmethod
    def zip_store(filepath: str, json_data):
        with gzip.open(filepath, 'wt') as fw:
            json.dump(json_data, fw, indent=4)
            fw.write("\n")

    @staticmethod
    def zip_load(filepath: str):
        with gzip.open(filepath, 'rb') as fr:
            ungzip = fr.read()
        return json.loads(ungzip.decode())
