from msc_class_original.classification import Evaluate
from msc_class_original.config import Config

user_config = Config(
    config_file_path="/home/marcel/data/PycharmProjects/"
                     "msc_classificator/config.ini"
)
index_file = f"{user_config.data_folder['save']}keyword_msc_idx.json"

eval1 = Evaluate(
    index_filepath=index_file
)

eval1.get_precision_recall()
