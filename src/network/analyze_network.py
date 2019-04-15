# -*- coding: utf-8 -*-
import click
import logging
import json
import networkx as nx
import pandas as pd
from dotenv import find_dotenv, load_dotenv


def single_source_shortest_path(graph, node):
    """
    Finds the shortest paths from a single source to the rest of the nodes in the graph.
    """
    nodes = []
    paths = {}
    for v in graph:
        paths[v] = []
    sigma = dict.fromkeys(graph, 0.0)
    distances_dict = dict()
    sigma[node] = 1.0
    distances_dict[node] = 0
    remaining_nodes = [node]
    while remaining_nodes:   # use BFS to find shortest paths
        v = remaining_nodes.pop(0)
        nodes.append(v)
        distance_v = distances_dict[v]
        sigma_v = sigma[v]
        for edge in graph[v]:
            if edge not in distances_dict:
                remaining_nodes.append(edge)
                distances_dict[edge] = distance_v + 1
            if distances_dict[edge] == distance_v + 1:   # this is a shortest path, count paths
                sigma[edge] += sigma_v
                paths[edge].append(v)  # predecessors
    return nodes, paths, sigma


def accumulate(betweenness, nodes_list, paths, sigma, current_node):
    delta = dict.fromkeys(nodes_list, 0)
    while nodes_list:
        node = nodes_list.pop()
        coefficient = (1.0 + delta[node]) / sigma[node]
        for v in paths[node]:
            delta[v] += sigma[v] * coefficient
        if node != current_node:
            betweenness[node] += delta[node]
    return betweenness


def rescale(betweenness, number_nodes):
    if number_nodes <= 2:
        # No normalization b=0 for all nodes
        scale = None
    else:
        scale = 1.0 / ((number_nodes - 1) * (number_nodes - 2))
    if scale is not None:
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
    betweenness = dict.fromkeys(graph, 0.0)
    nodes = graph
    nodes_set = set(graph.nodes)
    for s in nodes:
        # single source shortest paths with BFS
        nodes_list, paths, sigma = single_source_shortest_path(graph, s)
        # accumulation
        betweenness = accumulate(betweenness, nodes_list, paths, sigma, s)
    # rescaling
    betweenness = rescale(betweenness, len(graph))
    return betweenness


def closeness_centrality(graph, u=None):
    """
    Recursive method that returns a dictionary with the closeness centrality of all the nodes in a given graph network.
    The closeness centrality is the mean length of all shortest paths from a node to all other nodes in the
    network (i.e. how many hops on average it takes to reach every other node)
    """
    path_length = nx.single_source_shortest_path_length
    nodes = graph.nodes()
    closeness_centrality_dict = dict()
    for n in nodes:
        shortest_path = path_length(graph, n)
        totsp = sum(shortest_path.values())
        if totsp > 0.0 and len(graph) > 1:
            closeness_centrality_dict[n] = (len(shortest_path) - 1.0) / totsp
            # Normalize to (number of nodes - 1)
            s = (len(shortest_path) - 1.0) / (len(graph) - 1)
            closeness_centrality_dict[n] *= s
        else:
            closeness_centrality_dict[n] = 0.0
    if u is not None:
        return closeness_centrality_dict[u]
    else:
        return closeness_centrality_dict


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """
    Receives the location of the NetworkX graph as a command-line Path argument.
    With it, it generates a .csv report on the output filepath.
    """
    logger = logging.getLogger(__name__)
    logger.info('Importing NetworkX graph from ' + str(input_filepath))

    with open(input_filepath, 'r') as json_data:
        data = json.load(json_data)
        graph = nx.node_link_graph(data)

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

    # Creates output DataFrame with the format required for the report
    columns = ['email', 'degree centrality', 'betweenness centrality', 'closeness centrality']
    df_output = pd.DataFrame(data, columns=columns)
    # Save the processed subset on data reports/developer-network-output.csv
    logger.info('Saved processed results on ' + output_filepath + ' with ' + str(len(df_output)) + ' rows')
    df_output.to_csv(output_filepath, encoding='utf-8', index=False)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    load_dotenv(find_dotenv())

    main()
