# 💼 Topic 19 Interview Question Bank: Graphs & Network Topologies

> **Curated FAANG Interview Bank:** High-frequency technical interview questions, conceptual traps, system architecture queries, and debugging challenges.

---

## 📌 Conceptual & Architectural Questions

### Q1: Why does Dijkstra's algorithm fail on graphs with negative edge weights?
**Detailed Explanation:** Dijkstra is a greedy algorithm based on the premise that once a vertex is removed from the priority queue, its shortest distance is permanently finalized. With negative edge weights, a longer path with many edges can encounter a large negative weight later and become strictly cheaper than the previously finalized distance. Because Dijkstra never revisits finalized nodes, it produces incorrect results.
**Solution:** Use the Bellman-Ford algorithm ($O(V \times E)$).

### Q2: Compare Prim's vs. Kruskal's algorithm. When would you prefer one over the other?
**Answer:**
- **Prim's Algorithm:** Vertex-centric greedy algorithm. Takes $O((V + E) \log V)$ with binary heap or $O(V^2)$ with an adjacency matrix. Best for **Dense Graphs** ($E \approx V^2$).
- **Kruskal's Algorithm:** Edge-centric greedy algorithm. Takes $O(E \log E)$ time due to edge sorting. Best for **Sparse Graphs** ($E \ll V^2$). Kruskal's is also easier to implement when edge lists are already sorted.

### Q3: What is the exact difference between a Cross-Edge, Back-Edge, Forward-Edge, and Tree-Edge in DFS?
**Answer:**
- **Tree-Edge:** Edge traversed to visit an undiscovered vertex for the first time.
- **Back-Edge:** Edge pointing from current node to an ancestor in the active DFS recursion stack. **Presence of a back-edge proves a cycle!**
- **Forward-Edge:** Edge pointing from current node to a descendant in the DFS tree that was already visited.
- **Cross-Edge:** Edge connecting two vertices where neither is an ancestor of the other (connects different branches).

### Q4: How does Disjoint Set Union achieve $O(\alpha(N))$ nearly constant time?
**Answer:** DSU combines two synergistic optimizations:
1. **Union by Rank/Size:** Limits tree depth to $O(\log N)$ by attaching shallower trees under deeper roots.
2. **Path Compression:** Flattens tree branches during `find()` operations by pointing every visited node directly to the root.
Together, they reduce the amortized cost per operation to the inverse Ackermann function $\alpha(N) < 5$ for all universe sizes.

### Q5: Why is the bridge condition `low[v] > tin[u]` while articulation point is `low[v] >= tin[u]`?
**Answer:**
- For a bridge edge $(u, v)$, $v$ must have strictly no alternative way to reach $u$ or any ancestor of $u$. If $v$ could reach $u$ via a back-edge, `low[v] == tin[u]`, so removing edge $(u, v)$ would not disconnect $v$. Hence strict inequality `>` is required.
- For an articulation vertex $u$, if $v$'s back-edge only reaches $u$ itself (`low[v] == tin[u]`), removing vertex $u$ still destroys $v$'s only connection to the rest of the graph! Hence weak inequality `>=` applies.

### Q6: Can you find the shortest path in an unweighted graph using Dijkstra?
**Answer:** You *can*, but you shouldn't. Dijkstra runs in $O(V \log V + E)$. For an unweighted graph, all edges have weight 1. A simple BFS queue naturally explores nodes level-by-level (distance 1, 2, 3...), guaranteeing the shortest path in strictly $O(V + E)$ time without the overhead of a priority queue.

### Q7: Explain Kosaraju's vs Tarjan's algorithm for Strongly Connected Components (SCCs).
**Answer:** 
- **Kosaraju's:** Uses two passes of DFS and requires reversing the graph edges ($G^T$). It is conceptually simpler: DFS for finish times, transpose, then DFS on transpose using finish times.
- **Tarjan's:** Uses a single pass of DFS using `tin` and `low` arrays (like bridges/articulation points) and a stack to build components on the fly. It is marginally faster in practice (better cache locality, no transpose needed) but conceptually harder. Both are $O(V + E)$.

