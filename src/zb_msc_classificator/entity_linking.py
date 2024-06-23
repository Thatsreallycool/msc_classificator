from zb_msc_classificator.harmonize import Harmonizer
from nltk import ngrams


class EntityLink:
    def __init__(self, config):
        self.config = config
        self.harmonize = Harmonizer()

    def execute(self, text):
        tokens = self.clean_text_tokenize(text)
        for n in self.config.ngram_lengths:
            all_ngrams = self.get_ngrams(tokens=tokens, ngram_length=n)
            #TODO: get from index and position and url
            for current_ngram in all_ngrams:


        linked_keywords = {}
        return linked_keywords

    def clean_text_tokenize(self, text):
        """
        remove punctuation, lemmatization and potentially more preprocessing
        routines
        :param text: string of continous text, probably an abstract
        :return: a continuous string of words divided by space, removed any
        unwanted character
        """
        canonicalized = self.harmonize.canonicalize(text)
        removed_stopwords = self.harmonize.remove_stopwords(canonicalized)
        removed_punctuation = self.harmonize.remove_punctuation(
            removed_stopwords
        )
        tokenized = removed_punctuation.split()
        lemmatized = self.harmonize.lemmatization(token_list=tokenized)
        return lemmatized

    @staticmethod
    def get_ngrams(tokens: list, ngram_length: int):
        return list(ngrams(tokens, ngram_length))

