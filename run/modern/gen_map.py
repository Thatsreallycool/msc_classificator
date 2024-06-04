from zb_msc_classificator.generate_mapper import GenerateMap
from zb_msc_classificator.config.definition import ConfigGenerate
import time

my_cfg = ConfigGenerate(
    training_source='disk',
    store=False
)
gen = GenerateMap(
    config=my_cfg
)

starting_time = time.time()
print(len(gen.load_from_elastic()))
print(time.time() - starting_time)