from zb_msc_classificator.file_generator import GenerateFiles
from pydantic import ValidationError, FilePath, validator
from pathlib import Path

g = GenerateFiles()



import os
from pydantic import BaseModel


class User(BaseModel):
    id: FilePath
    name = 'John Doe'

    @validator("id", pre=True)
    def touch_it(cls, filepath):
        if not os.path.isfile(filepath):
            Path(filepath).touch()
        return filepath

try:
    user = User(id="/home/marcel/kw_allow_list.gz")
    print("huh?")
except ValidationError as e:
    print(e.errors())
    print("hhe")

