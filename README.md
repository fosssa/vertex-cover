# Vertex Cover Toolkit

Small research sandbox for experimenting with approximation and heuristic solutions to the minimum vertex cover problem. The repository bundles executable Python implementations, the supporting maths write-ups, notebook and benchmark for exploration.

## Getting Started
- Create a virtual environment (Python 3.12+): `python -m venv .venv` then `.\.venv\Scripts\Activate.ps1`
- Install dependencies: `pip install -r requirements.txt`

### Quick Example
```python
import networkx as nx
from algorithms import greedy_support, dijkstra_approx, cover_local_search

G = nx.gnp_random_graph(25, 0.15, seed=42)

greedy_cover = greedy_support(G)
dijkstra_cover = dijkstra_approx(G, start_node=next(iter(G.nodes())))
local_search_cover = cover_local_search(G, k=len(greedy_cover))

assert all(u in greedy_cover or v in greedy_cover for u, v in G.edges())
```

## Algorithms (`algorithms/`)
- `greedy.py` – Selects vertices with minimal support (sum of neighbour degrees); fast baseline that performs well on sparse graphs.
- `dijkstra_approx.py` – Implements the labelled-vertex, Dijkstra-guided branching algorithm from the accompanying notes, including special handling for complete graphs, cycles, and paths.
- `cover_local_search.py` – Starts from a greedy cover and performs tabu-guided swaps driven by weighted uncovered edges to refine toward smaller covers.

## Formal Descriptions (`formal_descriptions/`)
- `greedy_support.md`
- `dijkstra_approx.md`
- `local_search.md`

### Based on Literature
- Mohammed Eshtay, Azzam Sleit and Ahmad Sharieh. “NMVSA Greedy Solution for Vertex Cover Problem”. International Journal of Advanced Computer Science and Applications (IJACSA) 7.3 (2016). http://dx.doi.org/10.14569/IJACSA.2016.070309
- Jingrong Chen, Lei Kou, Xiaochuan Cui, An Approximation Algorithm for the Minimum Vertex Cover Problem, Procedia Engineering, Volume 137, 2016, Pages 180-185, ISSN 1877-7058, https://doi.org/10.1016/j.proeng.2016.01.248.
- Richter, S., Helmert, M., Gretton, C. (2007). A Stochastic Local Search Approach to Vertex Cover. In: Hertzberg, J., Beetz, M., Englert, R. (eds) KI 2007: Advances in Artificial Intelligence. KI 2007. Lecture Notes in Computer Science, vol 4667. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-540-74565-5_31

## Utilities (`utils/`)
- `checks.py` – Graph predicates (`is_vertex_cover`, `is_complete_graph`, `is_cycle`, `is_path`) used across algorithms.
- `dijkstra_helpers.py` – Component counting, label ordering, and special-structure checks supporting the Dijkstra approximation.
- `local_search_helpers.py` – Edge-weighted swap scoring, tabu handling, and uncovered-edge extraction for the local search heuristic.
- `simple_covers.py` – Closed-form minimum covers for complete graphs, cycles, and paths reused in step reductions.

## Examples & Notebooks (`examples/`)
- `benchmark.py` – CLI benchmark comparing all algorithms (and NetworkX function) on multiple random graph families with runtime and cover quality summaries.
- `plots.ipynb` – Notebook for visualising benchmark output and algorithm behaviour.

## Requirements
- Core dependencies are declared in `pyproject.toml` for editable installs and mirrored in `requirements.txt`.
- Primary libraries: `networkx` for graph primitives, `numpy` for randomness, `matplotlib` for visualisation, and `pytest` for the test suite.

## Project Status
- This is a workbench project: expect small, focused utilities rather than a polished package.
