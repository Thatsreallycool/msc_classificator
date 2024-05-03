from msc_class_original.classification import Evaluate

index_file = "../stored/keyword_msc_idx.json"

eval = Evaluate(
    index_filepath=index_file
)

eval.get_precision_recall_curves()
