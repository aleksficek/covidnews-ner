# CovidNews-NER

Welcome to the CovidNews-NER dataset. It is an English COVID-19 Named Entity Recognition dataset in the pandemic news domain, addressing current NER models’ lack of ability to tackle new and out-of-domain topics. 

**Structure**

There are 5 folders included in `dataset/`, dataset is in CONLL format. Files ending with `_text.txt` are the text for each entry, files ending with `_true.txt` are the strong labels for each entry and files ending with `_dist.txt` are the weak labels for each entry.

- `train/`: 2100 entries of strong and weak training data
- `valid/`: 600 entries of strong validation data
- `test/`: 300 entries of strong test data
- `rest/`: 10000 entries of additional weak data
- `other/`: contains all strong and weak data seperated by original language translated from and combined

**Entity Categories**

The dataset covers 10 entity categories listed below. For detailed information about the dataset please see the corresponding paper.

- person
- location
- organization
- time
- disease
- virus
- product
- animal
- symptom
- bacterium