import os.path


class Config:
    def __init__(self):
        # placeholder for later cutoff msc for categorization...
        self.nr_msc_cutoff = 10

        self.data_folder = {
            "load": "../data/",
            "save": "../stored/"
        }
        filepaths = {
            "load": {
                "stopwords": "stopwords.txt",
                "training_data": "out.csv",
                "test_data": "out-mr.csv"
            },
            "save": {
                "pred_text": f"pred_text_{self.nr_msc_cutoff}",
                "pred_keyword": f"pred_keyword_{self.nr_msc_cutoff}",
                "pred_refs": f"pred_refs_{self.nr_msc_cutoff}"
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
        if os.path.exists(self.data_folder[data_folder]):
            return True
        else:
            raise Exception("data folder for storing data doesnt exist!")
