from zb_msc_classificator.tools import Toolbox


class Evaluate:
    def __init__(self, config):
        self.config = config
        self.tools = Toolbox()
        self.prediction = self.get_prediction(mode="keyword")
        self.test_data = self.get_test_data()
        self.execute(mode="keyword")

    def count_perfect_match(self):
        pass

    def count_correct_msc_different_order(self):
        pass

    def count_nr_msc_missing(self):
        pass

    def count_nr_msc_wrong(self):
        pass

    def count_everything_wrong(self):
        pass

    def get_test_data(self):
        return self.tools.transform_csv_to_dict(
            filename=self.config.admin_config.filepath_input.test_data,
            delimiter=",",
            idx_name="de",
            column_names=['keyword', 'msc']
        )

    def get_prediction(self, mode: str):
        if mode == "keyword":
            return self.tools.load_json(
                filename=self.
                    config.admin_config.filepath_output.prediction_keyword
            )
        else:
            pass
        pass

    def execute(self, mode: str):
        pass
