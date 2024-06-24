from zb_msc_classificator.harmonize import Harmonizer
from nltk import ngrams

from zb_msc_classificator.tools import Toolbox

from SPARQLWrapper import SPARQLWrapper, JSON


class EntityLink:
    def __init__(self, config):
        self.config = config
        self.harmonize = Harmonizer()
        self.tools = Toolbox()
        self.map = self.tools.load_data(
            filepath=config.admin_config.filepath_output.map
        )

    def execute(self, text):
        from time import time
        tstart = time()
        text_tokens = self.tokenize(text=text)
        print(time()-tstart)
        preprocessed_tokens = self.harmonize.lemmatization(
            self.tokenize(
                self.harmonize.canonicalize(
                    self.harmonize.remove_punctuation_text(
                        text=text
                    )
                )
            )
        )
        print(time() - tstart)
        linked_keywords = []
        for n in self.config.ngram_lengths:
            ngrams = self.removing_entities(
                entity_list=self.get_ngrams(
                    tokens=preprocessed_tokens,
                    ngram_length=n
                )
            )

            print("ngrams", time() - tstart)
            print("checked map")
            # TODO: can i make a combined sparql request for performance reasons?
            urls = [
                self.get_wikidata_qid_wikipedia_url_sparql(entity=item)
                for item in ngrams
            ]
            print("after urls", time() - tstart)
            ngram_coords = self.get_ngram_coords(
                text=text,
                tokens=text_tokens,
                ngram_length=n
            )
            print("after ngram coords", time() - tstart)
            for item_nr, url in enumerate(urls):
                if url is not None:
                    if isinstance(url, int):
                        my_url = urls[url]
                    else:
                        my_url = url
                    linked_keywords.append(
                        {
                            'entity': ngram_coords[item_nr]['ngram'],
                            'span': [
                                ngram_coords[item_nr]['start'],
                                ngram_coords[item_nr]['end']
                            ],
                            'link': my_url
                        }
                    )
                    print(
                        type(
                            [
                                ngram_coords[item_nr]['start'],
                                ngram_coords[item_nr]['end']
                            ]
                        )
                    )
            print("after creating", time() - tstart)

        return linked_keywords

    def removing_entities(self, entity_list: list):
        """
        removing for performance reasons:
            - if all words are stopwords
            - if last word is stopword (only last word will be removed)
            - entities are already in list (return 2nd set of coordinates)
        :param entity_list: a list of text snippets
        :return: a list of text snippets
        """

        entity_list = [
            item if item in self.map.keys()
            else None
            for item in entity_list
        ]

        entity_list = [
            None if all(self.harmonize.check_for_stopwords(text=item))
            else item
            for item in entity_list
        ]

        entity_list = [
            self.harmonize.remove_stopwords(
                text=item,
                position_in_text=-1
            )
            for item in entity_list
        ]

        duplicates = self.harmonize.find_duplicates(entity_list)
        print(duplicates)
        if duplicates.keys():
            for coords in duplicates.values():
                for dup in coords[1:len(coords)]:
                    entity_list[dup] = coords[0]

        return entity_list

    def get_wikidata_qid_wikipedia_url_sparql(
            self,
            entity: str,
            include_aliases: bool = True
    ):
        """
        Get Wikidata QID and Wikipedia URL
        :param entity: term to find online
        :param include_aliases: bool for finding similar terms
        :return:
        """
        if entity is None or isinstance(entity, int):
            return entity
        try:
            # Initialize SPARQLWrapper
            sparql = SPARQLWrapper(self.config.sparql_link)

            sparql_query_string = self.get_sparql_query_string(
                entity,
                include_aliases
            )

            # Set the query and format
            sparql.setQuery(sparql_query_string)
            sparql.setReturnFormat(JSON)

            # Execute the query
            results = sparql.query().convert()

            # Extract the QID and sitelink
            bindings = results['results']['bindings']
            if bindings:
                sitelink = bindings[0].get('sitelink', {}).get('value', None)

                # Process sitelink to create the Wikipedia URL
                if sitelink:
                    page_title = sitelink.split('/')[-1].replace(' ', '_')
                    url = f"https://en.wikipedia.org/wiki/{page_title}"
                else:
                    url = None
            else:
                url = None
        except Exception as e:
            print(f'Error: {e}')
            url = None

        return url

    def get_sparql_query_string(self, name, include_aliases=True):
        lang = self.config.language.value
        # Define the SPARQL query
        if not include_aliases:
            # without aliases
            sparql_query_string = f"""
            SELECT ?item ?sitelink WHERE {{
            ?item rdfs:label "{name}"@{lang}.OPTIONAL {{ 
            ?sitelink schema:about ?item; schema:inLanguage "{lang}"; 
            schema:isPartOf <https://{lang}.wikipedia.org/>. }}
            }}
            """
        else:
            # with aliases
            sparql_query_string = f"""
            SELECT DISTINCT ?item ?sitelink WHERE {{
            {{
            ?item rdfs:label "{name}"@{lang} .
            OPTIONAL {{ 
            ?sitelink schema:about ?item; schema:inLanguage "{lang}"; 
            schema:isPartOf <https://{lang}.wikipedia.org/>. 
            }}
            }}
            UNION
            {{
            ?item skos:altLabel "{name}"@{lang} .
            OPTIONAL {{ 
            ?sitelink schema:about ?item; schema:inLanguage "{lang}"; 
            schema:isPartOf <https://{lang}.wikipedia.org/>. 
            }}
            }}
            }}
            """

        return sparql_query_string

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
    def get_ngram_coords(text: str, tokens: list, ngram_length: int):
        ngram_coords = []
        for ngram in ngrams(sequence=tokens, n=ngram_length):
            snippet = ' '.join(ngram)
            start = text.find(snippet)
            ngram_coords.append(
                {
                    'ngram': snippet,
                    'start': start,
                    'end': start + len(snippet)
                }
            )
        return ngram_coords

    @staticmethod
    def get_ngrams(tokens: list, ngram_length: int):
        return [
            ' '.join(item)
            for item in ngrams(sequence=tokens, n=ngram_length)
        ]

    @staticmethod
    def tokenize(text: str, separator: str = None):
        """
        :param text: abstract text separated usually by space
        :param separator: default is none, then space is the separator
        :return: text tokens
        """
        return text.split(separator)
