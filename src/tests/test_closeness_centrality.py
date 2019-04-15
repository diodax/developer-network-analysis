import pytest
import networkx as nx
from ..network.analyze_network import closeness_centrality


def test_closeness_centrality():
    # Create a random network, and compare the dict results with the ones in the library implementation
    graph = nx.erdos_renyi_graph(5, 0.5, seed=1, directed=False)
    centrality_nx = nx.closeness_centrality(graph)
    centrality_local = closeness_centrality(graph)
    assert centrality_nx == centrality_local
