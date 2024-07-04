from zb_msc_classificator.config.definition import ConfigClassify
from zb_msc_classificator.classification import Prediction

from tests.testfiles.example_test_set import example_test_set

classify = Prediction(
    config=ConfigClassify()
)

test_data = {
    de: values["editor"]["keywords"]
    for de, values in example_test_set.items()
}
result = classify.execute(data=test_data)

print(result)
sorted_result = {}
for kr, vr in result.items():
    sorted_result.update(
        {
            kr: {
                k: v for k, v in sorted(
                    vr.items(),
                    key=lambda item: item[1],
                    reverse=True
                )
            }
        }
    )
cutoff_result = {}
for kc, vc in sorted_result.items():
    cutoff_result.update(
        {
            kc: {
                msc: vc[msc]
                for place, msc in enumerate(vc.keys())
                if place<10
            }
        }
    )

print(sorted_result)
print(cutoff_result)

classify.tools.store_data(
    filepath="/home/marcel/data/test_data.json",
    data=example_test_set
)
