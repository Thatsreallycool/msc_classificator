from tests.testfiles.example_test_set import example_test_set


def flatten(xss):
    return [x.lower() for xs in xss for x in xs]


print(example_test_set)

from zb_msc_classificator.tools import Toolbox
from zb_msc_classificator.config.definition import ConfigGeneral

config = ConfigGeneral()
tools = Toolbox()
data_filename = config.admin_config.file_paths.data_stored
data = tools.load_data(filepath=data_filename)

msc_cooc = [val['mscs'] for val in data.values()]
kw_cooc = [val['keywords'] for val in data.values()]

mscs = set(flatten(msc_cooc))
keywords = set(flatten(kw_cooc))

from itertools import combinations

keyword_cooc = tools.nested_dict(layers=2, data_type=int)
MSC_cooc = tools.nested_dict(layers=2, data_type=int)
for m in msc_cooc:
    for item in combinations(m, 2):
        MSC_cooc[item[0]][item[1]] += 1
for kw in kw_cooc:
    for item in combinations(kw, 2):
        keyword_cooc[item[0]][item[1]] += 1

import itertools
km_cooc = tools.nested_dict(layers=2, data_type=int)
for km in data.values():
    k = km["keywords"]
    m = km["mscs"]
    all_combs = itertools.product(k, m)
    for item in all_combs:
        km_cooc[item[0]][item[1]] += 1


print(len(keyword_cooc.keys()))
one_set = list(example_test_set.values())[0]
print(
    [
        km_cooc[item]
        for item in one_set['keywords']
    ]
)

tools.store_data(
    filepath="/home/marcel/PycharmProjects/msc_classificator/data"
             "/kw_m_cooccurence.gz",
    data=km_cooc
)