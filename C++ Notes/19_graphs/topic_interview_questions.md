# 💼 Topic Interview Question Bank — Topic 19: Graphs

---

### Q1: Why does Dijkstra's Algorithm fail with negative edge weights?
**Answer:**
Dijkstra relies on a **Greedy Choice Property**: once a node is extracted from the Min-Heap, its shortest distance is finalized and marked closed under the invariant that adding non-negative edges can only increase total path weight. A negative edge can retroactively decrease the distance to an already closed node, violating the greedy invariant and leading to suboptimal distances or infinite loops. Bellman-Ford is required for negative weights.
