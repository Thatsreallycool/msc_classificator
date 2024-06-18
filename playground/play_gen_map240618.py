from zb_msc_classificator.config.definition import ConfigGenerate
from zb_msc_classificator.generate_mapper import GenerateMap
from time import time

start = time()
gen = GenerateMap(
    config=ConfigGenerate(
        training_source='elastic_snapshot',
        store_map=True
    )
)
loaded = time()
print(f"data loaded, items: {len(gen.training_data)}")

my_map = gen.execute()
executed = time()
filepath_zip = "/home/marcel/data/projects/msc_fine_grained/240618/test.gz"

import gzip
import json

with gzip.open(filepath_zip, 'wt') as fw:
    json.dump(my_map, fw, indent=4)
    fw.write("\n")
packed = time()

with gzip.open(filepath_zip, 'rb') as fr:
    ungzip = fr.read()

unj = json.loads(ungzip.decode())
unpacked = time()

print(f"checked: {unj == my_map}")
print(f"init time: {loaded - start}")
print(f"gen time: {executed - loaded}")
print(f"packing time: {packed - executed}")
print(f"readying time: {unpacked - packed}")

