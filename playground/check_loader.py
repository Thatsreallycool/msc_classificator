from zb_msc_classificator.config.definition import ConfigGeneral
from zb_msc_classificator.tools import Toolbox

file_pickle = "/home/marcel/PycharmProjects/msc_classificator/data/data.pickle"
file_zip = "/home/marcel/PycharmProjects/msc_classificator/data/test.gz"

config = ConfigGeneral()

tools = Toolbox()

data = tools.pickle_loader(
    filepath=file_pickle
)

print("")
