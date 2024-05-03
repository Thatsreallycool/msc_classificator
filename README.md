# msc_fine_grained
This package contains a linear mapping between keywords and msc categories, 
based on ... (placeholder text).

Please note that all run example codes treat the source code as a normal 
python package, so you need to install it first in your virtuel environment, 
before running the scripts or consider writing your own scripts (see 
Installation Manual below).

## Package requirements
Please create your virtual environment with package versions compatible with 
the following

see ./requirements.txt

## Changelog
see ./changelog.md

## Installation Manual
for dev purposes (from main folder)
`pip install zb_msc_classificator -r ./requirements.txt -e .`

## Coding Logic
### msc_class_original
#### Config File Editing
- **data_folder**: create 2 local folders and enter their location 
  - "load" for input data(stopwords, training_data, test_data). 
  - "save" for output data(prediction_[...])
- **filepaths**: local file paths for loading and storing data
- **nr_msc_cutoff**: currently placeholder for later

#### check if all configured correctly
- ./run/check_config.py
- first check if all filepaths in config are set for loading 
   - training_data

#### Creating Index Matrix 
- ./run/gen_index.py contains example code to run the generation process
   1. parameters: 
      1. index_category: 'keyword, 'refs' (, 'text', 'title')
      2. km: create index mapper(dict) from entities(keys) to classes(values)
         [optional: default=True]
      3. km: create index mapper(dict) from classes(keys) to entities(values)
         [optional: default=False]
      4. overwrite: overwrite existing index files 
         [optional: default: False]
- output: json in data_folder set in config

# TODO
- run original
  - reproduce predictions from new index 
  - generate index and find differences between zenodo version and mine
- transfer original to modularized version
  - reproduce results from original code
  - modules:
    - generate
    - evaluate
    - predict
    - harmonize
    - get data (Caretaker stuff)
    - config (pydantic?)
- evaluate: precision vs. recall figure
  - figure out how plt is done
    - https://zenodo.org/records/5884600
    - https://zenodo.org/records/10251194
    - https://zenodo.org/records/6448360
  - reproduce figure
  - automatize figure making
- improvement: 
  - edit philipps google document