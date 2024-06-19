import pandas as pd

filename = "/home/marcel/data/projects/msc_fine_grained/data/out_zenodo.csv"

q = pd.read_csv(filename, delimiter=",")

print(len(q))

from numpy import isnan

msc_list = list(q.msc.values)
keyword_list = list(q.keyword.values)

print(
    sum(
        [
            1
            for i in range(len(msc_list))
            if isinstance(msc_list[i], str) and isinstance(keyword_list[i], str)
        ]
    )
)