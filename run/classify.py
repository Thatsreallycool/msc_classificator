from msc_class_original.classification import Classification

from msc_class_original.config import Config

user_config = Config(
    config_file_path="/home/marcel/data/PycharmProjects/"
                     "msc_classificator/config.ini"
)

index_file = f"{user_config.data_folder['save']}keyword_msc_idx.json"

classify = Classification(
    index_filepath=index_file
)
print(classify.execute(pred_basis='text'))
print(classify.execute(pred_basis='keyword'))
print(classify.execute(pred_basis='refs'))
