from zb_msc_classificator.config.definition import ConfigGeneral

config = ConfigGeneral()

"""
  if any(admin_cfg):
            data_folder = DataFolder(**admin_cfg["DATA FOLDER"])
            if not all(
                [
                    os.path.isdir(data_folder.dict()[item])
                    for item in data_folder.__fields__.keys()
                ]
            ):
                raise FileNotFoundError("data folder not created!")
            fp_input = FilePathInput(
                **{
                    k: f"{data_folder.load_from}{v}"
                    for k, v in admin_cfg["FILEPATH INPUT"].items()
                }
            )
            if not all(
                [
                    os.path.isfile(fp_input.dict()[item])
                    for item in fp_input.__fields__.keys()
                ]
            ):
                raise FileNotFoundError("input files not found!")

            fp_output = FilePathOutput(
                **{
                    k: f"{data_folder.save_to}{v}"
                    for k, v in admin_cfg["FILEPATH OUTPUT"].items()
                }
            )
                    else:
            raise FileNotFoundError("config.ini not correct!")


self.load_from_disk(
                    filepath=self.config.admin_config.filepaths.csv_training_data,
                    columns=['msc', 'keyword'],
                    delimiter=','
                )

"""