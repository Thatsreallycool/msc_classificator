from zb_msc_classificator.generate_mapper import MapElastic
from zb_msc_classificator.config.definition import ConfigGenerate

my_id = 0

for i in range(50):

    run = MapElastic(
        config=ConfigGenerate(
            store_data_elastic=True,
            data_size=10000
        )
    )
    print(run.query)
    run.execute()
    if my_id == run.latest_id:
        break
    my_id = run.latest_id
    print(f"latest id: {run.latest_id}")

