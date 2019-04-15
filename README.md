Developer Network Analysis
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

After cloning the repository, we run the `make_dataset.py` script from the `/src/data` folder to
generate the text file with the list of edges at `/data/processed/edges-list.txt`.

```bash
python src/data/make_dataset.py data/external/che data/processed/edges-list.txt
```

## Step 2: Constructing the Network

This step uses the edge list file from the previous step to generate a NetworkX graph object.
To do so, we run the `build_network.py` script from the `/src/network` folder.

In this command, the first argument corresponds to the edge list file `data/processed/edges-list.txt` 
and the second argument specifies the output path for the JSON file with the NetworkX graph.

```bash
python src/network/build_network.py data/processed/edges-list.txt models/developer-network.json
```

Using the previous command, the resulting file will be saved on the `/models` folder as `developer-network.json`.

## Step 3: Analyzing the Network

With the data represented on a NetworkX graph by the previous step, we run the `analyze_network.py` script on
`/src/network` to compute the following measures. 
- Degree Centrality
- Betweenness Centrality
- Closeness Centrality

To generate the report file with the nodes and measures, execute:

```bash
python src/network/analyze_network.py models/developer-network.json reports/developer-network-output.csv
```

The `developer-network-output.csv` file will be created on the output path (in this case, `/reports`).

## Step 4: Graph Visualization

Based on the graph of `/models/developer-network.json`, running the `visualize_network.py` script 
on the `/src/visualization` folder will generate a figure of the NetworkX graph, while the
second argument specifies the output path for the graph image. 

```bash
python src/visualization/visualize_network.py models/developer-network.json reports/figures/developer-network-graph.png
```

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Location of the third party Eclipse CHE repository.
    │   └── processed      <- The final, canonical data sets for modeling. Location of the edges list text.
    │
    ├── models             <- Location of the generated NetworkX graph model
    │
    ├── reports            <- Generated output files produced for the graph's measures
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
        ├── network        <- Scripts to build and analyze the graph network
        │   ├── build_network.py
        │   └── analyze_network.py
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations
            └── visualize_network.py
