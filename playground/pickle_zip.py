from zb_msc_classificator.generate_mapper import MapElastic
from zb_msc_classificator.config.definition import ConfigGeneral
import time
import os

from zipfile import ZipFile

write_to_file = False
read_from_disk = False

filename = "test.pickle"
filefolder = "/home/marcel/PycharmProjects/msc_classificator/" \
           "playground/run_old_code/data/"
filepath = f"{filefolder}{filename}"

filepath_zip = "/home/marcel/PycharmProjects/msc_classificator/" \
           "playground/run_old_code/data/test.zip"


start = time.time()
with open(filepath, "r") as reader:
    map_elastic = reader.read()
print(f"file loaded after {time.time()-start} seconds!")
print(f"file size: {os.stat(filepath).st_size / (1024 * 1024)}MB!")

with ZipFile(filepath_zip, "w") as f:
    f.writestr(filename, map_elastic)
print(f"file zipped after {time.time()-start} seconds!")

data_from_zip = ZipFile(filepath_zip, 'r').read(filename)
print(f"file unzipped after {time.time()-start} seconds!")
print(f"is stored and loaded identical: {data_from_zip==map_elastic}")

if write_to_file:
    test = map_elastic.tools.compress(map_elastic)
    print(f"dump created after {time.time()-start} seconds!")
    print(f"char length: {len(test)}")


    filew = open(filepath, "w")
    filew.write(test)
    filew.close()
    print(f"dump stored after {time.time()-start} seconds!")

if read_from_disk:
    with open(filepath, "r") as reader:
        read_file = reader.read()
    print(f"file read after {time.time()-start} seconds!")
    print(f"char length: {len(read_file)}")
    print(f"is stored and loaded identical: {test==read_file}")

    read_test = map_elastic.tools.uncompress(read_file)
    print(f"unpickled after {time.time()-start} seconds!")
    print(f"file size: {os.stat(filepath).st_size/(1024*1024)}MB!")
    print(f"is stored and loaded identical: {map_elastic==read_test}")

