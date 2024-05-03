from msc_class_original.classification import Classification

index_file = "../stored/keyword_msc_idx.json"

classify = Classification(
    index_filepath=index_file
)
print(classify.execute(pred_basis='text'))
print(classify.execute(pred_basis='keyword'))
print(classify.execute(pred_basis='refs'))
