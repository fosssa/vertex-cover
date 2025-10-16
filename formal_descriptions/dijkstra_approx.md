Let G = (V,E) be a graph, where V is the set of vertices and E is the set of edges. A vertex cover S is a subset of V such that each edge has at least one ends in S. A minimum vertex cover of G is one subset of V in which the number of vertices is minimized. In this paper, we concern with undirected and connected plane graphs. If G is disconnected, each components would be discussed separately.

Label all vertices of G, and let an arbitrary vertex be the initial point denoted by $u_1$. Now we have set $S = \{u_1\}$, subgraph $H = G \setminus S$, allowed set $L = V \setminus \left(S \cup \{\text{isolated vertices of } H\}\right)$.

Assume we already have the set $S = \{u_1, u_2, \ldots, u_{i-1}, u_i\}$. If subgraph H are consist of isolated vertices, then S is a vertex cover of G. Because in graph G there is no edge with two ends in H. Now the edge set E is partitioned into two sets $E_1$ and $E_2$ with $E = E_1 \cup E_2$, where the edges of $E_1$ have one endpoint in S, the edges of $E_2$ have both endpoints in S. Now each edge of G has at least one ends in set S, so S is a vertex cover of G.

If there are complete graphs or circles or paths in the connected components of H, incorporate their corresponding minimum covers into the
set S separately, and put all adjacent vertices of leaves into the set S also.

If $u_i$ is an isolated vertex in $H = G \setminus \{u_1, u_2, \ldots, u_{i-1}\}$, then let $u_{i+1}$ be an arbitrary vertex of L and $S = S \cup \{u_{i+1}\}$. Otherwise, by using Dijkstra algorithm in subgraph $H = G \setminus \{u_1, u_2, \ldots, u_{i-1}\}$, we can get the shortest distances $d_{u_i, v}$ for $v \in L$ in H and compute the maximum value $d$. Then according to the two cases below to get a vertex cover of G.

### Case 1: d > 1

Let $T = \{v \mid d_{u_i, v} = d - 1,\ v \in L\}$, which is a set containing the vertices with the distance of $d - 1$ from $u_i$ to them. According to the following criteria, we will get the vertex $u_{i+1}$.

Delete each vertex of set T separately in subgraph H. Let $u_{i+1}$ be the vertex which has the minimum connected component increase after deleting, and the count of connected components does not include the isolated vertices.

If they have the same increase of connected components, then let $u_{i+1}$ be the vertex with maximum degree in H.

If there is only one vertex in T, then let it be $u_{i+1}$. If the conditions of all vertices in T are the same after deleting, then let $u_{i+1}$ be the one with the minimum label.  
Let $S = S \cup \{u_{i+1}\}$, and repeat the process above.

### Case 2: d = 1 

It is obviously that $u_i$ is adjacent to each vertex of set L. If $H = G \setminus S$ is the disjoint union of complete graphs or circles or paths, then it is easy to get a minimum vertex cover of H. So we obtain a vertex cover of G. Otherwise, let $u_{i+1}$ be the vertex with the maximum degree, or the minimum label if they have same degree in H. Now let $S = S \cup \{u_{i+1}\}$, and repeat the process above.

Now list the specific steps of the Algorithm below.

# The Algorithm

### Step 1.
Initialization: initialize the node labels and $S = \{u_1\}, L = \emptyset, T = \emptyset$.

### Step 2.
$S = \{u_1, u_2, \ldots, u_i\}$
If subgraph $H = G \setminus S$ are consist of isolated vertices, then stop the
Algorithm.
If there are complete graphs or circles or paths in the connected components of H, then incorporate their corresponding minimum cover into the set S separately, and put all adjacent vertices of leaves into the set S also. Go to Step 2 and still use the vertex iu to search.
Otherwise, go to Step 3.

### Step 3.
Let $H = G \setminus \{u_1, u_2, \ldots, u_{i-1}\}$ and $L = V \setminus \left(S \cup \{\text{isolated vertices of } H\}\right)$.  
If $u_i$ is an isolated vertex in H, then let $u_{i+1}$ be an arbitrary vertex of L. $S = S \cup \{u_{i+1}\}$, go to Step 2. Else invoke Dijkstra algorithm to get the shortest distances $d_{u_i, v}$ for $v \in L$ in H and compute maximum value $d$. Go to Step 4.

### Step 4.
If d > 1, go to Step 5, else Step 6.

### Step 5.
Let $T = \{v \mid d_{u_i, v} = d - 1,\ v \in L\}$, then according to Case 1 in the text to select $u_{i+1}$.
Let $S = S \cup \{u_{i+1}\}$ and go to Step 2.

### Step 6.
If subgraph $H = G \setminus S = G \setminus \{u_1, u_2, \ldots, u_i\}$ are the disjoint union of complete graphs or circles or paths, then a minimum vertex cover of H is obtained and stop the Algorithm.  
Otherwise, let $u_{i+1}$ be the vertex with the maximum degree, or with the minimum label if they have same degree in H. Let $S = S \cup \{u_{i+1}\}$ and go to Step 2.
