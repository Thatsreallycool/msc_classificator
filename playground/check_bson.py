import collections  # From Python standard library.
import bson
from bson.codec_options import CodecOptions

mydata = {
    "1": "2",
    "3": "213",
    "4": "sdsfdf",
    "5": ["1","2","3"],
    "6": {"2":"2", "3":"4"}
}

bdata = bson.BSON.encode(mydata)
print(bdata)

decoded_doc = bson.BSON(bdata).decode()

print(decoded_doc)
options = CodecOptions(document_class=collections.OrderedDict)
decoded_doc = bson.BSON(bdata).decode(codec_options=options)
print(decoded_doc)

import base64
import zlib
z = zlib.compress(bdata)
print(z)
cz = base64.b64encode(z).decode()
print(cz)

ucz = base64.b64decode(cz.encode())
ucuz = zlib.decompress(ucz)
print(bson.BSON(ucuz).decode())

