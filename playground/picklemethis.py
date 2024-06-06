from zb_msc_classificator.generate_mapper import MapElastic
from zb_msc_classificator.config.definition import ConfigGeneral
import time
import os

get_from_el = False
write_to_file = False
read_from_disk = False

filepath = "/home/marcel/PycharmProjects/msc_classificator/" \
           "playground/run_old_code/data/test.pickle"

start = time.time()
if get_from_el:
    map_elastic = MapElastic(
        config=ConfigGeneral()
    )
    print(f"size: {len(map_elastic.data)}")
    print(f"datablob done after {time.time()-start} seconds!")


if write_to_file:
    test = map_elastic.tools.compress(map_elastic.data)
    print(f"dump created after {time.time()-start} seconds!")
    print(f"char length: {len(test)}")


    filew = open(filepath, "w")
    filew.write(test)
    filew.close()
    print(f"dump stored after {time.time()-start} seconds!")

    with open(filepath, "r") as reader:
        read_file = reader.read()
    print(f"file read after {time.time()-start} seconds!")
    print(f"char length: {len(read_file)}")
    print(f"is stored and loaded identical: {test==read_file}")

    read_test = map_elastic.tools.uncompress(read_file)
    print(f"unpickled after {time.time()-start} seconds!")
    print(f"file size: {os.stat(filepath).st_size/(1024*1024)}MB!")
    print(f"is stored and loaded identical: {map_elastic.data==read_test}")

