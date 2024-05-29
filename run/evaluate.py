from msc_class_original.classification import Evaluate
from msc_class_original.config import Config

user_config = Config(
    config_file_path="/home/marcel/PycharmProjects/"
                     "msc_classificator/config"
                     ".ini"
)
#index_file = f"{user_config.data_folder['save']}keyword_msc_idx.json"
index_file = f"{user_config.data_folder['save']}ent_cls_idx.json"

eval1 = Evaluate(
    index_filepath=index_file,
    user_config=user_config
)

eval1.get_precision_recall2()
