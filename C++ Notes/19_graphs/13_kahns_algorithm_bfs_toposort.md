# Lecture 123: Topological Sorting using Kahn's Algorithm (BFS)

> **One-Line Purpose:** Master in-degree dependency reduction using a FIFO queue to compute topological ordering and simultaneously detect directed cycles in $O(V + E)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #123  
> **Video ID:** `BnQpaTZg6Sc`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=BnQpaTZg6Sc)  
> **Duration:** 18:47  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
By the end of this lecture, you should understand:
- The concept of In-Degree: number of incoming directed edges arriving at a vertex.
- Kahn's Invariant: Vertices with `inDegree == 0` have zero pending prerequisites and can be immediately scheduled.
- How removing a node decrements its neighbors' in-degrees.
- How Kahn's algorithm doubles as an elegant directed cycle detector (if `visitedCount < V`, a cycle exists).

---

## 🔵 Algorithmic Principle & Step-by-Step Mechanics

```
DAG Example:
5 ---> 0 <--- 4
|             |
v             v
2 ---> 3 ---> 1

In-Degrees:
Node 0: 2 (from 5, 4)
Node 1: 2 (from 4, 3)
Node 2: 1 (from 5)
Node 3: 1 (from 2)
Node 4: 0 (No prerequisites!)
Node 5: 0 (No prerequisites!)

Initial Queue with in-degree 0: [4, 5]
```

### Algorithm Steps:
1. Compute `inDegree[u]` for all $u \in V$.
2. Enqueue all vertices where `inDegree[u] == 0`.
3. While the queue is not empty:
   - Pop vertex $u$ and append to `topoOrder`.
   - For each outgoing neighbor $v$ of $u$:
     - Decrement `inDegree[v]--`.
     - If `inDegree[v] == 0`, push $v$ into the queue.
4. If `topoOrder.size() < V`, the graph contains a directed cycle (nodes in the cycle never reach in-degree 0).

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <queue>

using namespace std;

class KahnsAlgorithm {
private:
    int V;
    vector<vector<int>> adj;

public:
    KahnsAlgorithm(int vertices) : V(vertices), adj(vertices) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v); // Directed edge u -> v
    }

    pair<bool, vector<int>> getTopologicalOrder() {
        vector<int> inDegree(V, 0);

        // 1. Calculate in-degrees for all vertices
        for (int u = 0; u < V; ++u) {
            for (int v : adj[u]) {
                inDegree[v]++;
            }
        }

        // 2. Push all nodes with 0 in-degree into Queue
        queue<int> q;
        for (int i = 0; i < V; ++i) {
            if (inDegree[i] == 0) {
                q.push(i);
            }
        }

        vector<int> topoOrder;

        // 3. Process BFS Queue
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            topoOrder.push_back(u);

            for (int v : adj[u]) {
                inDegree[v]--;
                if (inDegree[v] == 0) {
                    q.push(v);
                }
            }
        }

        // 4. Cycle Detection Check
        if (topoOrder.size() != (size_t)V) {
            // Cycle detected! Not all nodes could be resolved
            return {false, {}};
        }

        return {true, topoOrder};
    }
};

int main() {
    KahnsAlgorithm g(6);
    g.addEdge(5, 2);
    g.addEdge(5, 0);
    g.addEdge(4, 0);
    g.addEdge(4, 1);
    g.addEdge(2, 3);
    g.addEdge(3, 1);

    auto [isDAG, order] = g.getTopologicalOrder();
    if (isDAG) {
        cout << "Kahn's Topo Sort Order: ";
        for (int x : order) cout << x << " ";
        cout << endl;
    } else {
        cout << "Graph contains a directed cycle! Topological sort impossible." << endl;
    }

    return 0;
}
```

---

## 🔍 Detailed Dry Run Table

| Step | Current Queue | Popped $u$ | Neighbors Decremented | In-Degree State after step | Topo Order |
|---|---|---|---|---|---|
| Init | `[4, 5]` | — | — | `{0:2, 1:2, 2:1, 3:1, 4:0, 5:0}` | `[]` |
| 1 | `[5]` | 4 | $0 \to 1, 1 \to 1$ | `{0:1, 1:1, 2:1, 3:1, 4:0, 5:0}` | `[4]` |
| 2 | `[]` | 5 | $2 \to 0$ (push 2), $0 \to 0$ (push 0) | `{0:0, 1:1, 2:0, 3:1}` | `[4, 5]` |
| 3 | `[0]` | 2 | $3 \to 0$ (push 3) | `{0:0, 1:1, 2:0, 3:0}` | `[4, 5, 2]` |
| 4 | `[3]` | 0 | None (outgoing to none) | `{1:1, 3:0}` | `[4, 5, 2, 0]` |
| 5 | `[]` | 3 | $1 \to 0$ (push 1) | `{1:0}` | `[4, 5, 2, 0, 3]` |
| 6 | `[]` | 1 | None | All 0 | `[4, 5, 2, 0, 3, 1]` |

Total vertices resolved: 6 of 6. Correct DAG valid topological order!

---

## ⚠️ Common Pitfalls & Corner Cases
1. **Topological Sort on Graphs with Cycles:** Never forget to check `topoOrder.size() == V`. If equal, it's a DAG. If strictly less, a directed cycle exists.
2. **Multiple Valid Topological Orderings:** A graph can have several valid topological sorts (e.g. `[4, 5, ...]` vs `[5, 4, ...]`). If the interview requests lexicographically smallest topological sort, replace `queue<int>` with a min-heap `priority_queue<int, vector<int>, greater<int>>`.

---

## 🔥 FAANG Technical Interview Questions
- **Q: How does Kahn's algorithm detect cycles compared to DFS?**  
  *A:* Kahn's algorithm detects cycles because vertices involved in a cycle or reachable only through a cycle will never reach in-degree 0; hence they never enter the queue, making `topoOrder.size() < V`. DFS detects cycles via back-edges pointing to active ancestors in the recursion stack (`inStack[v] == true`).
- **Q: Can Kahn's algorithm be applied to Undirected Graphs?**  
  *A:* No. In an undirected graph, every edge $(u, v)$ contributes in-degrees to both $u$ and $v$. In-degree 0 vertices would only be completely isolated nodes.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(V + E)$ where $V$ is vertices and $E$ is directed edges. Computing in-degrees takes $O(V + E)$, and each vertex/edge is queued and examined once.
- **Space Complexity:** $O(V + E)$ for adjacency list, $O(V)$ for `inDegree` vector and BFS queue.
