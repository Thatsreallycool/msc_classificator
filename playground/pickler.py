
test=[(item, item+1) for item in range(10)]
filepath = "/home/marcel/PycharmProjects/msc_classificator/" \
           "playground/run_old_code/data/test.pickle"


import base64
import zlib
import pickle
print(test)
print(pickle.dumps(test, protocol=4))
print(zlib.compress(
        pickle.dumps(test, protocol=4)
))
compressed_stuff = base64.b64encode(
    zlib.compress(
        pickle.dumps(test, protocol=4)
    )
).decode()

print(compressed_stuff)
print(len(compressed_stuff))
print("done\n")

print(compressed_stuff.encode())
print(base64.b64decode(compressed_stuff.encode()))
print(zlib.decompress(
        base64.b64decode(
            compressed_stuff.encode()
        )
    )
)
print(pickle.loads(
    zlib.decompress(
        base64.b64decode(
            compressed_stuff.encode()
        )
    )
))

