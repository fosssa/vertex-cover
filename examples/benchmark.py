import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import time
import statistics as stats
import networkx as nx
from networkx.algorithms.approximation import min_weighted_vertex_cover

from algorithms import greedy_support, dijkstra_approx, cover_local_search


def verify_vertex_cover(G, cover):
    """Verify that the given set is a valid vertex cover."""
    return all(u in cover or v in cover for u, v in G.edges())


def maximum_matching_lower_bound(G):
    """Calculate lower bound using maximum matching."""
    M = nx.algorithms.matching.max_weight_matching(G, maxcardinality=True)
    return len(M)


def run_algorithm(G, algo_func, **kwargs):
    """Run a single algorithm and return timing and result info."""
    G_copy = G.copy() if kwargs.pop('needs_copy', False) else G
    t0 = time.perf_counter()
    cov = algo_func(G_copy, **kwargs)
    dt = time.perf_counter() - t0
    ok = verify_vertex_cover(G, cov)
    return dt, len(cov), ok


def bench_family(name, gen, sizes, reps=3):
    """Benchmark a family of graphs across different sizes."""
    print(f"\n{'='*80}")
    print(f"{name}")
    print(f"{'='*80}")
    
    for n in sizes:
        G = gen(n)
        m = G.number_of_edges()
        lb = maximum_matching_lower_bound(G)
        
        start_node = next(iter(G.nodes())) if G.nodes() else None
        # Use lower bound + 40% buffer for local search target
        # Regular graphs need more buffer due to structural constraints
        k = int(lb * 1.4) + 2 if lb > 0 else max(1, n // 10)
        
        # Wrapper for NetworkX to return a set
        def nx_wrapper(G):
            return set(min_weighted_vertex_cover(G))
        
        algorithms = [
            ("NetworkX", nx_wrapper, {'needs_copy': False}),
            ("Greedy Support", greedy_support, {'needs_copy': False}),
            ("Dijkstra Approx", dijkstra_approx, {"start_node": start_node, 'needs_copy': False}),
            ("Local Search", cover_local_search, {"k": k, "max_iterations": 5000, 'needs_copy': False}),
        ]
        
        print(f"\nGraph: n={n}, m={m}, MM_lb={lb}")
        print(f"{'Algorithm':<20} {'Time (ms)':<12} {'Cover Size':<12} {'Ratio':<8} {'Valid'}")
        print("-" * 80)
        
        for algo_name, algo_func, kwargs in algorithms:
            times, covers, oks = [], [], []
            
            for _ in range(reps):
                try:
                    dt, cov_sz, ok = run_algorithm(G, algo_func, **kwargs)
                    times.append(dt * 1000)
                    covers.append(cov_sz)
                    oks.append(ok)
                except Exception as e:
                    print(f"{algo_name:<20} ERROR: {str(e)[:50]}")
                    break
            else:
                median_time = stats.median(times)
                median_cover = int(stats.median(covers))
                ratio = median_cover / max(1, lb)
                all_valid = all(oks)
                
                print(f"{algo_name:<20} {median_time:>10.2f}  {median_cover:>10}  {ratio:>6.3f}  {all_valid}")

def main():
    """Run benchmarks on various graph families."""
    # Use smaller sizes for reasonable runtime
    sizes_sparse = [50, 100, 200]
    sizes_medium = [50, 100]

    bench_family(
        "Erdős-Rényi sparse (p=0.1)",
        lambda n: nx.gnp_random_graph(n, 0.1, seed=100),
        sizes_sparse,
        reps=3
    )
    
    bench_family(
        "Barabási-Albert (m=3)",
        lambda n: nx.barabasi_albert_graph(n, 3, seed=200),
        sizes_medium,
        reps=3
    )
    
    bench_family(
        "Random regular (d=6)",
        lambda n: nx.random_regular_graph(6, n, seed=300),
        sizes_medium,
        reps=3
    )
    
    bench_family(
        "Watts-Strogatz (k=8, p=0.1)",
        lambda n: nx.watts_strogatz_graph(n, 8, 0.1, seed=400),
        sizes_medium,
        reps=3
    )


if __name__ == "__main__":
    main()