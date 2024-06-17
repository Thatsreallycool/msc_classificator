# msc_fine_grained
This package contains a linear mapping between keywords and msc categories, 
based on ... (placeholder text)....

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
### zb_msc_classificator
#### Admin Config File Editing
- **general**: 
  - __map_source__: keyword switch:
    - elastic: will access elastic search index with credentials (see 
      "elastic" section)
    - local: will load map from local file (see training_data)
- **data_folder**: create 2 local folders and enter their location 
  - __"load_from"__ for input data(stopwords, training_data, test_data). 
  - __"save_from"__ for output data(prediction_[...])
- **filepath input**: local file paths for loading and storing data
  - __stopwords__: text file separated by line breank
  - __training_data__: csv file, delimiter "," with columns: "de", "msc", 
    "text", "keyword", "refs"
  - __test_data__: csv file, delimiter "," with columns: "de", "msc", 
    "text", "keyword", "refs"
  - __mrmscs__: json file, important for evaluation
- **filepath output**:
  - __pred_text__: ... 
  - __pred_keyword__: ...
  - __pred_refs__: ...


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