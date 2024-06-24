from zb_msc_classificator.config.definition import ConfigGenerate
from zb_msc_classificator.generate_mapper import GenerateMap

gen = GenerateMap(
    config=ConfigGenerate(
        training_source="elastic_snapshot",
        store_map=True
    )
)

gen.execute()