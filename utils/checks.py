from typing import Any
import networkx as nx

def is_complete_graph(G: nx.Graph) -> bool:
    """Check if graph G is a complete graph (clique) using NetworkX density."""
    if len(G.nodes()) <= 1:
        return True
    # Complete graph has density 1.0 (maximum possible edges)
    return nx.density(G) == 1.0

def is_cycle(G: nx.Graph) -> bool:
    """Check if graph G is a simple cycle using NetworkX functions."""
    if G.number_of_nodes() < 3:
        return False
    # A cycle: connected, all vertices degree 2, and edges == nodes
    return (nx.is_connected(G) and 
            all(G.degree(n) == 2 for n in G.nodes()) and 
            G.number_of_edges() == G.number_of_nodes())


def is_path(G: nx.Graph) -> bool:
    """Check if graph G is a simple path using NetworkX functions."""
    if G.number_of_nodes() <= 1:
        return True  # Single vertex or empty graph is trivially a path
    
    # A path is a tree with exactly 2 vertices of degree 1 (leaves/endpoints)
    return (nx.is_tree(G) and 
            sum(1 for n in G.nodes() if G.degree(n) == 1) == 2)

def is_vertex_cover(graph: nx.Graph, cover: set[Any]) -> bool:
    """Return True if cover touches every edge of graph."""
    for u, v in graph.edges():
        if u not in cover and v not in cover:
            return False
    return True