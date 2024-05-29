import os.path
from zb_msc_classificator import read_ini


class Config:
    def __init__(self, config_file_path):
        """
        set file locations, classification settings, etc.
        """
        # placeholder for later cutoff msc for categorization...
        # TODO: if more parameters for classification needed, refactor this
        #  into dict or object -> pydantic model for config?(!)
        self.nr_msc_cutoff = 10

        try:
            config_read = read_ini(config_file_path)
            self.check_config_data = True
        except FileNotFoundError:
            self.check_config_data = False
            raise Exception("config.ini not found!")

        self.data_folder = {
            "load": config_read["DATA FOLDER"]["load"],
            "save": config_read["DATA FOLDER"]["save"]
        }
        filepaths = {
            "load": {
                "stopwords": config_read["FILEPATH-LOAD"]["stopwords"],
                "training_data": config_read["FILEPATH-LOAD"]["training_data"],
                "test_data": config_read["FILEPATH-LOAD"]["test_data"],
                "mrmscs": config_read["FILEPATH-LOAD"]["mrmscs"],

            },
            "save": {
                "pred_text": config_read["FILEPATH-SAVE"]["pred_text"],
                "pred_keyword": config_read["FILEPATH-SAVE"]["pred_keyword"],
                "pred_refs": config_read["FILEPATH-SAVE"]["pred_refs"],
            }
        }
        self.filepaths = {
            ls: {
                name: f"{self.data_folder[ls]}{file}"
                for name, file in files.items()
            }
            for ls, files in filepaths.items()
        }

        # check for known problems
        if all(
            [
                self.check_files_to_load(data_folder="load"),
                self.check_folder_existing(data_folder="save"),
                self.check_config_data
            ]
        ):
            print("Looks like all is configured. Let's start!")

    def check_files_to_load(self, data_folder):
        """
        check if files exists
        :param data_folder: data folder where file should be located
        :return: bool
        """
        files_exist = {
            name: os.path.isfile(file)
            for name, file in self.filepaths[data_folder].items()
        }
        if all(
           list(files_exist.values())
        ):
            return True
        else:
            not_existing_files = ", ".join(
                [
                    name
                    for name, tf in files_exist.items()
                    if not tf
                ]
            )
            raise Exception(f"Please check if all files to load exist:"
                            f" {not_existing_files}")

    def check_folder_existing(self, data_folder):
        """
        check if data folder exists
        TODO: if data folder for saving doesnt exist, mkdir

        :param data_folder: location of data folder on disk (either relative
        or absolute
        :return: bool
        """
        if os.path.exists(self.data_folder[data_folder]):
            return True
        else:
            raise Exception("data folder for storing data doesnt exist!")
