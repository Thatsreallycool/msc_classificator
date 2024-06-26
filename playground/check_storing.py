from zb_msc_classificator.config.definition \
    import ConfigGenerate, AdminConfig, FilePathOutput
from zb_msc_classificator.tools import Toolbox
from zb_msc_classificator.generate_mapper import MapElastic
file = "/home/marcel/PycharmProjects/msc_classificator/" \
       "playground/data/test.pickle"
config = ConfigGenerate(
    store_data_elastic=True,
    admin_config=AdminConfig(
        filepath_output=FilePathOutput(
            data_elastic=file
        )
    )
)
run = MapElastic(config=config)
run.execute()

stored = run.data

tools = Toolbox()
loaded = tools.pickle_loader(filepath=config.admin_config.filepath_output.data_elastic)

print("")



