# ⚡ Rapid Revision — Topic 19: Graphs

> **Target:** 5-minute pre-interview refresher on Graph algorithms, complexities, and condition rules.

---

## 🔑 Algorithm Selection Cheat Sheet
- **Single Source Shortest Path (non-negative):** Dijkstra ($O((V + E) \log V)$).
- **Single Source Shortest Path (negative weights):** Bellman-Ford ($O(V \times E)$).
- **All Pairs Shortest Path:** Floyd-Warshall ($O(V^3)$).
- **Minimum Spanning Tree:** Kruskal (Sort edges + DSU) or Prim (Min-heap).
- **Topological Sort:** DAGs only. DFS + stack or Kahn's in-degree BFS.
- **Bridges (Tarjan):** `low[v] > tin[u]`.
- **SCC (Kosaraju):** DFS finish stack $\to$ Transpose graph $\to$ DFS components.
