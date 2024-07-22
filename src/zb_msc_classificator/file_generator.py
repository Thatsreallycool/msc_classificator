from pathlib import Path
from pydantic import ValidationError
from zb_msc_classificator.config.admin_config import ConfigLoader, FilePaths
import os


class GenerateFiles:
    def __init__(self):
        self.config = ConfigLoader()
        todo = []
        try:
            filenames = self.config.get_filepaths()
            for data, file in filenames:
                if os.stat(file).st_size == 0:
                    todo.append(data)

        except ValidationError as e:
            fields = FilePaths.__fields__.keys()
            for error in e.errors():
                if error["loc"][0] in fields \
                        and error["type"] == 'value_error.path.not_exists':
                    data = error['loc'][0]
                    todo.append(data)
                    Path(self.config.config["FILEPATHS"][data]).touch()

        for data in todo:
            getattr(self, f"generate_{data}")()

    @staticmethod
    def generate_data_set_classificator():
        from zb_msc_classificator.generate_mapper import MapElastic
        from zb_msc_classificator.config.definition \
            import ConfigMap
        MapElastic(
            config=ConfigMap(
                store_data=True
            )
        ).execute()
        print("data set for classificator extracted from elastic search index!")

    @staticmethod
    def generate_data_set_entitylinking():
        from zb_msc_classificator.generate_mapper import MapElastic
        from zb_msc_classificator.config.definition \
            import ConfigMap, FilterDocuments
        MapElastic(
            config=ConfigMap(
                data_size=5000,
                store_data=True,
                create="entitylinking",
                filter_documents=FilterDocuments(
                    publication_year_start=None,
                    state=None
                )
            )
        ).execute()
        print("data set for entity linking extracted from elastic search "
              "index!")

    @staticmethod
    def generate_keywords_allowed():
        from zb_msc_classificator.entity_linking import EntityLink
        from zb_msc_classificator.config.definition import ConfigEntityLinking
        EntityLink(config=ConfigEntityLinking(generate_allow_list=True))
        print("keyword allow list generated!")

    @staticmethod
    def generate_map():
        from zb_msc_classificator.generate_mapper import GenerateMap
        from zb_msc_classificator.config.definition import ConfigGenerate
        GenerateMap(config=ConfigGenerate(store_map=True)).execute()
        print("map generated!")


