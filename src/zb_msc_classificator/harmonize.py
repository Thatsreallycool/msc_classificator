import pandas as pd

from zb_msc_classificator.tools import Toolbox
from zb_msc_classificator.config.definition import ConfigGeneral

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords as stopwords_nltk

import re

import collections


class Harmonizer:
    # TODO: remove more special ,
    #  - stop_punctuation = '.,;:!?' # ()\\"\'[]{}<>`~@#$%^&*_-=+|/
    #  - canonicalize
    #  - lemmatization (grammatikalische Normierung)
    #  from nltk.stem import WordNetLemmatizer
    #  preprocesser = WordNetLemmatizer()
    #  entity = ' '.join([preprocesser.lemmatize(word) for word in nngram])
    #  reihenfolge train / test
    def __init__(self, config=ConfigGeneral()):
        self.config = config
        self.stop_punctuation = [".", ",", ";", ":", "!", "?", " ' ", "(", ")"]
        self.stop_words = self.get_stopwords()
        self.replacements = {k: "" for k in self.stop_words}

    def get_stopwords(self):
        tools = Toolbox()
        language = self.config.language.name
        all_stopwords = stopwords_nltk.words(language) + tools.txt_load(
            self.config.admin_config.filepath_input.stopwords
        )
        return list(set(all_stopwords))

    def replace_any(self, match):
        return self.replacements[match.group(0)]

    def check_for_stopwords(self, text):
        if text is None:
            return [False]
        else:
            return [
                True if item in self.stop_words
                else False
                for item in text.split()
            ]

    @staticmethod
    def find_duplicates(text_list):
        counter = collections.Counter(text_list)
        duplicates = [i for i in counter if counter[i] != 1]
        return {
            item: [i for i, j in enumerate(text_list) if j == item]
            for item in duplicates
            if item is not None
        }

    def remove_stopwords(self, text, position_in_text=None):
        if text is None or isinstance(text, int):
            return text
        if position_in_text is None:
            return re.sub(
                '|'.join(r'\b%s\b' % re.escape(s) for s in self.replacements),
                self.replace_any,
                text
            )
        elif isinstance(position_in_text, int):
            word_list = text.split()
            if word_list[position_in_text] in self.stop_words:
                del word_list[position_in_text]
                return ' '.join(word_list)
            else:
                return text
        else:
            raise ValueError(f"please choose a number between -1 and the "
                             "number of words in this text: '{text}'")

    def transform_csv_to_list_of_tuples(self, csv_data: pd.DataFrame):
        keyword_msc_list = []
        tools = Toolbox()
        for row in csv_data.itertuples():
            msc_list = tools.str_spaces_to_list(
                string=self.clean_csv_data(
                    string_to_clean=row.msc
                ),
                delimiter=", "
            )
            keyword_list = tools.str_spaces_to_list(
                string=self.clean_csv_data(
                    string_to_clean=row.keyword
                ),
                delimiter=","
            )
            keyword_list = [
                self.remove_special_char(item)
                for item in keyword_list
            ]
            keyword_msc_list.append((keyword_list, msc_list))
        return keyword_msc_list

    def remove_punctuation_text(self, text: str):
        for dot in self.stop_punctuation:
            text = text.replace(dot, " ")
        return text

    @staticmethod
    def lemmatization(token_list):
        preprocessor = WordNetLemmatizer()
        return [preprocessor.lemmatize(word) for word in token_list]

    @staticmethod
    def canonicalize(text: str):
        return text.lower()

    @staticmethod
    def clean_csv_data(string_to_clean: str):
        """
        :param string_to_clean: remove specific special characters from string
        :return: cleaned string
        """
        if not isinstance(string_to_clean, str):
            return ""
        else:
            return string_to_clean.replace(
                '[', ''
            ).replace(
                ']', ''
            ).replace(
                '\\', ''
            ).replace(
                "'", ''
            )

    @staticmethod
    def remove_special_char(string_to_clean: str):
        if not isinstance(string_to_clean, str):
            return ""
        else:
            string_to_clean = string_to_clean.lstrip().rstrip()
            #TODO put this in config
            for clean_from in [',', "'", '"', "`", '\\']:
                string_to_clean = string_to_clean.strip(clean_from)
            return string_to_clean