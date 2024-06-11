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

    def execute(self):
        mscs_predicted = {}

        total = len(list(self.test_data_dict.keys()))
        run = 0
        import numpy as np
        milestones = [round(n) for n in np.linspace(0, total, 10)]
        for de, actual in self.test_data_dict.items():
            run += 1
            if run in milestones:
                print(f"done: {round(run/total*100)}% ...")
            predictions = [
                self.map[item]
                for item in actual["keywords"]
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