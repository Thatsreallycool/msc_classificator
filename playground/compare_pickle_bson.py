from decimal import Decimal
from random import randint

from zb_msc_classificator.generate_mapper import MapElastic
from zb_msc_classificator.config.definition import ConfigGeneral


from time import time

import os
data1 = False
data2 = False
data3 = True

data_range = 100000
if data1:
    data = {
        str(item): randint(0, 100)
        for item in range(data_range)
    }
if data2:
    data = {
        str(item): str(item+1)
        for item in range(data_range)
    }
if data3:
    start_es = time()
    data3 = MapElastic(
        config=ConfigGeneral()
    )
    data = {
        str(i): item
        for i, item in enumerate(data3.data)
    }
    print(f"nr. of items: {len(data.keys())}")
    print(f"it took: {round((time()-start_es)/60, 1)}min")

#print(data)

import base64
import zlib
work_folder = "/home/marcel/data/PycharmProjects/" \
                  "msc_classificator/playground/data/"
home_folder = "/home/marcel/PycharmProjects/msc_classificator" \
                    "/playground/run_old_code/data/"
data_folder = home_folder

filepath_pickle = data_folder+"test.pickle"
start_pickle = time()
import pickle

pickle_stage1 = pickle.dumps(data, protocol=5)
pickle_stage2 = zlib.compress(pickle_stage1)
pickle_stage3 = base64.b64encode(pickle_stage2).decode()
packed_pickle = time()-start_pickle
with open(filepath_pickle, "w") as fwp:
    fwp.write(pickle_stage3)
stored_pickle = time()-start_pickle

with open(filepath_pickle, "r") as frp:
    pickled = frp.read()
loaded_pickle = time()-start_pickle

unpickle_stage3 = base64.b64decode(pickled.encode())
unpickle_stage2 = zlib.decompress(unpickle_stage3)
unpickle_stage1 = pickle.loads(unpickle_stage2)
end_pickle = time()-stored_pickle -start_pickle
print(f"pickle intact: {data == unpickle_stage1}")

filepath_bson = data_folder+"test.bson"
start_bson = time()
import bson
bson_stage1 = bson.BSON.encode(data)
bson_stage2 = zlib.compress(bson_stage1)
bson_stage3 = base64.b64encode(bson_stage2).decode()
packed_bson = time() - start_bson
with open(filepath_bson, "w") as fwb:
    fwb.write(bson_stage3)
stored_bson = time()- start_bson

with open(filepath_bson, "r") as frb:
    bsoned = frb.read()
loaded_bson = time() - start_bson
unbson_stage3 = base64.b64decode(bsoned.encode())
unbson_stage2 = zlib.decompress(unbson_stage3)
unbson_stage1 = bson.BSON(unbson_stage2).decode()
# print(unbson_stage1)
end_bson = time()-stored_bson - start_bson
print(f"bson intact: {unbson_stage1==data}")

filepath_zip = data_folder+"test.gz"

start_gzip = time()
import gzip
import json
with gzip.open(filepath_zip, 'wt') as fw:
    json.dump(data, fw, indent=4)
    fw.write("\n")
packed_gzip = time()-start_gzip
with gzip.open(filepath_zip, 'rb') as fr:
    ungzip = fr.read()
unj = json.loads(ungzip.decode())
end_gzip = time()-packed_gzip-start_gzip
print(f"zip intact: {data == unj}")


print(f"pickle size: {os.path.getsize(filepath_pickle)}, "
      f"storing: {Decimal(stored_pickle):.2E}s, "
      f"done: {Decimal(end_pickle):.2E}s")
print("\n")
print(f"bson size: {os.path.getsize(filepath_bson)}, "
      f"storing: {Decimal(stored_bson):.2E}s, "
      f"done: {Decimal(end_bson):.2E}s")
print("\n")
print(f"zip size: {os.path.getsize(filepath_zip)}, "
      f"packing: {Decimal(packed_gzip):.2E}s, "
      f"done: {Decimal(end_gzip):.2E}s")
print("\n")

print(f"diff len(p-b): {len(pickle_stage3)-len(bson_stage3)}, "
      f"diff packing time: {Decimal(packed_pickle-packed_bson):.2E}s, "
      f"diff total time: {Decimal(end_pickle-end_bson):.2E}s.")


