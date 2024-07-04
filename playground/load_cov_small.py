filepath_k = "/home/marcel/PycharmProjects/msc_classificator/data" \
           "/keyword_occurence.gz"

filepath_m = "/home/marcel/PycharmProjects/msc_classificator/data" \
             "/msc_occurence.gz"

filepath_km = "/home/marcel/PycharmProjects/msc_classificator/data" \
              "/kw_m_cooccurence.gz"

from zb_msc_classificator.tools import Toolbox

tools = Toolbox()

keyword_cooc = tools.load_data(filepath=filepath_km)

from tests.testfiles.example_test_set import example_test_set

for one_set in list(example_test_set.values()):
    try:
        print(
            sum(
                [
                    len(keyword_cooc[item].keys())
                    for item in one_set['keywords']
                ]
            )
        )
    except KeyError:
        print("nothing!")
