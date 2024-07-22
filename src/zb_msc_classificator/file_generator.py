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
    def generate_data_set():
        from zb_msc_classificator.generate_mapper import MapElastic
        MapElastic().execute()

    def generate_keywords_allowed(self):
        from zb_msc_classificator.entity_linking import EntityLink
        from zb_msc_classificator.config.definition import ConfigEntityLinking
        EntityLink(config=ConfigEntityLinking(generate_allow_list=True))

    def generate_map(self):
        print("map!")

