import numpy as np

from zb_msc_classificator.tools import Toolbox
from zb_msc_classificator.config.definition import ConfigGeneral

config = ConfigGeneral()
tools = Toolbox()
data_filename = config.admin_config.file_paths.data_stored
data = tools.load_data(filepath=data_filename)


def flatten(xss):
    return [x.lower() for xs in xss for x in xs]

from time import time

start = time()
msc_cooc = [
    val['mscs']
    for val in data.values()
]
kw_cooc = [
    val['keywords']
    for val in data.values()
]
mscs = set(flatten(msc_cooc))

keywords = set(flatten(kw_cooc))
print(f"took {time()-start}s!")

from itertools import combinations, chain
"""start2 = time()
m2 = set(chain(*[
            val['mscs']
            for val in data.values()
        ]))
k2 = set(chain(*[
            val['keywords']
            for val in data.values()
        ]))
print(f"now {time()-start2}s")
"""

msc_state = list(mscs)

start_c = time()
from collections import defaultdict
obs_k = defaultdict(int)
obs_m = defaultdict(int)
for run, msc_input in enumerate(msc_cooc):
    if not run%500000:
        print(f"{round(run*100/len(msc_cooc), 2)}% "
              f"at time: {round(time()-start_c, 2)}s")
    for m in [str(item).lower() for item in combinations(msc_input, 2)]:
        obs_m[m] += 1
    for k in [str(item).lower() for item in combinations(kw_cooc[run], 2)]:
        obs_k[k] += 1

print(len(obs_m.keys()))
print(len(obs_k.keys()))

import matplotlib.pyplot as plt
my_data = list(obs_k.values())
new_list1 = [item for item in my_data if item>1]
print(len(my_data))
print(len(new_list1))
new_list2 = [item for item in my_data if item>2]
print(len(new_list2))
plt.plot(np.log10(sorted(new_list2)))
plt.show()

from collections import Counter
print(Counter(my_data))