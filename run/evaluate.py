from msc_class_original.classification import Evaluate
from msc_class_original.config import Config

user_config = Config()
index_file = f"{user_config.data_folder['save']}keyword_msc_idx.json"

eval = Evaluate(
    index_filepath=index_file
)

eval.get_precision_recall()
