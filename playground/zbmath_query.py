from zb_msc_classificator import MapElastic
from zb_msc_classificator.config.definition import ConfigMap

me = MapElastic(
    config=ConfigMap(
        diff_only=False,
        store_data=False
    )
)
print(me.get_zbmath_query())
test_query = {"query": {'function_score': {'query': {'bool': {'must': [{'bool': {'must': {'range': {'py': {'gte': 2000, 'lte': 2024}}}}}, {'term': {'st': 'j'}}]}}, 'field_value_factor': {'field': 'score_linear'}}}}
print(me.query == test_query)