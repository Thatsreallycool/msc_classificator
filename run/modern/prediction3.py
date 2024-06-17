from zb_msc_classificator.classification import Prediction
from zb_msc_classificator.config.definition \
    import ConfigClassify, AdminConfig, FilePathOutput

my_config = ConfigClassify()
prediction = Prediction(
    config=my_config
)
print("configuration loaded! starting...")

data = {
    1: ["keyword1", "keyword2", "keywords3"],
    2: ["keyword1", "keyword2", "keywords3"]
}

print(prediction.execute(data=data))