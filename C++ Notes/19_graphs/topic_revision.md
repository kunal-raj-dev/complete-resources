# ⚡ Topic 19 Revision: Graphs & Network Topologies

> **High-Yield Comprehensive Sheet:** Core graph algorithms, state transitions, time/space bounds, and decision matrix for placement interviews.

---

## 1. 🎯 Graph Algorithms Decision Matrix

| Problem / Target | Primary Algorithm | Time Complexity | Auxiliary Space | Prerequisite / Constraint |
|---|---|---|---|---|
| **Unweighted Shortest Path** | BFS | $O(V + E)$ | $O(V)$ | All edge weights must be identical/unweighted |
| **Connected Components** | DFS / BFS / DSU | $O(V + E)$ | $O(V)$ | Undirected or 2D grid matrix |
| **Directed Cycle Detection** | DFS (`recStack`) / Kahn's BFS | $O(V + E)$ | $O(V)$ | Directed Graph |
| **Undirected Cycle Detection**| DFS/BFS (`parent != neighbor`) | $O(V + E)$ | $O(V)$ | Undirected Graph |
| **Topological Sort** | Kahn's Algorithm (BFS) / DFS Stack | $O(V + E)$ | $O(V)$ | Directed Acyclic Graph (DAG) |
| **Non-Negative SSSP** | Dijkstra's Algorithm | $O((V + E) \log V)$ | $O(V)$ | No negative weight edges |
| **Negative Weights SSSP** | Bellman-Ford | $O(V \times E)$ | $O(V)$ | Detects negative weight cycles |
| **Minimum Spanning Tree (MST)**| Prim's (Dense) / Kruskal's (Sparse) | $O((V+E)\log V)$ / $O(E \log E)$ | $O(V)$ | Connected, undirected weighted graph |
| **Critical Bridges** | Tarjan's Bridge (`low[v] > tin[u]`)| $O(V + E)$ | $O(V)$ | Undirected connected graph |
| **Cut Vertices** | Tarjan's Articulation (`low[v] >= tin[u]`)| $O(V + E)$ | $O(V)$ | Root requires $\ge 2$ children |
| **Strongly Connected Components**| Kosaraju's 2-Pass DFS | $O(V + E)$ | $O(V)$ | Directed Graph |
| **All-Pairs Shortest Path** | Floyd-Warshall | $O(V^3)$ | $O(V^2)$ | Intermediate loop $k$ must be outer |

---

## 2. 🧠 Universal Code Patterns & Invariants

### 1. BFS Push-Before-Visit Guarantee
```cpp
// When adding a neighbor to a BFS queue:
visited[neighbor] = true; // MUST MARK BEFORE PUSHING!
q.push(neighbor);
```
*Why?* If you wait to mark it visited until you `pop()` it, multiple nodes traversing the graph at the same time might push that same neighbor into the queue multiple times, causing a memory limit exceeded (MLE) or TLE.

### 2. Kahn's Topological Sort Core Logic
```cpp
// Only push nodes with 0 incoming dependencies
for (int neighbor : adj[u]) {
    inDegree[neighbor]--;
    if (inDegree[neighbor] == 0) q.push(neighbor);
}
```

### 3. Dijkstra's Stale State Rejection
```cpp
auto [dist, u] = pq.top();
pq.pop();
// Ignore stale entries in the C++ priority_queue
if (dist > shortest_distance[u]) continue; 
```

### 4. DSU with Path Compression & Union by Rank
```cpp
int find(int u) {
    if (u == parent[u]) return u;
    return parent[u] = find(parent[u]); // Path compression on return
}
```

### 5. Tarjan's Bridge vs Articulation Point Invariant
```text
Bridge Edge (u, v):           low[v] > tin[u]   (Strictly no back-edge to u or higher)
Articulation Vertex u:        low[v] >= tin[u]  (Back-edge does not bypass u)
Root Articulation Vertex:     children > 1      (In DFS tree)
Back-Edge Update Rule:        low[u] = min(low[u], tin[v]) // MUST USE tin[v]
```

### 6. Floyd-Warshall Core Loop
```cpp
// k MUST be on the outside!
for (int k = 0; k < V; ++k)
    for (int i = 0; i < V; ++i)
        for (int j = 0; j < V; ++j)
            if (mat[i][k] != INF && mat[k][j] != INF)
                mat[i][j] = min(mat[i][j], mat[i][k] + mat[k][j]);
```

