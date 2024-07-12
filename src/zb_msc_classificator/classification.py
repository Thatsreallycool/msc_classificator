from zb_msc_classificator.tools import Toolbox
from zb_msc_classificator.harmonize import Harmonizer
from zb_msc_classificator.config.definition \
    import ConfigHarmonize, ConfigClassify
import numpy as np


class Prediction:
    def __init__(self, config: ConfigClassify = ConfigClassify()):
        self.config = config
        self.tools = Toolbox()
        self.harmonizer = Harmonizer(
            config=ConfigHarmonize(use_stopwords=False)
        )
        self.map = self.get_map()

    def execute(self, data: dict):
        """
        :param data: key should be the de_number, value is list of keyword
        phrases
        :return: dict with key is de_number, value is list of msc codes
        """
        mscs_predicted = {}

        total = len(list(data.keys()))
        run = 0

        milestones = [round(n) for n in np.linspace(0, total, 10)]
        for de, keywords in data.items():
            if len(keywords) == 0:
                continue
            run += 1
            if run in milestones:
                print(f"done: {round(run/total*100)}% ...")

            predictions = [
                self.map[item]
                for item in keywords
                if item in self.map.keys()
            ]

            convoluted = {}
            for msc_code in set(
                    msc_code
                    for msc_dict in predictions
                    for msc_code in msc_dict
            ):
                convoluted[msc_code] = sum(
                    [
                        msc_dict[msc_code]
                        for msc_dict in predictions
                        if msc_code in msc_dict
                    ]
                )
            mscs_predicted.update({str(de): convoluted})

        return mscs_predicted

    def get_map(self):
        return self.tools.load_data(
            filepath=self.config.admin_config.file_paths.map
        )

    def get_data_to_classify(self, data):
        pass