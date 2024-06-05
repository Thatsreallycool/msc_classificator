index_name = "zbmath_staging_final_documents"

myquery = {
            "query": {
                'function_score': {
                    'query': {
                        'bool': {
                            'must': {
                                'range': {
                                    'de': {'gte': 0, 'lte': 200000}
                                }
                            }
                        }
                    },
                    'field_value_factor': {'field': 'score_linear'}
                }
            }
        }

from elasticsearch.helpers import scan

results = scan()