from typing import Any

import networkx as nx

from .checks import is_complete_graph, is_cycle, is_path


def label_key(node: Any) -> tuple[int, Any]:
    """Build a stable ordering key for arbitrary hashable labels."""
    if isinstance(node, (int, float, str)):
        return (0, node)
    return (1, repr(node))


def count_non_isolated_components(graph: nx.Graph) -> int:
    """Return the number of connected components that contain at least one edge."""
    count = 0
    for component in nx.connected_components(graph):
        sub = graph.subgraph(component)
        if sub.number_of_edges() == 0:
            continue
        count += 1
    return count


def _is_special_component(subgraph: nx.Graph) -> bool:
    return (
        is_complete_graph(subgraph)
        or is_cycle(subgraph)
        or is_path(subgraph)
    )


def all_components_special(graph: nx.Graph) -> bool:
    """Return True if every connected component is a complete graph, cycle, or path."""
    if graph.number_of_nodes() == 0:
        return True
    for component in nx.connected_components(graph):
        sub = graph.subgraph(component).copy()
        if not _is_special_component(sub):
            return False
    return True

