from pydantic import BaseModel, FilePath, DirectoryPath, validator
from typing import Optional

data_folder = "/home/marcel/data/240712/"


class FilePaths(BaseModel):
    data_set: FilePath = "data.gz"
    twst: Optional[str] = None

    @validator("data_set", pre=True, always=True)
    def add_dir_path(cls, dd):
        return f"{data_folder}{dd}"

print(FilePaths())