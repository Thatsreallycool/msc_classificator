from pydantic import BaseModel, ValidationError, validator
import os
from zb_msc_classificator import read_ini
from zb_msc_classificator.config.config_datamodel \
    import AdminConfig, DataFolder, FilePathInput, FilePathOutput, \
    TrainingSource


class ConfigGeneral(BaseModel):
    admin_config: AdminConfig = AdminConfig()

    @validator("admin_config", always=True)
    def config_filepath_location(cls, cfg_data):
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

        data_folder = DataFolder(**admin_cfg["DATA FOLDER"])
        fp_input = {
            k: f"{data_folder.load_from}{v}"
            for k, v in admin_cfg["FILEPATH INPUT"].items()
        }
        fp_output = {
            k: f"{data_folder.save_to}{v}"
            for k, v in admin_cfg["FILEPATH OUTPUT"].items()
        }

        return AdminConfig(
            data_folder=data_folder,
            filepath_input=FilePathInput(**fp_input),
            filepath_output=FilePathOutput(**fp_output)
        )


class ConfigGenerate(ConfigGeneral):
    training_source: TrainingSource
    store: bool = False


class ConfigClassify(ConfigGeneral):
    nr_msc_cutoff: int = 10

    @validator("nr_msc_cutoff")
    def msc_cutoff_pos_int(cls, val):
        if val < 1:
            raise ValueError("must be positive")
        return val
