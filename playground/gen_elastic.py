import time
from zb_msc_classificator.generate_mapper import GenerateMap
from zb_msc_classificator.config.definition import ConfigGenerate

start = time.time()
gen = GenerateMap(
    config=ConfigGenerate(
        training_source="elastic",
        store=True
    )
)
print(f"datablob done after {time.time()-start} seconds!")