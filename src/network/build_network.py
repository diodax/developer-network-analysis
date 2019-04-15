# -*- coding: utf-8 -*-
import click
import logging
import json
import networkx as nx
from dotenv import find_dotenv, load_dotenv
from networkx.readwrite import json_graph


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """
    Receives the location of the list of edges as a command-line Path argument.
    With it, it builds the graph network and generates a .json export for analysis.
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

    # Save graph to json object
    logger.info('Saving results on ' + output_filepath)
    with open(output_filepath, 'w') as writer:
        graph_serialized = json_graph.node_link_data(graph)
        writer.write(json.dumps(graph_serialized))


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    load_dotenv(find_dotenv())

    main()
