import json
import os.path

from zb_msc_classificator.harmonize import Harmonizer
from zb_msc_classificator.tools import Toolbox
import pandas as pd


class Prediction:
    def __init__(self, config):
        self.config = config
        self.harmonizer = Harmonizer()
        self.tools = Toolbox()
        # TODO get map from zip!
        self.map = self.get_map(
            filepath=self.config.admin_config.filepath_output.map_zipped
        )
        self.test_data_dict = self.get_test_data_csv()

    def get_map(self, filepath: str):
        if os.path.isfile(filepath):
            return self.tools.zip_load(filepath=filepath)
        else:
            raise FileNotFoundError("map file not found")

    def get_test_data(self, data: dict):
        """
        TODO: placeholder method for api
        :param data: key=de number, value=list of keyword phrases
        :return:
        """
        pass

    def get_test_data_csv(self):
        #TODO: see toolbox. transform_csv_to_dict -test
        filepath = self.config.admin_config.filepath_input.test_data
        test_data = pd.read_csv(filepath, delimiter=',')
        test_dict = {}
        for row in range(len(test_data)):
            de = test_data['de'][row]
            if not isinstance(test_data['keyword'][row], float) \
                    and not isinstance(test_data['msc'][row], float):
                try:
                    keywords = eval(test_data['keyword'][row])
                except (SyntaxError, NameError):
                    keywords = test_data['keyword'][row]
                try:
                    mscs = eval(test_data['msc'][row])
                except (SyntaxError, NameError):
                    mscs = test_data['msc'][row]
                test_dict.update(
                    {de:
                        {
                            "keywords": keywords,
                            "mscs": mscs
                        }
                    }
                )
            else:
                continue
        return test_dict

    def execute(self, data: dict):
        """
        :param data: key should be the de_number, value is list of keyword
        phrases
        :return: dict with key is de_number, value is list of msc codes
        """
        mscs_predicted = {}

        total = len(list(data.keys()))
        run = 0
        import numpy as np
        milestones = [round(n) for n in np.linspace(0, total, 10)]
        for de, keywords in data.items():
            run += 1
            if run in milestones:
                print(f"done: {round(run/total*100)}% ...")
            predictions = [
                self.map[item]
                for item in keywords
                if item in self.map.keys()
            ]

            convoluted = {}
            for k in set(k for d in predictions for k in d):
                convoluted[k] = sum(
                    [
                        d[k]
                        for d in predictions
                        if k in d
                    ]
                )
            mscs_predicted.update(
                {
                    str(de): convoluted
                }
            )

        return mscs_predicted

    @staticmethod
    def search_string(input_string):
        pass

    def store_prediction(self, filepath):
        pass