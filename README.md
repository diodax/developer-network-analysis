developer-network-analysis
==============================

Implementation of a social network analysis of influential developers in a developer network

## Setting up locally

Make sure you have [Python](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installing/) installed.

```bash
git clone https://github.com/diodax/developer-network-analysis.git
cd developer-network-analysis
pip install -r requirements.txt
```

## Step 1: The Dataset

We will work with the [Eclipse CHE](https://github.com/eclipse/che) (Java) Github project as the basis for 
constructing the network. This project will be cloned locally inside the `/data/external/` folder:

```bash
cd data/external
git clone https://github.com/eclipse/che.git
```

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Location of the third party Eclipse CHE repository.
    │   └── processed      <- The final, canonical data sets for modeling.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download or generate data
        │   └── make_dataset.py
        │
        ├── features       <- Scripts to turn raw data into features for modeling
        │   └── build_features.py
        │
        ├── models         <- Scripts to train models and then use trained models to make
        │   │                 predictions
        │   └── analyze_network.py
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations
            └── visualize_network.py
