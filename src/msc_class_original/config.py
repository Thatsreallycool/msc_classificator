import os.path


class Config:
    def __init__(self):
        """
        set file locations, classification settings, etc.
        """
        # placeholder for later cutoff msc for categorization...
        # TODO: if more parameters for classification needed, refactor this
        #  into dict or object -> pydantic model for config?(!)
        self.nr_msc_cutoff = 10

        self.data_folder = {
            "load": "../data/",
            "save": "../stored/"
        }
        filepaths = {
            "load": {
                "stopwords": "stopwords.txt",
                "training_data": "out.csv",
                "test_data": "out-mr.csv",
                "mrmscs": "mrmscs_dict.json"

            },
            "save": {
                "pred_text": f"pred_text_{self.nr_msc_cutoff}.csv",
                "pred_keyword": f"pred_keyword_{self.nr_msc_cutoff}.csv",
                "pred_refs": f"pred_refs_{self.nr_msc_cutoff}.csv"
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
                self.check_folder_existing(data_folder="save")
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
