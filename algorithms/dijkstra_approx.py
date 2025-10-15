from typing import Any

import networkx as nx

from utils import (
    all_components_special,
    complete_graph,
    count_non_isolated_components,
    cycle,
    is_complete_graph,
    is_cycle,
    is_path,
    is_vertex_cover,
    label_key,
    path,
)


def _step_2(S: set[Any], H: nx.Graph) -> tuple[set[Any], nx.Graph]:
    """
    Remove vertices in S from H and handle special graph structures.

    If there are complete graphs or cycles or paths in the connected components of H,
    then incorporate their corresponding minimum cover into S, and place every
    neighbour of a leaf into S as well.
    """
    while True:
        changed = False

        for n in list(S):
            if H.has_node(n):
                H.remove_node(n)

        for component in list(nx.connected_components(H)):
            subgraph = H.subgraph(component).copy()
            cover_vertices = set()
            if is_complete_graph(subgraph):
                cover_vertices = complete_graph(subgraph)
            elif is_cycle(subgraph):
                cover_vertices = cycle(subgraph)
            elif is_path(subgraph):
                cover_vertices = path(subgraph)
            else:
                continue

            new_vertices = cover_vertices - S
            if new_vertices:
                S.update(new_vertices)
                changed = True
            H.remove_nodes_from(cover_vertices)

        leaves = [n for n in H.nodes() if H.degree(n) == 1]
        if leaves:
            neighbours_to_add = set()
            for leaf in leaves:
                neighbours_to_add.update(H.neighbors(leaf))
            neighbours_to_add -= S
            if neighbours_to_add:
                S.update(neighbours_to_add)
                H.remove_nodes_from(neighbours_to_add)
                changed = True

        if not changed:
            break

    return S, H

def _step_3(G: nx.Graph, S: set[Any], u_i: Any) -> dict[str, Any]:
    """Derive working subgraph, allowed set, and distance data for Step 3."""
    if u_i not in S:
        raise ValueError("u_i must belong to the current cover set S")

    S_without_ui = set(S) - {u_i}
    H = G.copy()
    H.remove_nodes_from(S_without_ui)

    isolated_vertices = {v for v in H.nodes() if H.degree(v) == 0}
    L_nodes = set(G.nodes()) - S - isolated_vertices
    is_u_isolated = u_i in isolated_vertices

    distances = {}
    max_distance = 0
    if not is_u_isolated:
        try:
            raw_distances = nx.single_source_shortest_path_length(H, u_i)
        except nx.NetworkXError:
            raw_distances = {}
        distances = {node: dist for node, dist in raw_distances.items() if node in L_nodes}
        if distances:
            max_distance = max(distances.values())

    return {
        "H": H,
        "L": L_nodes,
        "isolated_vertices": isolated_vertices,
        "is_u_isolated": is_u_isolated,
        "distances": distances,
        "max_distance": max_distance,
    }

def _step_4(max_distance: int) -> bool:
    """Return True when the algorithm should branch to Step 5, else Step 6."""
    return max_distance > 1


def _step_5(H: nx.Graph, L: set[Any], distances: dict[Any, int], max_distance: int) -> Any | None:
    if max_distance <= 1:
        return None

    target_distance = max_distance - 1
    candidates = {v for v in L if distances.get(v) == target_distance}
    if not candidates:
        return None

    base_components = count_non_isolated_components(H)
    best_choice = None
    best_key = None

    for candidate in candidates:
        H_candidate = H.copy()
        if H_candidate.has_node(candidate):
            H_candidate.remove_node(candidate)
        component_count = count_non_isolated_components(H_candidate)
        increase = component_count - base_components
        degree = H.degree(candidate) if H.has_node(candidate) else 0
        key = (increase, -degree, label_key(candidate))
        if best_key is None or key < best_key:
            best_key = key
            best_choice = candidate

    return best_choice


def _step_6(G: nx.Graph, S: set[Any]) -> tuple[set[Any], Any | None, bool]:
    H_remaining = G.copy()
    H_remaining.remove_nodes_from(S)

    if H_remaining.number_of_edges() == 0:
        return S, None, True

    if all_components_special(H_remaining):
        final_cover, _ = _step_2(set(S), H_remaining)
        return final_cover, None, True

    non_isolated = [n for n in H_remaining.nodes() if H_remaining.degree(n) > 0]
    if not non_isolated:
        return S, None, True

    max_degree = max(H_remaining.degree(n) for n in non_isolated)
    tied = [n for n in non_isolated if H_remaining.degree(n) == max_degree]
    next_vertex = min(tied, key=label_key)
    return S, next_vertex, False


def dijkstra_approx(graph: nx.Graph, start_node: Any) -> set[Any]:
    """
    Approximate a vertex cover using the Dijkstra-guided strategy described.

    Args:
        graph: A NetworkX graph.
        start_node: The starting vertex u₁.

    Returns:
        A set of vertices that form a vertex cover.
    """

    if start_node not in graph:
        raise ValueError("start_node must exist in the input graph")

    S = {start_node}
    current_u = start_node
    S, _ = _step_2(S, graph.copy())

    if is_vertex_cover(graph, S):
        return S

    while True:
        if is_vertex_cover(graph, S):
            break

        step3_result = _step_3(graph, S, current_u)

        if step3_result["is_u_isolated"]:
            L_nodes = step3_result["L"]
            if not L_nodes:
                break
            next_vertex = min(L_nodes, key=label_key)
            if next_vertex in S:
                break
            S.add(next_vertex)
            current_u = next_vertex
            S, _ = _step_2(S, graph.copy())
            continue

        max_distance = step3_result["max_distance"]
        branch_to_step5 = _step_4(max_distance)

        if branch_to_step5:
            candidate = _step_5(
                step3_result["H"],
                step3_result["L"],
                step3_result["distances"],
                max_distance,
            )
            if candidate is None:
                new_cover, next_vertex, done = _step_6(graph, S)
                S = new_cover
                if done:
                    break
                if next_vertex is None or next_vertex in S:
                    break
                S.add(next_vertex)
                current_u = next_vertex
                S, _ = _step_2(S, graph.copy())
                continue

            S.add(candidate)
            current_u = candidate
            S, _ = _step_2(S, graph.copy())
            continue

        new_cover, next_vertex, done = _step_6(graph, S)
        S = new_cover
        if done:
            break
        if next_vertex is None or next_vertex in S:
            break
        S.add(next_vertex)
        current_u = next_vertex
        S, _ = _step_2(S, graph.copy())

    return S