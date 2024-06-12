from zb_msc_classificator.evaluation import Evaluate
from zb_msc_classificator.config.definition import ConfigGeneral

my_config = ConfigGeneral()
my_config.admin_config.filepath_output.prediction_keyword = f"{my_config.admin_config.data_folder.save_to}predictions.json"
eval = Evaluate(
    config=my_config
)