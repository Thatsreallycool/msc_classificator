from __future__ import annotations

from json import JSONEncoder, dump
from typing import Any, Iterator

import pandas

from collections import defaultdict

import os.path

from msc_class_original.config import Config


class Serialize(JSONEncoder):

    def iterencode(self, o: Any, _one_shot: bool = ...) -> Iterator[str]:
        if isinstance(o, defaultdict):
            for k, v in o.items():
                if isinstance(v, defaultdict):
                    o[k] = {label: count for label, count in sorted(v.items(), key=lambda x: x[1], reverse=True)}
        return super().iterencode(o, _one_shot)


class GenerateIndex:
    def __init__(self,
                 index_category: str,
                 km: bool = True,
                 mk: bool = False,
                 store_it: bool = True,
                 overwrite: bool = False
                 ):
        """

        :param index_category: 'keyword' or 'refs'
        :param km: create keyword_to_msc index map
        :param mk: create msc_to_keyword index map
        :param overwrite: boolean. enable if index results already exists and
        you want to overwrite
        """
        user_config = Config(config_file_path="/home/marcel/PycharmProjects/"
                     "msc_classificator/config.ini")

        training_data = self.load_training_data(
            filepath=user_config.filepaths["load"]["training_data"],
            columns=['msc', 'keyword', 'refs', 'text', 'title'],
            delimiter=','
        )

        store_folder = user_config.data_folder["save"]
        store_index_filepaths = {
            "km": {
                "file": f"{store_folder}/{index_category}_msc_idx.json",
                "todo": km
            },
            "mk": {
                "file": f"{store_folder}/msc_{index_category}_idx.json",
                "todo": mk
            }
        }
        self.index_generated = self.generate_idx(
            df=training_data,
            idx_name=index_category,
            km=km,
            mk=mk
        )["km"]
        if store_it:
            self.store_index(
                filepaths=store_index_filepaths,
                index=self.index_generated,
                overwrite=overwrite
            )

    def nested_dict(
            self,
            n: int,
            t: type
    ):
        """

        :param n: nr of levels in nested dict
        :param t: default type of content if key doesnt exist
        :return: nested default dict of n levels
        """
        if n == 1:
            return defaultdict(t)
        else:
            return defaultdict(lambda: self.nested_dict(n - 1, t))

    @staticmethod
    def clean(string: str):
        """

        :param string: remove specific special characters from string
        :return: cleaned string
        """
        if not isinstance(string, str):
            return ""
        return string.replace(
            '[', ''
        ).replace(
            ']', ''
        ).replace(
            '\\', ''
        ).replace(
            "'", ''
        )

    @staticmethod
    def load_training_data(
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

    def generate_idx(
            self,
            df: pandas.DataFrame,
            idx_name: str,
            km: bool,
            mk: bool
    ):
        """

        :param df: pandas dataframe
        :param idx_name: which column from training table is accessed
        :param km: bool. if True create map from entity -> class
        (to optimize performance)
        :param mk: bool. if True create map from class -> entity
        (to optimize performance)
        :return:
        """
        if km:
            print("mapping entity -> class")
            km_idx = self.nested_dict(2, int)
        if mk:
            print("mapping class -> entity")
            mk_idx = self.nested_dict(2, int)
        if not km and not mk:
            print("Nothing to do!")
            return None

        latest_progress = 0
        print(f"start {idx_name}")
        for row in df.itertuples():
            current_progress = round(row[0] / len(df) * 100, 1)
            if current_progress != latest_progress and \
                    current_progress % 10 == 0:
                print(current_progress, '%')
                latest_progress = current_progress
            mscs = self.clean(row.msc).replace(' ', '').split(',')
            for keyword in self.clean(getattr(row, idx_name)).split(","):
                keyword = keyword.lstrip().rstrip()
                for clea_str in [',', "'", '"', "`", '\\']:
                    keyword = keyword.strip(clea_str)
                if '' == keyword:
                    continue
                for msc in mscs:
                    if km:
                        km_idx[keyword][msc] += 1
                    if mk:
                        mk_idx[msc][keyword] += 1
        print(f"finished {idx_name}")

        if km and mk:
            return {
                "km": km_idx,
                "mk": mk_idx
            }
        elif km:
            return {"km": km_idx}
        elif mk:
            return {"mk": mk_idx}

    @staticmethod
    def store_index(
            filepaths: dict,
            index: dict,
            overwrite: bool = False
    ):
        for mapping, instructions in filepaths.items():
            if instructions["todo"]:
                if os.path.isfile(instructions["file"]):
                    if overwrite:
                        with open(instructions["file"], 'w') as f:
                            dump(index[mapping], f, cls=Serialize)
                        return os.path.isfile(instructions["file"])
                    else:
                        raise Exception("file already exists, please enable "
                                        "overwrite!")
                else:
                    with open(instructions["file"], 'w') as f:
                        dump(index[mapping], f, cls=Serialize)
                    return os.path.isfile(instructions["file"])
            else:
                continue

    def index_cutoff_keywords(self, max_keywords: int):
        return {
            keywords: values
            for keywords, values in self.index_generated.items()
            if len(keywords.split()) <= max_keywords
        }