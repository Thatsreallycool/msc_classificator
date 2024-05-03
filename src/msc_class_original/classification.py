import pandas
# Suppress FutureWarning messages
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import os
import json
#import requests

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer
from nltk import ngrams

from collections import Counter
import math
import numpy as np
import scipy

#from matplotlib import pyplot as plt

from zbmsc_finegrained.config import Config

from abc import ABC, abstractmethod


class Caretaker(ABC):
    def __init__(self, index_filepath: str):
        """
        purpose: for reusing methods

        """
        super().__init__()
        self.user_config = Config()
        self.index_filepath = index_filepath
        self.index = self.load_indexes(index_filepath=index_filepath)

    @staticmethod
    def load_indexes(index_filepath: str):
        print('Loading index ' + index_filepath)
        if os.path.isfile(index_filepath):
            with open(index_filepath, 'r') as f:
                print("done.")
                return json.load(f)
        else:
            raise Exception("no file found")


class Evaluate(Caretaker):
    def print_index_statistics(self, index_name: str, index_data: dict):
        print('\nStats of index ' + index_name)

        idx_avg_count = self.get_mean_count(index_data)
        print('Average entry per key count: ' + str(idx_avg_count))

        idx_avg_entropy = self.get_mean_entropy(index_data)
        print('Average entry per key entropy: ' + str(idx_avg_entropy))

        print('\n')
        return 0

    def get_mean_entropy(self):
        """
        # entropy
        :return:
        """
        entropies = []
        for cls in self.index.values():
            frequencies = [ent for ent in cls.values()]
            entropies.append(scipy.stats.entropy(frequencies))
        avg_entropy = np.mean(entropies)
        return avg_entropy

    def get_mean_count(self):
        """
        # average length
        :return:
        """
        lengths = [
            len(item)
            for item in self.index.values()
        ]
        return np.mean(lengths)


class Classification(Caretaker):
    def execute(self):
        test_data = self.load_test_data(
            filepath=self.user_config.filepaths["test_data"],
            delimiter=','
        )

        return self.predict_entity_msc(
            test_data=test_data,
            index=self.index
        )

    def predict_entity_msc(self, test_data, index):
        prediction_table = pandas.DataFrame(
            columns=[
                'de',
                'mscs_actual',
                'mscs_predicted',
                'confidences',
                'overlap_ratio'
            ]
        )

        # mscs actual vs. predicted
        mscs_actual = {}
        mscs_predicted = {}
        mscs_pred_conf = {}
        overlap_ratios = []

        sstopwords = self.get_data_from_txt(
            filepath=self.user_config.filepaths["stopwords"]
        )

        tot_rows = len(test_data)
        latest_progress = 0
        print("starting prediction...")
        for idx in range(tot_rows):
            # print(idx)
            current_progress = round(idx / tot_rows * 100, 1)
            if current_progress != latest_progress and \
                    current_progress % 10 == 0:
                print(current_progress, '%')
                latest_progress = current_progress

            de = test_data['de'][idx]
            text = test_data['text'][idx]
            mscs_actual[idx] = self.get_mscs(test_data, idx)
            mscs_predicted_stat = {}
            n_gram_lengths = [2, 3]
            for n in n_gram_lengths:
                try:
                    nngrams = ngrams(text.split(), n)
                    for nngram in nngrams:
                        entity = ''
                        for word in nngram:
                            entity += word + ' '
                        entity = entity[:-1]
                        try:
                            if index[entity] is not None and \
                                    entity not in sstopwords:
                                # print(entity)
                                # mscs_predicted[idx].extend(
                                # list(sorted_keyword_msc_idx[entity])[0:1])
                                for cls in index[entity].keys():
                                    try:
                                        # SELECTION HERE
                                        mscs_predicted_stat[cls] += 1
                                        # cls[1]#1 # weightedcontribution or
                                        # binarycontribution
                                    except:
                                        mscs_predicted_stat[cls] = 1
                        except:
                            pass
                except:
                    pass
        print("prediction finished!")
        return mscs_predicted_stat

    def get_mscs(self, table, idx):
        mscs = []
        for msc in self.clean(table['msc'][idx]).split():
            msc = msc.strip(',')
            mscs.append(msc)
        return mscs

    @staticmethod
    def clean(string):
        if not isinstance(string, str):
            return ""
        return string.replace(
            '[', ''
        ).replace(
            ']', ''
        ).replace(
            '\\',''
        ).replace(
            "'",''
        )

    @staticmethod
    def load_test_data(filepath: str, delimiter: str):
        return pandas.read_csv(
            filepath,
            delimiter=delimiter
        )

    @staticmethod
    def get_data_from_txt(filepath: str):
        with open(filepath, 'r') as f2:
            txt_data = f2.readlines()
        return txt_data
