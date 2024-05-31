from msc_class_original.generate_index import GenerateIndex
from msc_class_original.classification import Classification, Evaluate
from msc_class_original.config import Config

user_config = Config(
    config_file_path="/home/marcel/PycharmProjects/"
                     "msc_classificator/config.ini"
)

create_index = 'keyword'
keyword_length = 50
kl = [7, 6, 5, 4, 3, 2]


gen = GenerateIndex(
        index_category=create_index,
        km=True,
        mk=False,
        store_it=False,
        overwrite=True
    )
print(f"total nr of entities found: {len(gen.index_generated.keys())}")

results = {}

for i, l in enumerate(kl):
    cut_index = gen.index_cutoff_keywords(max_keywords=l)
    print(f"total nr of entities used: {len(cut_index.keys())}")

    classified = Classification(
        user_config=user_config,
        index=cut_index
    ).execute(
        pred_basis=create_index,
        store_to_file=False
    )

    pr = Evaluate(
        index=cut_index,
        user_config=user_config
    ).get_precision_recall2(kw=classified)
    pr.update({"entities": len(cut_index.keys())})
    results.update({l: pr})

    print(f"done {round((i+1)/len(kl)*100, 2)}%")

print(results)