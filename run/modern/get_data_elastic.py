from zb_msc_classificator.config.definition import ConfigMap
from zb_msc_classificator.generate_mapper import MapElastic

collector = MapElastic(
    config=ConfigMap(
        store_data=True,
        data_size=200000
    )
)
collector.execute()
