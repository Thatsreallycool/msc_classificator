from zb_msc_classificator.classification import Prediction
from zb_msc_classificator.config.definition import ConfigClassify

my_config = ConfigClassify()
prediction = Prediction(
    config=my_config
)
print("configuration loaded! starting...")


from zb_msc_classificator.tools import Toolbox
tools = Toolbox()

store_filename = f"{my_config.admin_config.data_folder.save_to}predictions.json"
tools.store_json(
    filename=store_filename,
    dict2store=prediction.execute()
)