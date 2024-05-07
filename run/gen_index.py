from msc_class_original.generate_index import GenerateIndex

create_indexes = ['keyword', 'text', 'refs']


gen = [
    GenerateIndex(
        index_category=item,
        km=True,
        mk=True,
        overwrite=True
    )
    for item in create_indexes
]
