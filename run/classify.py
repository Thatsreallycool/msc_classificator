from msc_class_original.config import Config
from msc_class_original.classification import Classification, Evaluate

index_file = "../stored/keyword_msc_idx.json"
#index_file = "../stored/msc_keyword_idx.json"

classify = Classification(
    index_filepath=index_file
)
print(classify.execute(pred_basis='text'))
