from __future__ import annotations

from collections import deque
from typing import Any

import networkx as nx
import numpy as np

from utils import choose_swap, get_uncovered_edges

_rng = np.random.default_rng()


def _greedy_initial_cover(graph: nx.Graph, k: int) -> set[Any]:
    """Build initial cover by greedily selecting vertices with most uncovered edges.
    
    Args:
        graph: Input graph.
        k: Desired size of the cover.

    Returns:
        A set of vertices forming the initial cover.
    """
    cover = set()
    uncovered_edges = set(graph.edges())
    
    while len(cover) < k and uncovered_edges:
        # Find vertices that cover the most uncovered edges
        best_count = 0
        best_vertices = []
        
        for node in graph.nodes():
            if node in cover:
                continue
            # Count uncovered edges incident to this node
            count = sum(1 for u, v in uncovered_edges if node in (u, v))
            if count > best_count:
                best_count = count
                best_vertices = [node]
            elif count == best_count and count > 0:
                best_vertices.append(node)
        
        if not best_vertices:
            break
            
        chosen = _rng.choice(best_vertices)
        cover.add(chosen)
        
        # Remove covered edges
        uncovered_edges = {(u, v) for u, v in uncovered_edges if chosen not in (u, v)}
    
    # Fill remaining slots with random vertices if needed
    if len(cover) < k:
        remaining = [node for node in graph.nodes() if node not in cover]
        needed = min(k - len(cover), len(remaining))
        cover.update(_rng.choice(remaining, size=needed, replace=False))
    
    return cover


def cover_local_search(
    graph: nx.Graph,
    k: int,
    max_iterations: int = 1000,
) -> set[Any]:
    """Local search algorithm for vertex cover problem.
       Iteratively swaps vertices to improve cover quality using weighted edges.
    
    Args:
        graph: Input graph.
        k: Desired size of the vertex cover.
        max_iterations: Maximum number of iterations to perform.
    
    Returns:
        A set of vertices forming the best vertex cover found.
    """
    cover = _greedy_initial_cover(graph, k)
    
    # Initialize edge weights (used to prioritize uncovered edges)
    edge_weights = {tuple(sorted([u, v])): 0.05 for u, v in graph.edges()}
    
    # Track best solution found
    uncovered_edges = get_uncovered_edges(graph, cover)
    best_cover = set(cover)
    best_uncovered_count = len(uncovered_edges)
    
    # Tabu list prevents immediate re-swapping
    tabu = deque(maxlen=4)
    
    iteration = 0
    while uncovered_edges and iteration < max_iterations:
        iteration += 1
        
        # Pick a random uncovered edge
        chosen_edge = list(uncovered_edges)[_rng.integers(len(uncovered_edges))]
        swap = choose_swap(graph, cover, chosen_edge, tabu, edge_weights)
        
        if swap is None:
            break
        
        add_node, remove_node = swap
        
        # Perform swap
        cover.remove(remove_node)
        cover.add(add_node)
        tabu.append(add_node)
        tabu.append(remove_node)
        uncovered_edges = get_uncovered_edges(graph, cover)
        
        for edge in uncovered_edges:
            edge_weights[edge] += 1.0
        
        if len(uncovered_edges) < best_uncovered_count:
            best_uncovered_count = len(uncovered_edges)
            best_cover = set(cover)
        
        if len(uncovered_edges) == 0:
            break
    
    return best_cover
