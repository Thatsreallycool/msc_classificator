from msc_class_original.generate_index import GenerateIndex

create_indexes = 'keyword'
keyword_length = 50

gen = GenerateIndex(
        index_category=create_indexes,
        km=True,
        mk=False,
        store_it=False,
        overwrite=True
    )


