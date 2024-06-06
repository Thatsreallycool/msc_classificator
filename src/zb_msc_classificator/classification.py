import json

from zb_msc_classificator.harmonize import Harmonizer
import pandas as pd


class Prediction:
    def __init__(self, config):
        self.config = config
        self.harmonizer = Harmonizer()
        self.map = self.get_map()
        self.test_data_dict = self.get_test_data_csv()


    def get_map(self):
        with open(self.config.admin_config.filepath_output.map, "r") as f:
            map = json.load(f)
        return map

    def get_test_data(self, data: list):
        pass

    def get_test_data_csv(self):
        filepath = self.config.admin_config.filepat_input.test_data
        test_data = pd.read_csv(filepath, delimiter=',')
        test_dict = {}
        for row in range(len(test_data)):
            de = test_data['de'][row]
            keywords = self.harmonizer.clean_csv_data(test_data['keyword'][row].split()
            mscs = self.harmonizer.clean_csv_data(test_data['msc'][row]).split()
            test_dict.update(
                {de:
                    {
                        "keywords": keywords,
                        "mscs": mscs
                    }
                }
            )
        return test_dict

    def execute(self):
        pass

    def store_prediction(self, filepath):
        pass