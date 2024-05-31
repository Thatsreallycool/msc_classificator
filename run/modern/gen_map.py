from zb_msc_classificator.generate_mapper import GenerateMap
from zb_msc_classificator.config.definition import ConfigGenerate

my_cfg = ConfigGenerate(
    training_source='disk',
    store=True
)
gen = GenerateMap(
    config=my_cfg
)

print(len(gen.training_data))
print(len(gen.map.keys()))
print(my_cfg)
print(gen.done)