### Q8: What happens if you use a DFS instead of BFS in Kahn’s Algorithm for Topological Sort?
**Answer:** Kahn's Algorithm relies entirely on in-degrees and a queue (BFS). If you swap the queue for a stack (DFS), Kahn's algorithm will *still* produce a valid topological sort! Any data structure that retrieves elements with 0 in-degree works. However, using DFS for standard topological sort typically refers to the post-order stack reversal method, not Kahn's.

### Q9: How can you find the longest path in a Directed Acyclic Graph (DAG)?
**Answer:** Unlike general graphs (where longest path is NP-Hard), in a DAG you can find it in $O(V + E)$. First, find the Topological Sort. Then initialize a `dist` array to $-\infty$, `dist[source] = 0`. Iterate through the nodes in topological order, relaxing edges: `dist[v] = max(dist[v], dist[u] + weight(u, v))`.

### Q10: How do you detect a negative weight cycle in a graph?
**Answer:** 
- **Bellman-Ford:** Run the edge relaxation loop $V-1$ times. Run it one more time (the $V$-th time). If any distance updates during this final pass, a negative cycle exists.
- **Floyd-Warshall:** After running the $O(V^3)$ algorithm, check the main diagonal of the distance matrix. If `dist[i][i] < 0` for any $i$, a negative cycle exists.

### Q11: What is the "Bipartite Graph" test and why is it useful?
**Answer:** A graph is bipartite if you can color it with 2 colors such that no adjacent nodes have the same color. It is tested using BFS/DFS coloring. It is useful for mapping relationships (e.g., matching applicants to jobs, students to classes) and fundamentally means the graph contains **no odd-length cycles**.

### Q12: Why do we use a Min-Heap (Priority Queue) in Dijkstra's algorithm instead of a regular Queue?
**Answer:** A regular queue processes nodes strictly in the order they were discovered. In a weighted graph, discovering a node early doesn't mean we found the shortest path to it. A Min-Heap ensures we always process the currently known closest node first, which mathematically guarantees that when a node is popped, we have found the absolute shortest path to it (assuming no negative weights).

---

## 💻 Output Prediction & Debugging Challenges

### Q13: [Output Prediction] What happens if Floyd-Warshall's outer loop is $i$ instead of $k$?
```cpp
// INCORRECT NESTING:
for (int i = 0; i < V; ++i)
    for (int j = 0; j < V; ++j)
        for (int k = 0; k < V; ++k)
            matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j]);
```
**Answer:** This computes the shortest path between $i$ and $j$ considering only a single intermediate hop $k$. It completely fails to propagate multi-hop paths. In Floyd-Warshall DP, $k$ represents the subset of allowed intermediate vertices $\{0 \dots k\}$ and MUST be the outermost loop to build paths incrementally.

### Q14: [Debugging] Find the flaw in this Disjoint Set Union `find` function.
```cpp
int find(int i) {
    if (parent[i] == i) return i;
    return find(parent[i]);
}
```
**Answer:** It lacks **Path Compression**. It returns the root correctly, but leaves the tree structure intact. If the tree becomes a skewed linked list, `find` degrades to $O(N)$. 
**Fix:** Update the parent pointer during the recursive return: `return parent[i] = find(parent[i]);`

### Q15: [Debugging] Why does this standard Dijkstra template TLE (Time Limit Exceeded) on large graphs?
```cpp
while(!pq.empty()) {
    auto [dist, u] = pq.top();
    pq.pop();
    for (auto edge : adj[u]) {
        int v = edge.to;
        int weight = edge.weight;
        if (dist + weight < distance[v]) {
            distance[v] = dist + weight;
            pq.push({distance[v], v});
        }
    }
}
```
**Answer:** It lacks the **stale state check**. In C++, `priority_queue` does not support updating keys. So we push duplicate entries for the same node `v` with better distances. If `v` is popped later with an outdated, larger distance, the code still uselessly iterates over all its neighbors.
**Fix:** Add `if (dist > distance[u]) continue;` immediately after popping from `pq`.
