from zb_msc_classificator.classification import Prediction
from zb_msc_classificator.config.definition import ConfigClassify

prediction = Prediction(
    config=ConfigClassify()
)

prediction.map = {
    "keyword1": {
        "code1": 1,
        "code2": 2,
        "code3": 3
    },
    "keyword2": {
        "code1": 2,
        "code3": 10
    },
    "keyword3": {
        "code1": 10,
        "code2": 3
    },
    "keyword4": {
        "code4": 4
    }
}
prediction.test_data_dict = {
    1: {
        "keywords": ["keyword1", "keyword2"],
        "mscs": ["code1", "code2"]
    },
    2: {
        "keywords": ["keyword1", "keyword3"],
        "mscs": ["code3 ", "code2"]
    },
    3: {
        "keywords": ["keyword3", "keyword2"],
        "mscs": ["code3", "code1"]
    },
    4: {
        "keywords": ["keyword4", "keyword1"],
        "mscs": ["code1"]
    }
}

expected_result = {
    1: {'code1': 3, 'code2': 2, 'code3': 13},
    2: {'code1': 11, 'code2': 5, 'code3': 3},
    3: {'code1': 12, 'code2': 3, 'code3': 10},
    4: {'code1': 1, 'code2': 2, 'code3': 3, 'code4': 4}
}

print(
    prediction.execute()
)