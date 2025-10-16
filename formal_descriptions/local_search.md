COVER is an SLS algorithm for k-vertex cover, i. e. it takes as input a graph G = (V, E) and a parameter k, and searches for a vertex cover of size k of G. Its candidate solutions are subsets of the vertices V of size k (which are not necessarily vertex covers). The step to a neighbouring candidate solution consists of exchanging two vertices: a vertex u that is in the current candidate solution C is taken out of C, and a vertex v which is not currently in C is put into C.

The initial candidate solution is constructed greedily. In detail, COVER builds C by iteratively adding vertices that have a maximum number of incident edges which are not covered by C, i. e. they have no endpoint in C, until the cardinality of C is k. When several vertices satisfy the criterion for inclusion in C, COVER selects one of them randomly, with uniform probabilities. Favouring vertices of high degree is a common heuristic for vertex cover algorithms. In fact, we find that some benchmark problems are even solved by this initialization step alone, e. g. the p-hat class of the DIMACS benchmark set.

The termination criterion COVER uses is straightforward: at each step, it tests whether its current candidate solution is a vertex cover of G. The algorithm terminates when either a vertex cover is found, or when a maximum number of steps, denoted by MAX ITERATIONS, has been reached.

The most influential part of an SLS algorithm is the definition of its step function. COVER uses several heuristic criteria to choose which two vertices to exchange in C, but also utilizes a substantial element of randomness, thus striking a balance between guided search and the diversity that is necessary to escape local optima. This balance is achieved with a simple division of responsibilities: the vertex to be taken out of C is chosen mainly according to heuristics, while the vertex to be put into C is chosen almost randomly.

When choosing possible candidates for inclusion in C, COVER selects uniformly at random an edge e that is not covered. The vertex added to C is then chosen from one of the endpoints of e, ensuring that e will be covered in the successive candidate solution. When choosing which one of the two endpoints of e to include and which vertex to take out of the current candidate solution, COVER uses a heuristic based on an edge weighting scheme: with each edge of G, we associate a positive real number. Intuitively, these weights indicate for each edge how “difficult” it is to cover it – i. e. how difficult it is to find a candidate solution
that contains one of the endpoints of that edge.

In the beginning, all edge weights are initialized to a small constant (0.05).

In each of the following iterations, COVER adds 1 to the weights of all edges that are not covered. We then derive vertex weights from the weights of edges incident to the vertex. We say that a vertex v potentially covers an incident edge (v, u) if u is not in the current candidate solution C. Let the weight of a vertex v, weight(v), be the weighted sum of all edges that vertex v potentially covers. An exchange of two vertices a and b, where a is taken out of C and b is put into C then results in a gain defined as weight(b) − weight(a) + δ, where δ is the weight of the edge between a and b if they are connected, and zero otherwise. COVER tries to maximize this gain, thereby covering the more “difficult” edges of higher weight with greater priority. Using weights to direct the search of stochastic local search algorithms is popular practice, and a similar approach has led to very good results for the Boolean Satisfiability problem [19].

COVER also employs a taboo list of size 2, keeping track of the vertices last inserted into C and last removed from C. This prevents it from immediately reversing a decision made in the last iteration. Moreover, COVER remembers for each vertex the iteration count at which it was last removed from C. When inserting a vertex into C, COVER favours vertices that have not been in the cover recently. In particular, this “time stamp” criterion is used to break ties between all insertion candidates that result in maximum gain and are not taboo.

When removing vertices from the candidate solution, COVER chooses randomly with uniform probability between all removal candidates.

Pseudo code for the algorithm is given in Alg. 2

### Algorithm 2 COVER(G, k, MAX ITERATIONS)

initialize C greedily with |C| = k

initialize weights

iteration number = 1

**while** exists uncovered edge and iteration  number < MAX ITERATIONS do

    choose uncovered edge e = (u1, u2) randomly

    choose vertices u ∈ {u1, u2} and v ∈ C according to max gain criterion

    C = C\{v}

    C = C ∪ {u}

    taboo list = {v, u}

    u.time stamp = iteration number

    update weights

    increase iteration number by 1

**end while**