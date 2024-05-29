# msc_fine_grained
This package contains a linear mapping between keywords and msc categories, 
based on ... (placeholder text).

Please note that all run example codes treat the source code as a normal 
python package, so you need to install it first in your virtual environment, 
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
  - __"load"__ for input data(stopwords, training_data, test_data). 
  - __"save"__ for output data(prediction_[...])
- **filepaths**: local file paths for loading and storing data
  - __load__ (external files not created by code): 
    - stopwords: text file separated by line breank
    - training_data: csv file, delimiter "," with columns: "de", "msc", 
      "text", "keyword", "refs"
    - test_data: csv file, delimiter "," with columns: "de", "msc", 
      "text", "keyword", "refs"
    - mrmscs: json file, important for evaluation
  - __save__ (files created by code):
    - pred_text: csv file predicted msc categories based on abstract text 
      entities
    - pred_keyword: csv file predicted msc categories based on keyword entities
    - pred_refs: csv file predicted msc categories based on reference msc entities
      categories
- **nr_msc_cutoff**: nr of entities considered for classification

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
- check how text2msc works (2-3 n gram?)
- transfer original to modularized version
  - reproduce results from original code
  - modules:
    - generate
      - load from file / from esi
      - clean data with harmonizer
      - generate map(keywords, text, mscs, combination, ... -> mscs)
        - output: dict or sparse matrix
    - evaluate
      - load
        - actual
        - human base line
        - prediction basis map results
          - keyword
          - text
          - msc
          - all combined
          - ...
      - metrics
        - precision recall
        - order of prediction correct?
      - store results
    - predict
      - get map(s) from
        - file
        - esi binary
      - get data to map from
        - file
        - ...
      - execute mapping
      - store data to
        - file
        - ...?
    - harmonize
      - remove special characters
      - canonicalize
      - turn strings into lists(?)
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