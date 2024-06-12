import pandas as pd

from zb_msc_classificator.tools import Toolbox


class Harmonizer:
    # TODO: remove more special ,
    #  - stop_punctuation = '.,;:!?' # ()\\"\'[]{}<>`~@#$%^&*_-=+|/
    #  - canonicalize
    #  - lemmatization (grammatikalische Normierung)
    #  from nltk.stem import WordNetLemmatizer
    #  preprocesser = WordNetLemmatizer()
    #  entity = ' '.join([preprocesser.lemmatize(word) for word in nngram])
    #  reihenfolge train / test
    def __init__(self):
        self.tools = Toolbox()

    def transform_csv_to_list_of_tuples(self, csv_data: pd.DataFrame):
        keyword_msc_list = []
        for row in csv_data.itertuples():
            msc_list = self.tools.str_spaces_to_list(
                string=self.clean_csv_data(
                    string_to_clean=row.msc
                ),
                delimiter=", "
            )
            keyword_list = self.tools.str_spaces_to_list(
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