from typing import Any

import networkx as nx

def greedy_support(graph: nx.Graph) -> set[Any]:
    """
    Greedy algorithm to find a vertex cover of a graph using support values.

    Args:
        graph: Input graph.
    
    Returns:
        A set of vertices that form a vertex cover.
    """
    cover = set()
    working_graph = graph.copy()

    while working_graph.edges:
        # Step 1: Calculate degree for each vertex
        vertex_degrees = dict(working_graph.degree())
        
        if not vertex_degrees:
            break
        
        # Step 2: Calculate support value for each vertex
        # Support = sum of degrees of all neighbors
        vertex_support = {}
        for vertex in working_graph.nodes():
            neighbors = list(working_graph.neighbors(vertex))
            support = sum(vertex_degrees[neighbor] for neighbor in neighbors)
            vertex_support[vertex] = support
            
        # Step 3: Find vertices with minimum support value
        min_support = min(vertex_support.values())
        min_support_vertices = [v for v, sup in vertex_support.items() if sup == min_support]
        
        # Step 4: Get all neighbors of minimum support vertices and find max support among them
        neighbors = set()
        for vertex in min_support_vertices:
            neighbors.update(working_graph.neighbors(vertex))
        
        if not neighbors:
            selected_vertex = min_support_vertices[0]
        else:
            # Select neighbor with maximum support value
            neighbor_support = {v: vertex_support[v] for v in neighbors}
            max_support = max(neighbor_support.values())
            max_support_neighbors = [v for v, sup in neighbor_support.items() if sup == max_support]
            
            # If multiple vertices have the same max support, choose the first one
            selected_vertex = max_support_neighbors[0]
        
        # Step 5: Add vertex to cover and remove all adjacent edges
        cover.add(selected_vertex)
        working_graph.remove_node(selected_vertex)

    return cover
