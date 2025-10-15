from collections import deque
from typing import Any

import networkx as nx
import numpy as np

_rng = np.random.default_rng()


def get_uncovered_edges(graph: nx.Graph, cover: set[Any]) -> set[tuple[Any, Any]]:
    """Return edges not covered by the current cover.
    
    Args:
        graph: Input graph.
        cover: Current vertex cover.
    
    Returns:
        A set of edges (tuples) that are not covered by the vertices in 'cover'.
    """
    return {(u, v) for u, v in graph.edges() if u not in cover and v not in cover}


def _compute_vertex_score(
    graph: nx.Graph,
    node: Any,
    cover: set[Any],
    edge_weights: dict[tuple[Any, Any], float]) -> float:
    """Compute weighted score for a vertex based on uncovered edges it would cover.
    Args:
        graph: Input graph.
        node: Vertex to score.
        cover: Current vertex cover.
        edge_weights: Weights assigned to edges.
    Returns:
        A float score representing the benefit of adding 'node' to the cover.
    """
    score = 0.0
    for neighbor in graph.neighbors(node):
        if neighbor not in cover:
            edge = tuple(sorted([node, neighbor]))
            score += edge_weights.get(edge, 0.0)
    return score


def choose_swap(
    graph: nx.Graph,
    cover: set[Any],
    endpoints: tuple[Any, Any],
    tabu: deque,
    edge_weights: dict[tuple[Any, Any], float],
) -> tuple[Any, Any] | None:
    """Choose best swap: add one endpoint, remove one from cover.
    
    Args:
        graph: Input graph.
        cover: Current vertex cover.
        endpoints: Tuple of two vertices (u, v) from an uncovered edge.
        tabu: Deque of recently added/removed vertices to avoid immediate re-swapping.
        edge_weights: Weights assigned to edges.
    
    Returns:
        A tuple (add_node, remove_node) representing the swap, or None if no valid swap found.
    """
    best_gain = float('-inf')
    best_pairs = []
    
    for add_node in endpoints:
        if add_node in cover or add_node in tabu:
            continue
            
        add_score = _compute_vertex_score(graph, add_node, cover, edge_weights)
        
        for remove_node in cover:
            if remove_node in tabu:
                continue
                
            remove_score = _compute_vertex_score(graph, remove_node, cover, edge_weights)
            
            # Adjustment if add_node and remove_node are neighbors
            edge = tuple(sorted([add_node, remove_node]))
            adjustment = edge_weights.get(edge, 0.0) if graph.has_edge(add_node, remove_node) else 0.0
            
            gain = add_score - remove_score + adjustment
            
            if gain > best_gain:
                best_gain = gain
                best_pairs = [(add_node, remove_node)]
            elif gain == best_gain:
                best_pairs.append((add_node, remove_node))
    
    if not best_pairs:
        return None
    
    return best_pairs[_rng.integers(len(best_pairs))] if len(best_pairs) > 1 else best_pairs[0]
