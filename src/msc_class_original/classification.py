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

from matplotlib import pyplot as plt
import pandas as pd

from msc_class_original.config import Config

from abc import ABC, abstractmethod


class Caretaker(ABC):
    def __init__(
            self,
            user_config,
            index_filepath: str = None,
            index: dict = {}
    ):
        """
        purpose: universal class for reusing methods, cannot be initiated

        :param index_filepath: relative or absolute filepath for generated
        index. taken out from config, so that different instances (i.e.
        indexes) can be run, compared and analysed independently.
        """
        super().__init__()
        self.config = user_config
        if index_filepath:
            self.index_filepath = index_filepath
            self.index = self.load_indexes(index_filepath=index_filepath)
        elif index.keys():
            self.index_filepath = None
            self.index = index
        else:
            raise Exception("either provide index file path or index with "
                            "keys!")

    @staticmethod
    def load_indexes(
            index_filepath: str
    ):
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
            raise Exception(f"no file found. looking for {index_filepath}")

    @staticmethod
    def store_df(
            data_filepath: str,
            data: dict,
            header: list
    ):
        """

        :param data_filepath: local storage location
        :param data: nested dictionary with data: keys: {k1: val, k2: val}
        :param header:  [keys, k1, k2]
        :return:
        """
        df = pandas.DataFrame(columns=header)
        for de, mscs in data.items():
            new_row = {
                header[0]: de,
                header[1]: mscs[header[1]],
                header[2]: mscs[header[2]]
            }
            df = df.append(new_row, ignore_index=True)

        store_filename = data_filepath
        if os.path.isfile(store_filename):
            os.remove(store_filename)
        df.to_csv(store_filename)
        if os.path.isfile(store_filename):
            return True
        else:
            return False

    @staticmethod
    def retrieve_df(
            df_filepath: str
    ):
        return pandas.read_csv(df_filepath)

    @staticmethod
    def retrieve_json(
            json_filepath: str
    ):
        with open(json_filepath, 'r') as f:
            return json.load(f)

    @staticmethod
    def clean_list(
            string: str,
            sep: str
    ):
        """
        cleaning of certain strings from special characters
        :param string: string with characters [,],\\,'
        :param sep: define separator for turning string into list
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
        ).split(sep=sep)


class Classification(Caretaker):
    def execute(
            self,
            pred_basis: str,
            store_to_file: bool = True
    ):
        """
        after initiating this class (init from Caretaker) the index is
        already loaded and here the test data defined in config is
        :param prediction_basis: either 'refs', 'keyword' or 'text'
        :return: a dict mapping: de -> 10 MSCs ordered by importance
        """
        test_data = self.load_test_data(
            filepath=self.config.filepaths["load"]["test_data"],
            delimiter=','
        )

        data = self.predict_entity_msc(
            test_data=test_data,
            index=self.index,
            prediction_basis=pred_basis
        )
        if store_to_file:
            return self.store_df(
                data_filepath=self.config.filepaths["save"][f"pred_{pred_basis}"],
                data=data,
                header=['de', 'mscs_predicted', 'mscs_actual']
           )
        else:
            return data

    def predict_entity_msc(
            self,
            test_data: pandas.DataFrame,
            index: dict,
            prediction_basis: str
    ):
        """
        core function to map(by index) the text of test_data to MSCs

        :param test_data: test data from msc (defined in config)
        :param index: mapping from text -> MSCs (loaded by init)
        :param prediction_basis: string describing either 'refs', 'keyword'
        or 'text'
        :return: dict map from de number (from test data set) -> MSCs_predicted
        and MSCs_actual according to test data set
        """
        # mscs actual vs. predicted
        mscs_actual = {}
        mscs_predicted = {}
        mscs_pred_conf = {}
        overlap_ratios = []

        sstopwords = self.get_data_from_txt(
            filepath=self.config.filepaths["load"]["stopwords"]
        )

        tot_rows = len(test_data)
        latest_progress = 0
        print(f"starting prediction based on... {prediction_basis}")
        for idx in range(tot_rows):
            # print(idx)
            current_progress = round(idx / tot_rows * 100, 1)
            if current_progress != latest_progress and \
                    current_progress % 10 == 0:
                print(current_progress, '%')
                latest_progress = current_progress

            de = test_data['de'][idx]
            mscs_actual[de] = self.get_mscs(test_data, idx)
            mscs_predicted_stat = {}
            if prediction_basis == "text":
                text = test_data[prediction_basis][idx]
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
                    mscs_predicted[de] = list(
                        sorted_mscs_predicted_stat
                    )[:self.config.nr_msc_cutoff]
                    # cut off at fixed nr_mscs_cutoff or dynamic number
                    # #len(mscs_actual[idx])
            elif prediction_basis == "keyword":
                keywords = self.clean_list(
                    string=test_data[prediction_basis][idx],
                    sep=", "
                )

                for keyword in keywords:
                    try:
                        for cls in index[keyword].items():
                            try:
                                # SELECTION HERE
                                mscs_predicted_stat[cls[0]] += 1
                                # cls[1]#1 # weightedcontribution or binarycontribution
                            except:
                                mscs_predicted_stat[cls[0]] = 1
                    except:
                        pass

                if len(mscs_predicted_stat) != 0:
                    # sort
                    sorted_mscs_predicted_stat = dict(
                        sorted(
                            mscs_predicted_stat.items(),
                            key=lambda item: item[1],
                            reverse=True
                        )
                    )

                    # get (normalized) prediction (confidence)
                    mscs_predicted[de] = list(
                        sorted_mscs_predicted_stat
                    )[:self.config.nr_msc_cutoff]  # cut off at fixed
                    # nr_mscs_cutoff or dynamic number #len(mscs_actual[idx])
                    mscs_cut_off = list(
                        sorted_mscs_predicted_stat.items()
                    )[:self.config.nr_msc_cutoff]
                    # norm
                    tot = sum(v for k, v in mscs_cut_off)
                    # confidence
                    mscs_pred_conf[idx] = [v / tot for k, v in mscs_cut_off]
            elif prediction_basis == "refs":
                references = self.clean_list(
                    string=test_data[prediction_basis][idx],
                    sep=","
                )

                for reference in references:
                    try:
                        for cls in index[reference].items():
                            try:
                                # SELECTION HERE
                                mscs_predicted_stat[cls[0]] += 1
                                # cls[1]#1 # weightedcontribution or binarycontribution
                            except:
                                mscs_predicted_stat[cls[0]] = 1
                    except:
                        pass

                if len(mscs_predicted_stat) != 0:
                    # sort
                    sorted_mscs_predicted_stat = dict(
                        sorted(
                            mscs_predicted_stat.items(),
                            key=lambda item: item[1],
                            reverse=True
                        )
                    )

                    # get (normalized) prediction (confidence)
                    mscs_predicted[de] = list(
                        sorted_mscs_predicted_stat
                    )[:self.config.nr_msc_cutoff]  # cut off at fixed nr_mscs_cutoff or dynamic number #len(mscs_actual[idx])
                    mscs_cut_off = list(
                        sorted_mscs_predicted_stat.items()
                    )[:self.config.nr_msc_cutoff]

        print("prediction finished!")
        return {
            de: {
                "mscs_predicted": mscs_predicted[de],
                "mscs_actual": mscs_actual[de]
            }
            for de, predicted in mscs_predicted.items()
            if de in mscs_predicted.keys() and de in mscs_actual.keys()
        }

    def get_mscs(
            self,
            table,
            idx
    ):
        """
        retrieve msc array from tables row
        :param table: table with column "msc"
        :param idx: row number
        :return:
        """
        mscs = []
        for msc in self.clean_list(
            string=table['msc'][idx],
            sep=" "
        ):
            msc = msc.strip(',')
            mscs.append(msc)
        return mscs

    @staticmethod
    def load_test_data(
            filepath: str,
            delimiter: str
    ):
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
    def get_data_from_txt(
            filepath: str
    ):
        """
        get data from text file
        :param filepath: local file path
        :return: data from text file as list
        """
        with open(filepath, 'r') as f2:
            txt_data = f2.readlines()
        return txt_data


class Evaluate(Caretaker):
    def print_index_statistics(
            self,
            index_name: str,
            index_data: dict
    ):
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

    def get_precision_recall(self):
        # load from file
        ## load prediction tables
        prediction_table_text = self.retrieve_df(
            df_filepath=self.config.filepaths["save"]["pred_text"]
        )
        prediction_table_keywords = self.retrieve_df(
            df_filepath=self.config.filepaths["save"]["pred_keyword"]
        )
        prediction_table_references = self.retrieve_df(
            df_filepath=self.config.filepaths["save"]["pred_refs"]
        )

        # load mrmscs baseline
        mrmscs_dict = self.retrieve_json(
            json_filepath=self.config.filepaths["load"]["mrmscs"]
        )

        # preprocess input data
        ## filter test data for de numbers that contain keywords AND texts
        de_numbers_containing_keywords_and_texts = [
            item
            for item in list(prediction_table_keywords['de'])
            if item in list(prediction_table_text['de'])
            if item in list(prediction_table_references['de'])
        ]

        ## prep results dict
        precision_recall = {
            'mscs_human_baseline': {},
            'mscs_predicted_text': {},
            'mscs_predicted_keywords': {},
            'mscs_predicted_references': {}
        }

        latest_progress = 0
        for runx, de in enumerate(de_numbers_containing_keywords_and_texts):
            # print(idx / len(prediction_table_text))
            current_progress = round(
                (runx + 1) / len(de_numbers_containing_keywords_and_texts)*100,
                1
            )
            if current_progress != latest_progress \
                    and current_progress % 10 == 0:
                print(current_progress, '%')
                latest_progress = current_progress

            idx = prediction_table_text.index[
                prediction_table_text['de'] == de
            ].tolist()[0]

            # collect mscs
            mscs_dict = {}
            mscs_dict['mscs_mr'] = mrmscs_dict[str(de)]
            mscs_dict['mscs_human_baseline'] = self.clean_list(
                string=prediction_table_text['mscs_actual'][idx],
                sep=", "
            )
            mscs_dict['mscs_predicted_text'] = self.clean_list(
                string=prediction_table_text['mscs_predicted'][idx],
                sep=", "
            )
            idxk = prediction_table_keywords.index[
                prediction_table_keywords['de'] == de
            ].tolist()[0]
            mscs_dict['mscs_predicted_keywords'] = self.clean_list(
                string=prediction_table_keywords["mscs_predicted"][idxk],
                sep=", "
            )
            idxr = prediction_table_references.index[
                prediction_table_references['de'] == de
            ].tolist()[0]
            mscs_dict['mscs_predicted_references'] = self.clean_list(
                string=prediction_table_references["mscs_predicted"][idxr],
                sep=","
            )

            # calc precision, recall
            mscs_actual = mscs_dict['mscs_mr']
            for mscs_origin in precision_recall.keys():
                mscs_predicted_full = mscs_dict[mscs_origin]

                for i in range(2, self.config.nr_msc_cutoff + 1):
                    mscs_predicted = mscs_predicted_full[:i]
                    mscs_intersection = [
                        msc
                        for msc in mscs_predicted
                        if msc in mscs_actual
                    ]

                    if len(mscs_predicted) > 0:
                        precision = len(mscs_intersection) / len(mscs_predicted)
                    else:
                        precision = 1

                    if len(mscs_actual) > 0:
                        recall = len(mscs_intersection) / len(mscs_actual)
                    else:
                        recall = 1

                    try:
                        precision_recall[
                            mscs_origin
                        ][i]['precisions'].append(precision)
                        precision_recall[
                            mscs_origin
                        ][i]['recalls'].append(recall)
                    except:
                        try:
                            precision_recall[
                                mscs_origin
                            ][i]['precisions'] = [precision]
                            precision_recall[
                                mscs_origin
                            ][i]['recalls'] = [recall]
                        except:
                            precision_recall[
                                mscs_origin
                            ][i] = {'precisions': [precision]}
                            precision_recall[
                                mscs_origin
                            ][i] = {'recalls': [recall]}

        # plot data
        fig, ax = plt.subplots()
        for mscs_origin in precision_recall.keys():

            pr_rc = precision_recall[mscs_origin]
            precisions = []
            recalls = []
            cutoffs = []
            for p_r in pr_rc.items():
                cutoffs.append(p_r[0])
                precisions.append(np.mean(p_r[1]['precisions']))
                recalls.append(np.mean(p_r[1]['recalls']))

            marker_dict = dict(
                zip(
                    precision_recall.keys(),
                    ['x', 's', 'o', '>']
                )
            )
            ax.scatter(
                recalls,
                precisions,
                marker=marker_dict[mscs_origin],
                s=10,
                label=mscs_origin
            )

        plt.title('Precision-Recall (ROC) Curve')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.xlim((0, 1))
        plt.ylim((0, 1))
        plt.xticks(np.arange(0, 1.01, 0.1))
        plt.yticks(np.arange(0, 1.01, 0.1))
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.savefig(
            f'{self.config.data_folder["save"]}prec-rec-curve.pdf',
            format="pdf",
            bbox_inches="tight"
        )
        plt.show()

    def get_precision_recall2(self, kw: dict = None):
        # load from file
        ## load prediction tables
        prediction_table_text = self.retrieve_df(
            df_filepath=self.config.filepaths["save"]["pred_text"]
        )
        prediction_dict_text = {
            prediction_table_text['de'][x]: {
                'predicted': prediction_table_text['mscs_predicted'][x],
                'actual': prediction_table_text['mscs_actual'][x]
            }
            for x in range(len(prediction_table_text))
        }
        if kw is None:
            prediction_table_keywords = self.retrieve_df(
                df_filepath=self.config.filepaths["save"]["pred_keyword"]
            )
            prediction_dict_keywords = {
                prediction_table_keywords['de'][x]: {
                    'predicted': prediction_table_keywords['mscs_predicted'][x],
                    'actual': prediction_table_keywords['mscs_actual'][x]
                }
                for x in range(len(prediction_table_keywords))
            }
        else:
            prediction_dict_keywords = {
                k: {
                    "predicted": v["mscs_predicted"],
                    "actual": v["mscs_actual"]
                }
                for k, v in kw.items()
            }
        prediction_table_references = self.retrieve_df(
            df_filepath=self.config.filepaths["save"]["pred_refs"]
        )
        prediction_dict_references = {
            prediction_table_references['de'][x]: {
                'predicted': prediction_table_references['mscs_predicted'][x],
                'actual': prediction_table_references['mscs_actual'][x]
            }
            for x in range(len(prediction_table_references))
        }

        # load mrmscs baseline
        mrmscs_dict = self.retrieve_json(
            json_filepath=self.config.filepaths["load"]["mrmscs"]
        )

        ## prep results dict
        precision_recall = {
            'mscs_human_baseline': {},
            'mscs_predicted_text': {},
            'mscs_predicted_keywords': {},
            'mscs_predicted_references': {}
        }

        latest_progress = 0
        tot_rows = len(prediction_dict_text.keys()) + \
                   len(prediction_dict_references.keys()) + \
                   len(prediction_dict_keywords.keys())
        print(f"starting... total: {tot_rows}")

        for runx, de in enumerate(prediction_table_text['de']):
            current_progress = round(
                (runx + 1) / tot_rows * 100, 1
            )
            if current_progress != latest_progress \
                    and current_progress % 10 == 0:
                print(current_progress, '%')
                latest_progress = current_progress

            # collect mscs
            mscs_dict = {}
            mscs_dict['mscs_human_baseline'] = self.clean_list(
                string=prediction_dict_text[de]['actual'],
                sep=", "
            )
            mscs_dict['mscs_predicted_text'] = self.clean_list(
                string=prediction_dict_text[de]['predicted'],
                sep=", "
            )

            # calc precision, recall
            precision_recall = self.get_prec(
                mscs_dict=mscs_dict,
                precision_recall=precision_recall,
                mscs_origin="mscs_predicted_text",
                mscs_actual=mrmscs_dict[str(de)]
            )
            precision_recall = self.get_prec(
                mscs_dict=mscs_dict,
                precision_recall=precision_recall,
                mscs_origin="mscs_human_baseline",
                mscs_actual=mrmscs_dict[str(de)]
            )

        for runy, de in enumerate(prediction_dict_keywords.keys()):
            current_progress = round(
                (len(prediction_table_text) + runy + 1) / tot_rows * 100, 1
            )
            if current_progress != latest_progress \
                    and current_progress % 10 == 0:
                print(current_progress, '%')
                latest_progress = current_progress

            # collect mscs
            mscs_dict = {}
            mscs_dict[
                'mscs_predicted_keywords'
            ] = prediction_dict_keywords[de]['predicted']

            # calc precision, recall
            precision_recall = self.get_prec(
                mscs_dict=mscs_dict,
                precision_recall=precision_recall,
                mscs_origin="mscs_predicted_keywords",
                mscs_actual=mrmscs_dict[str(de)]
            )

        for runz, de in enumerate(prediction_table_references['de']):
            current_progress = round(
                (len(prediction_table_text) + len(
                    prediction_dict_keywords.keys()) +
                 runz + 1) / tot_rows * 100, 1
            )
            if current_progress != latest_progress \
                    and current_progress % 10 == 0:
                print(current_progress, '%')
                latest_progress = current_progress

            # collect mscs
            mscs_dict = {}
            mscs_dict['mscs_predicted_references'] = self.clean_list(
                string=prediction_dict_references[de]['predicted'],
                sep=", "
            )

            # calc precision, recall
            precision_recall = self.get_prec(
                mscs_dict=mscs_dict,
                precision_recall=precision_recall,
                mscs_origin="mscs_predicted_references",
                mscs_actual=mrmscs_dict[str(de)]
            )

        # plot data
        fig, ax = plt.subplots()
        pr = None
        for mscs_origin in precision_recall.keys():

            pr_rc = precision_recall[mscs_origin]
            precisions = []
            recalls = []
            cutoffs = []
            for p_r in pr_rc.items():
                cutoffs.append(p_r[0])
                precisions.append(np.mean(p_r[1]['precisions']))
                recalls.append(np.mean(p_r[1]['recalls']))
            if mscs_origin == "mscs_predicted_keywords":
                pr = {
                    "precisions": precisions,
                    "recalls": recalls
                }
            else:
                pass
            marker_dict = dict(
                zip(
                    precision_recall.keys(),
                    ['x', 's', 'o', '>']
                )
            )
            ax.scatter(
                recalls,
                precisions,
                marker=marker_dict[mscs_origin],
                s=10,
                label=mscs_origin
            )

        plt.title('Precision-Recall (ROC) Curve')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.xlim((0, 1))
        plt.ylim((0, 1))
        plt.xticks(np.arange(0, 1.01, 0.1))
        plt.yticks(np.arange(0, 1.01, 0.1))
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.savefig(
            f'{self.config.data_folder["save"]}prec-rec-curve_key.pdf',
            format="pdf",
            bbox_inches="tight"
        )
        plt.show()
        print("test end")

        return pr

    def get_precision_recall_boot(self, prediction_dict_keywords):
        pass

    def get_prec(
            self,
            mscs_dict,
            precision_recall,
            mscs_origin,
            mscs_actual
    ):

        mscs_predicted_full = mscs_dict[mscs_origin]

        for i in range(2, self.config.nr_msc_cutoff + 1):
            mscs_predicted = mscs_predicted_full[:i]
            mscs_intersection = [
                msc
                for msc in mscs_predicted
                if msc in mscs_actual
            ]

            if len(mscs_predicted) > 0:
                precision = len(mscs_intersection) / len(mscs_predicted)
            else:
                precision = 1

            if len(mscs_actual) > 0:
                recall = len(mscs_intersection) / len(mscs_actual)
            else:
                recall = 1

            try:
                precision_recall[
                    mscs_origin
                ][i]['precisions'].append(precision)
                precision_recall[
                    mscs_origin
                ][i]['recalls'].append(recall)
            except:
                try:
                    precision_recall[
                        mscs_origin
                    ][i]['precisions'] = [precision]
                    precision_recall[
                        mscs_origin
                    ][i]['recalls'] = [recall]
                except:
                    precision_recall[
                        mscs_origin
                    ][i] = {'precisions': [precision]}
                    precision_recall[
                        mscs_origin
                    ][i] = {'recalls': [recall]}
        return precision_recall