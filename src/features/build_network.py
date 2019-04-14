# -*- coding: utf-8 -*-
import click
import logging
import json
import networkx as nx
import pandas as pd
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt


def single_source_shortest_path(G, s):
    S = []
    P = {}
    for v in G:
        P[v] = []
    sigma = dict.fromkeys(G, 0.0)    # sigma[v]=0 for v in G
    D = {}
    sigma[s] = 1.0
    D[s] = 0
    Q = [s]
    while Q:   # use BFS to find shortest paths
        v = Q.pop(0)
        S.append(v)
        Dv = D[v]
        sigmav = sigma[v]
        for w in G[v]:
            if w not in D:
                Q.append(w)
                D[w] = Dv + 1
            if D[w] == Dv + 1:   # this is a shortest path, count paths
                sigma[w] += sigmav
                P[w].append(v)  # predecessors
    return S, P, sigma


def accumulate(betweenness, S, P, sigma, s):
    delta = dict.fromkeys(S, 0)
    while S:
        w = S.pop()
        coeff = (1.0 + delta[w]) / sigma[w]
        for v in P[w]:
            delta[v] += sigma[v] * coeff
        if w != s:
            betweenness[w] += delta[w]
    return betweenness


def rescale(betweenness, n, normalized, directed=False, k=None):
    if normalized is True:
        if n <= 2:
            scale = None  # no normalization b=0 for all nodes
        else:
            scale = 1.0 / ((n - 1) * (n - 2))
    else:  # rescale by 2 for undirected graphs
        if not directed:
            scale = 1.0 / 2.0
        else:
            scale = None
    if scale is not None:
        if k is not None:
            scale = scale * n / k
        for v in betweenness:
            betweenness[v] *= scale
    return betweenness


def degree_centrality(graph):
    """
    Returns a dictionary with the degree centrality of all the nodes in a given graph network.
    A node’s degree centrality is the number of links that lead into or out of the node.
    """
    nodes = set(graph.nodes)
    s = 1.0 / (len(nodes) - 1.0)
    centrality = dict((n, d * s) for n, d in graph.degree(nodes))
    return centrality


def betweenness_centrality(graph):
    """
    Returns a dictionary with the betweenness centrality of all the nodes in a given graph network.
    The number of shortest paths that pass through a node divided by all shortest paths in the network.
    """
    betweenness = dict.fromkeys(graph, 0.0)  # b[v]=0 for v in G
    nodes = graph
    for s in nodes:

        # single source shortest paths
        # use BFS
        S, P, sigma = single_source_shortest_path(graph, s)

        # accumulation
        betweenness = accumulate(betweenness, S, P, sigma, s)

    # rescaling
    betweenness = rescale(betweenness, len(graph), normalized=True, directed=False, k=None)
    return betweenness


def closeness_centrality(graph, u=None):
    """
    Returns a dictionary with the closeness centrality of all the nodes in a given graph network.
    The closeness centrality is the mean length of all shortest paths from a node to all other
    nodes in the network (i.e. how many hops on average it takes to reach every other node)
    """
    path_length = nx.single_source_shortest_path_length
    nodes = graph.nodes()
    closeness_centrality = {}
    for n in nodes:
        sp = path_length(graph, n)
        totsp = sum(sp.values())
        if totsp > 0.0 and len(graph) > 1:
            closeness_centrality[n] = (len(sp) - 1.0) / totsp

            # normalize to number of nodes-1 in connected part
            s = (len(sp) - 1.0) / (len(graph) - 1)
            closeness_centrality[n] *= s
        else:
            closeness_centrality[n] = 0.0
    if u is not None:
        return closeness_centrality[u]
    else:
        return closeness_centrality


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('Importing list of edges from ' + str(input_filepath))
    edges = []
    with open(input_filepath, 'r') as reader:
        for line in reader.readlines():
            edge = tuple(line.split(':'))
            edges.append(edge)

    logger.info('Generating NetworkX graph...')
    graph = nx.Graph()

    for edge in edges:
        graph.add_edge(edge[0].replace('\n', ''), edge[1].replace('\n', ''))

    nx.draw(graph)  # networkx draw()
    plt.draw()

    # Save to json object
    logger.info('Saving results on ' + 'models/developer-network.json')
    with open('models/developer-network.json', 'w') as writer:
        graph_serialized = json_graph.node_link_data(graph)
        writer.write(json.dumps(graph_serialized))

    # plt.show()

    # Calculating the degree/betweenness/closeness centrality of each node
    dg_centrality_man = degree_centrality(graph)
    bt_centrality_man = betweenness_centrality(graph)
    cl_centrality_man = closeness_centrality(graph)

    dict_nodes = dict.fromkeys(graph.nodes)
    data = list()
    for key, value in dict_nodes.items():
        dg = dg_centrality_man[key]
        bt = bt_centrality_man[key]
        cl = cl_centrality_man[key]
        row = {'email': key, 'degree centrality': dg, 'betweenness centrality': bt, 'closeness centrality': cl}
        data.append(row)

    # Creates output DataFrame
    columns = ['email', 'degree centrality', 'betweenness centrality', 'closeness centrality']
    df_output = pd.DataFrame(data, columns=columns)
    # Save the processed subset on data reports/developer-network-output.csv

    logger.info('Saved processed results on ' + output_filepath + ' with ' + str(len(df_output)) + ' rows')
    df_output.to_csv(output_filepath, encoding='utf-8', index=False)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
