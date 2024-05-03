# msc_fine_grained
This package contains a linear mapping between keywords and msc categories, 
based on ...

## Package requirements
Please create your virtual environment with package versions compatible with 
the following
* nltk ~= 3.5
* scipy ~= 1.6.0
* numpy ~= 1.19.5
* (pandas ~= 1.1.5)

## Changelog
see ./changelog.md

## Installation Manual
for dev purposes (from main folder)
`pip install zb_msc_classificator -r ./requirements.txt -e .`

## Config File Editing
- **filepaths**: local file paths for loading and storing data
- **nr_msc_cutoff**: currently placeholder for later

## Coding Logic
### msc_class_original
#### Creating Index Matrix
1. first check if all filepaths in config are set for loading 
   1. training_data
2. ./run/gen_index.py contains example code to run the generation process
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