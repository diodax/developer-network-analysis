# -*- coding: utf-8 -*-
import click
import logging
import json
import networkx as nx
from dotenv import find_dotenv, load_dotenv
import matplotlib.pyplot as plt


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """
    Receives the location of the NetworkX graph as a command-line Path argument.
    With it, it generates a image graph of the network on the output filepath.
    """
    logger = logging.getLogger(__name__)
    logger.info('Importing NetworkX graph from ' + str(input_filepath))

    with open(input_filepath, 'r') as json_data:
        data = json.load(json_data)
        graph = nx.node_link_graph(data)

    nx.draw(graph)  # networkx draw()
    plt.draw()

    # the plot gets saved to 'reports/figures/developer-network-graph.png'
    plt.savefig(output_filepath)
    logger.info('Created plot graph at ' + output_filepath)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    load_dotenv(find_dotenv())

    main()
