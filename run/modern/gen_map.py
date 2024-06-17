from zb_msc_classificator.generate_mapper import GenerateMap
from zb_msc_classificator.config.definition import ConfigGenerate

my_cfg = ConfigGenerate(
    training_source='elastic_live',
    store_map=True
)
gen = GenerateMap(
    config=my_cfg
)