---

## 3. ⚠️ Fatal Traps to Avoid

1. **Cycle Checking Undirected Graphs:** You MUST pass the `parent` into your DFS. If you look at a neighbor and it's visited, it's only a cycle if `neighbor != parent`. The edge you just came from doesn't count as a cycle.
2. **Negative Edges in Dijkstra:** Standard Dijkstra does not work. Use Bellman-Ford. If you force Dijkstra, it will either loop infinitely or produce wrong shortest paths.
3. **Array Bounds in Grids:** When doing Flood Fill / Grid DFS, always write your boundary checks `if (r < 0 || c < 0 || r >= R || c >= C)` FIRST in the `if` statement so it short-circuits before attempting to evaluate `grid[r][c]`, avoiding SegFaults.
4. **Kosaraju's Visited Array:** Do not forget to completely clear/reset your `visited` array to `false` between Pass 1 and Pass 2!

---

## 4. 🔥 Interview Q&A — Google / Amazon Level

### Q1: When would you prefer BFS over DFS, and vice versa?
**BFS** is strictly better for finding the shortest path on unweighted graphs because it radiates outwards layer-by-layer. **DFS** is better when you need to explore all paths, perform topological sorting (relying on post-order finish times), or detect cycle dependencies. Memory-wise, BFS uses $O(W)$ where $W$ is the maximum width of the graph tree, whereas DFS uses $O(H)$ where $H$ is the depth. On very wide but shallow graphs, DFS takes less memory.

### Q2: What is the significance of the `low` array in Tarjan's algorithm?
The `low[v]` value represents the earliest (lowest discovery time) node that can be reached from the subtree rooted at `v` using **at most one** back-edge. If `low[v] > tin[u]`, it proves there is no alternative path back to `u` or its ancestors, meaning the edge `(u, v)` is the ONLY bridge connecting the two components.

### Q3: Why does Kosaraju's Algorithm require two passes and a transposed graph?
Strongly Connected Components (SCCs) form a DAG when condensed. 
- **Pass 1 (Original Graph):** Calculates the finish times of nodes. Pushing to a stack ensures nodes belonging to "sink" SCCs are at the bottom, and "source" SCCs are at the top.
- **Pass 2 (Transposed Graph):** We pop from the stack (visiting sources first). By reversing the edges, we trap the DFS inside the current SCC because the edges that used to go *out* to other SCCs now point *in*, preventing the DFS from leaking into other components.

### Q4: How would you detect a cycle in a Directed graph using BFS?
Use Kahn's Algorithm (Topological Sort). Track the count of nodes processed (those with `inDegree == 0`). If the graph has a cycle, nodes in the cycle will never reach `inDegree == 0`. At the end of BFS, if `processed_count != V`, a cycle exists.

### Q5: Can Disjoint Set Union (DSU) be used to detect cycles in a Directed Graph?
No. Standard DSU tracks undirected connectivity. In a directed graph, nodes `A -> B` and `A -> C` both being in the same set doesn't mean there is a cycle (e.g., `A -> B -> D` and `A -> C -> D`). It works exclusively for undirected graphs where any alternative path between two connected components inherently forms a cycle.

## 5. ⚡ 2-Minute Revision Flash Card

- **Shortest Path Unweighted:** BFS.
- **Shortest Path Non-Negative:** Dijkstra (Min-Heap).
- **Shortest Path Negative Edges:** Bellman-Ford ($V-1$ relaxations).
- **All Pairs Shortest Path:** Floyd-Warshall ($O(V^3)$ DP, $k$ is outer loop).
- **MST:** Prim's (Node-based, Min-Heap) or Kruskal's (Edge-based, DSU).
- **Topological Sort:** Kahn's (BFS, Indegree) or DFS (Stack on return).
- **Cycle Directed:** DFS (recStack) or Kahn's (processed < V).
- **Cycle Undirected:** DFS/BFS (visited && neighbor != parent) or DSU.
- **Bridges/Articulation:** Tarjan's (`low` and `tin` times).
- **Strongly Connected Components:** Kosaraju's (DFS stack $\to$ transpose $\to$ DFS).
