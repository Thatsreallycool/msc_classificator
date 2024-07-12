from zb_msc_classificator.config.definition import ConfigMap
from zb_msc_classificator.generate_mapper import MapElastic

from time import time

start = time()
collector = MapElastic(
    config=ConfigMap(
        store_data=True
    )
)
collector.execute()
print(f"This took {time()-start}s!")
