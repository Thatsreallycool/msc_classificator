from nltk import ngrams

from zb_msc_classificator.harmonize import Harmonizer
from zb_msc_classificator.tools import Toolbox

from zb_msc_classificator.config.definition \
    import ConfigEntityLinking, ConfigLoader, AdminConfig

from SPARQLWrapper import SPARQLWrapper, JSON


class EntityLink:
    def __init__(
            self,
            config: ConfigEntityLinking = ConfigEntityLinking()
    ):
        self.config = config
        self.harmonize = Harmonizer()
        self.tools = Toolbox()
        self.keywords_allowed = self.get_allow_list_keywords()
        self.sparql = SPARQLWrapper(endpoint=self.config.sparql_link)

    def execute(
            self,
            text: str
    ):
        text_tokens = self.tokenize(text=text)
        preprocessed_tokens = self.harmonize.lemmatization(
            self.tokenize(
                self.harmonize.canonicalize(
                    self.harmonize.remove_punctuation_text(
                        text=text
                    )
                )
            )
        )
        linked_keywords = []
        for n in self.config.ngram_lengths:
            ngrams = self.removing_entities(
                entity_list=self.get_ngrams(
                    tokens=preprocessed_tokens,
                    ngram_length=n
                )
            )

            # TODO: can i make a combined sparql request for performance reasons?
            urls = [
                self.get_wikidata_qid_wikipedia_url_sparql(entity=item)
                for item in ngrams
            ]
            ngram_coords = self.get_ngram_coords(
                text=text,
                tokens=text_tokens,
                ngram_length=n
            )
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
        return linked_keywords

    @staticmethod
    def tokenize(
            text: str,
            separator: str = None
    ):
        """
        :param text: abstract text separated usually by space
        :param separator: default is none, then space is the separator
        :return: text tokens
        """
        return text.split(separator)

    @staticmethod
    def get_ngrams(
            tokens: list,
            ngram_length: int
    ):
        """
        input are preprocessed tokens that are turned into ngrams for keyword
        recognition
        :param tokens: preprocessed token
        :param ngram_length: int- nr of token
        :return: list of tuples from ngrams() are turend into text snippets
        for keyword recognition in mapper
        """
        return [
            ' '.join(item)
            for item in ngrams(sequence=tokens, n=ngram_length)
        ]

    @staticmethod
    def get_ngram_coords(
            text: str,
            tokens: list,
            ngram_length: int
    ):
        ngram_coords = []
        """
        find ngrams in text to return coordinates and mark original text 
        snippets
        :param text: original text
        :param tokens: original text snippets to search in text
        :param ngram_length: length of ngram
        :return: list of dicts:
        [{'ngram': <str>, 'start': <int>, 'end': <int>}, {...}, ...]
        """
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

    def removing_entities(
            self,
            entity_list: list
    ):
        """
        removing for performance reasons:
            - if all words are stopwords
            - if last word is stopword (only last word will be removed)
            - entities are already in list (return 2nd set of coordinates)
            - entities that are not in mapper
        :param entity_list: a list of text snippets
        :return: a list of text snippets
        """

        entity_list = [
            item if item in self.keywords_allowed
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
        :return: url of request
        performance update:
            if keyword was already search: entity is <int>: return without
            accessing sparql
            if keyword was removed due to being insignificant: entity is
            None: return without sparql
        """
        if entity is None or isinstance(entity, int):
            return entity
        try:
            sparql_query_string = self.get_sparql_query_string(
                name=entity,
                include_aliases=include_aliases
            )

            # Set the query and format
            self.sparql.setQuery(sparql_query_string)
            self.sparql.setReturnFormat(JSON)

            # Execute the query
            results = self.sparql.query().convert()

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

    def get_sparql_query_string(
            self,
            name: str,
            include_aliases=True
    ):
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

    def get_allow_list_keywords(self):
        return self.tools.load_data(
            filepath=self.config.file_paths.keywords_allowed
        )

    def generate_allow_list_keywords(self):
        data_set = self.tools.load_data(
            filepath=self.config.file_paths.data_set
        )
        self.tools.store_data(
            filepath=self.config.file_paths.keywords_allowed,
            data=self.tools.transform_data_set_to_list(
                data_set=data_set,
                subkey="keywords"
            )
        )
