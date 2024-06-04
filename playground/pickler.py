
test=[(item, item+1) for item in range(10)]

import base64
import zlib
import pickle
print(test)
compressed_stuff = base64.b64encode(
    zlib.compress(
        pickle.dumps(test, protocol=4)
    )
).decode()

print(compressed_stuff)

print(pickle.loads(
    zlib.decompress(
        base64.b64decode(
            compressed_stuff.encode()
        )
    )
))

