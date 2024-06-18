from pydantic import BaseModel, ValidationError, validator
import os
from zb_msc_classificator import read_ini
from zb_msc_classificator.config.config_datamodel \
    import AdminConfig, DataFolder, FilePathInput, FilePathOutput, \
    TrainingSource, Elastic


class ConfigGeneral(BaseModel):
    admin_config: AdminConfig = AdminConfig()

    @validator("admin_config", always=True)
    def confirm_consistency(cls, cfg_data):
        filepath_options = [
            f"{cfg_data.zbmath_path}{cfg_data.config_filename}",
            f"../../{cfg_data.config_filename}",
            f"../{cfg_data.config_filename}",
            cfg_data.config_filename
        ]
        viable_paths = [
            True if os.path.isfile(item)
            else False
            for item in filepath_options
        ]
        if any(viable_paths):
            config_filepath = filepath_options[viable_paths.index(True)]
        else:
            raise FileNotFoundError("config.ini not found!")
        admin_cfg = read_ini(file_path=config_filepath)

        if any(admin_cfg):
            data_folder = DataFolder(**admin_cfg["DATA FOLDER"])
            if not all(
                [
                    os.path.isdir(data_folder.dict()[item])
                    for item in data_folder.__fields__.keys()
                ]
            ):
                raise FileNotFoundError("data folder not created!"
                                        "")
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

        return AdminConfig(
            data_folder=data_folder,
            filepath_input=fp_input,
            filepath_output=fp_output,
            elastic=Elastic(**admin_cfg["ELASTIC"])
        )


class ConfigGenerate(ConfigGeneral):
    training_source: TrainingSource = None
    store_data_elastic: bool = False
    data_size: int = None
    store_map: bool = False

    @validator("data_size", always=True)
    def int_gt0(cls, number):
        minimum_jump = 10000
        if number is None:
            return minimum_jump
        elif number <= 0:
            return minimum_jump
        elif number > 0:
            return number
        else:
            raise ValueError(
                "data size addendum for datablob must be bigger than zero"
            )


class ConfigClassify(ConfigGeneral):
    nr_msc_cutoff: int = 10

    @validator("nr_msc_cutoff")
    def msc_cutoff_pos_int(cls, val):
        if val < 1:
            raise ValueError("must be positive")
        return val


class ConfigEvaluate(ConfigGeneral):
    pass