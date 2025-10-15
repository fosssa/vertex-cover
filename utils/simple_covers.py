from typing import Any

import networkx as nx

def get_path_order(G: nx.Graph) -> list[Any]:
    """Get vertices of a path in order from one end to the other."""
    if len(G.nodes()) == 0:
        return []
    if len(G.nodes()) == 1:
        return list(G.nodes())
    
    # Find endpoints (vertices with degree 1)
    endpoints = [n for n in G.nodes() if G.degree(n) == 1]
    if len(endpoints) != 2:
        # Fallback to any ordering if not a proper path
        return list(G.nodes())
    
    try:
        return nx.shortest_path(G, endpoints[0], endpoints[1])
    except nx.NetworkXNoPath:
        # Fallback if no path exists (shouldn't happen for connected components)
        return list(G.nodes())


def complete_graph(subgraph: nx.Graph) -> set[Any]:
    """
    Handle complete graph case for vertex cover.
    
    For complete graph Kn, minimum vertex cover size is n-1.
    Returns all but one vertex.
    """
    vertices = list(subgraph.nodes())
    if vertices:
        return set(vertices[:-1])  # Return all except the last vertex
    return set()


def cycle(subgraph: nx.Graph) -> set[Any]:
    """
    Handle cycle case for vertex cover.
    
    For cycle, minimum vertex cover size is n/2 (rounded up).
    Takes every other vertex.
    """
    vertices = list(subgraph.nodes())
    if len(vertices) >= 3:  # Valid cycle must have at least 3 vertices
        # Take every other vertex starting from first
        return set(vertices[::2])
    return set()


def path(subgraph: nx.Graph) -> set[Any]:
    """
    Handle path case for vertex cover.
    
    For path, uses greedy approach: take every other vertex
    starting from second vertex (index 1).
    """
    if len(subgraph.nodes()) >= 2:
        path_vertices = get_path_order(subgraph)
        # Take every other vertex starting from second
        return set(path_vertices[1::2])
    return set()
