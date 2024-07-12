import unittest
from zb_msc_classificator import MapElastic
from zb_msc_classificator.config.definition import ConfigMap


class GenerateTest(unittest.TestCase):
    def test_get_zbmath_query(self):
        map_test = MapElastic(
            config=ConfigMap(
                diff_only=False,
                store_data=False
            )
        )
        zbmath_query = "py:2000-2024 & st:j"
        expected_elastic_query = {
            'function_score': {
                'query': {
                    'bool': {
                        'must': [
                            {
                                'bool': {
                                    'must': {
                                        'range': {
                                            'py': {'gte': 2000, 'lte': 2024}
                                        }
                                    }
                                }
                            }, {
                                'term': {'st': 'j'}
                            }
                        ]
                    }
                },
                'field_value_factor': {'field': 'score_linear'}
            }
        }
        assert map_test.query == expected_elastic_query
