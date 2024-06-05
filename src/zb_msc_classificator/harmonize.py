class Harmonizer:
    # TODO: remove more special ,
    #  - stop_punctuation = '.,;:!?' # ()\\"\'[]{}<>`~@#$%^&*_-=+|/
    #  - canonicalize
    #  - lemmatization (grammatikalische Normierung)
    #  from nltk.stem import WordNetLemmatizer
    #  preprocesser = WordNetLemmatizer()
    #  entity = ' '.join([preprocesser.lemmatize(word) for word in nngram])
    #  reihenfolge train / test

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