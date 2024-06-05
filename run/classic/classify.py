from msc_class_original.classification import Classification

from msc_class_original.config import Config

user_config = Config(
    config_file_path="/config.ini"
)

#index_file = f"{user_config.data_folder['save']}keyword_msc_idx.json"
index_file = f"{user_config.data_folder['save']}ent_cls_idx.json"

classify = Classification(
    index_filepath=index_file,
    user_config=user_config
)
print(classify.execute(pred_basis='keyword'))
print(classify.execute(pred_basis='text'))

index_file_r = f"{user_config.data_folder['save']}ref_cls_idx.json"
classify_r = Classification(
    index_filepath=index_file_r,
    user_config=user_config
)
print(classify_r.execute(pred_basis='refs'))
