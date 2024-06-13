from decimal import Decimal
from random import randint

from zb_msc_classificator.generate_mapper import MapElastic
from zb_msc_classificator.config.definition import ConfigGeneral

data_range = 100
data1 = {
    str(item): randint(0, 100)
    for item in range(data_range)
}
data2 = {
    str(item): str(item+1)
    for item in range(data_range)
}
data3 = MapElastic(
    config=ConfigGeneral()
)

data = {
    str(i): item
    for i, item in enumerate(data3.data)
}

#print(data)

from time import time
import base64
import zlib

start_pickle = time()
import pickle

pickle_stage1 = pickle.dumps(data, protocol=5)
pickle_stage2 = zlib.compress(pickle_stage1)
pickle_stage3 = base64.b64encode(pickle_stage2).decode()
packed_pickle = time()-start_pickle

unpickle_stage3 = base64.b64decode(pickle_stage3.encode())
unpickle_stage2 = zlib.decompress(unpickle_stage3)
unpickle_stage1 = pickle.loads(unpickle_stage2)
print(data == unpickle_stage1)
end_pickle = time()-start_pickle

start_bson = time()
import bson
bson_stage1 = bson.BSON.encode(data)
bson_stage2 = zlib.compress(bson_stage1)
bson_stage3 = base64.b64encode(bson_stage2).decode()
packed_bson = time() - start_bson

unbson_stage3 = base64.b64decode(bson_stage3.encode())
unbson_stage2 = zlib.decompress(unbson_stage3)
unbson_stage1 = bson.BSON(unbson_stage2).decode()
# print(unbson_stage1)
end_bson = time()-start_bson

print(f"pickle size: {len(pickle_stage3)}, "
      f"packing: {Decimal(packed_pickle):.2E}s, "
      f"done: {Decimal(end_pickle):.2E}s")
print("\n")
print(f"bson size: {len(bson_stage3)}, "
      f"packing: {Decimal(packed_bson):.2E}s, "
      f"done: {Decimal(end_bson):.2E}s")

print(f"diff len(p-b): {len(pickle_stage3)-len(bson_stage3)}, "
      f"diff packing time: {Decimal(packed_pickle-packed_bson):.2E}s, "
      f"diff total time: {Decimal(end_pickle-end_bson):.2E}s.")
