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

from msc_class_original.config import Config

from abc import ABC, abstractmethod


class Caretaker(ABC):
    def __init__(self, index_filepath: str):
        """
        purpose: universal class for reusing methods, cannot be initiated

        :param index_filepath: relative or absolute filepath for generated
        index. taken out from config, so that different instances (i.e.
        indexes) can be run, compared and analysed independently.
        """
        super().__init__()
        self.user_config = Config()
        self.index_filepath = index_filepath
        self.index = self.load_indexes(index_filepath=index_filepath)

    @staticmethod
    def load_indexes(index_filepath: str):
        """

        :param index_filepath:  relative or absolute filepath for generated
        index
        :return: index as nested dictionary (entity -> class or class -> entity)
        """
        print('Loading index ' + index_filepath)
        if os.path.isfile(index_filepath):
            with open(index_filepath, 'r') as f:
                print("done.")
                return json.load(f)
        else:
            raise Exception("no file found")


class Classification(Caretaker):
    def execute(self):
        """
        after initiating this class (init from Caretaker) the index is
        already loaded and here the test data defined in config is
        :return: a dict mapping: de -> 10 MSCs ordered by importance
        """
        test_data = self.load_test_data(
            filepath=self.user_config.filepaths["load"]["test_data"],
            delimiter=','
        )

        return self.predict_entity_msc(
            test_data=test_data,
            index=self.index
        )

    def predict_entity_msc(self, test_data, index):
        """
        core function to map(by index) the text of test_data to MSCs

        :param test_data: test data from msc (defined in config)
        :param index: mapping from text -> MSCs (loaded by init)
        :return: map from de number (from test data set) -> MSCs
        """
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
            filepath=self.user_config.filepaths["load"]["stopwords"]
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
            if len(mscs_predicted_stat) != 0:
                sorted_mscs_predicted_stat = dict(
                    sorted(
                        mscs_predicted_stat.items(),
                        key=lambda item: item[1], reverse=True
                    )
                )

                # get (normalized) prediction (confidence)
                mscs_predicted[de] = list(sorted_mscs_predicted_stat)[
                                      :self.user_config.nr_msc_cutoff
                                      ]
                # cut off at fixed nr_mscs_cutoff or dynamic number
                # #len(mscs_actual[idx])
        print("prediction finished!")
        return mscs_predicted

    def get_mscs(self, table, idx):
        """
        retrieve msc array from tables row
        :param table: table with column "msc"
        :param idx: row number
        :return:
        """
        mscs = []
        for msc in self.clean(table['msc'][idx]).split():
            msc = msc.strip(',')
            mscs.append(msc)
        return mscs

    @staticmethod
    def clean(string):
        """
        cleaning of certain strings from special characters
        :param string: string with characters [,],\\,'
        :return: cleaned string
        """
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
        """
        load data from csv file
        :param filepath: local file path
        :param delimiter: delimiter in csv file
        :return: pandas data frame
        """
        return pandas.read_csv(
            filepath,
            delimiter=delimiter
        )

    @staticmethod
    def get_data_from_txt(filepath: str):
        """
        get data from text file
        :param filepath: local file path
        :return: data from text file as list
        """
        with open(filepath, 'r') as f2:
            txt_data = f2.readlines()
        return txt_data


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
