# Lecture 133: Bridge in Graph using Tarjan's Algorithm (LeetCode 1192)

> **One-Line Purpose:** Detect all critical "bridge" edges whose deletion increases the number of connected components in $O(V + E)$ time using DFS discovery time (`tin`) and lowest reachable time (`low`).

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #133  
> **Video ID:** `6h1SucBNxgc`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=6h1SucBNxgc)  
> **Duration:** 32:36  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Understand the definition of a "Bridge" (Critical Connection) in an undirected graph.
- Differentiate between a tree-edge and a back-edge in DFS traversals.
- Master the `tin` (Time of Insertion) and `low` (Lowest reachable time) array technique.
- Apply Tarjan's bridge condition: `low[v] > tin[u]`.

---

## 🧠 Core Intuition — Why This Works

A bridge is an edge that is the ONLY way to reach a certain part of the graph. If you cut a bridge, the graph splits into two pieces.
How do we know an edge `(u, v)` is the ONLY way to reach `v`'s territory from `u`?
Because if there was another way, `v` (or some node deeper than `v`) would have a "back-edge" pointing back to `u` or an ancestor of `u`.

**Tarjan's Concept (`tin` and `low`):**
- `tin[u]`: A timestamp. What time did DFS first arrive at node `u`?
- `low[u]`: The lowest `tin` timestamp reachable from `u` (including its descendants) using *at most one back-edge*.

**The Bridge Condition:** `low[v] > tin[u]`
When we are at `u` and we send DFS down edge `(u, v)`. When DFS for `v` finishes, we check `v`'s `low` value.
If `low[v] > tin[u]`, it means the deepest/earliest node `v` could reach back to was still *after* `u` was discovered. Meaning, `v` could NOT reach back to `u` or above `u`. Therefore, the edge `(u, v)` was a one-way ticket. It is a bridge!

**ASCII Visualization:**
```text
  (0)        tin[0]=1, low[0]=1
 /   \
(1)---(2)    tin[1]=2, tin[2]=3. They form a cycle. low[1]=1, low[2]=1.
 |
(3)          tin[3]=4, low[3]=4.
```
For edge `(1, 3)`: `u=1`, `v=3`. `tin[1]=2`. `low[3]=4`.
Since `4 > 2`, `(1,3)` is a bridge! There is no back-edge from 3 to 0, 1, or 2.

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Critical Connections"**: Direct keyword for bridges.
- **"Vulnerability in a network"**: Finding single points of failure in servers, roads, or wiring.
- **"Removing an edge disconnects the graph"**: Literal definition of a bridge.

---

## 📐 Algorithm Walk-Through

1. **Initialization**:
   - `timer = 0`.
   - `tin` and `low` arrays size $V$, initialized to $-1$.
   - `visited` array initialized to `false`.
2. **DFS Traversal**:
   - For every unvisited node, call `dfs(i, -1)`. (Parent is -1 initially).
3. **Inside DFS(`u`, `parent`)**:
   - Mark `visited[u] = true`.
   - Assign `tin[u] = low[u] = ++timer`.
   - Iterate through neighbors `v` of `u`:
     - **Skip Parent**: If `v == parent`, `continue`. (We don't want to immediately turn around and call the edge we just came down a "back-edge").
     - **Back-Edge found** (`visited[v] == true`):
       - `low[u] = min(low[u], tin[v])`. (Update lowest reachable time).
     - **Tree-Edge found** (`visited[v] == false`):
       - Call `dfs(v, u)`.
       - When it returns, update `low[u] = min(low[u], low[v])`. (Propagate the lowest reachable time up the tree).
       - **Bridge Check**: If `low[v] > tin[u]`, push `{u, v}` to results!

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

class TarjanBridges {
private:
    int timer;
    void dfs(int u, int parent, vector<vector<int>>& adj, vector<int>& tin,
             vector<int>& low, vector<bool>& visited, vector<vector<int>>& bridges) {
        visited[u] = true;
        tin[u] = low[u] = ++timer;

        for (int v : adj[u]) {
            if (v == parent) continue; // Skip trivial reverse edge to parent

            if (visited[v]) {
                // Back-edge found: v is already visited and is not the parent.
                // It's a path back to an ancestor.
                low[u] = min(low[u], tin[v]);
            } else {
                // Tree-edge: standard DFS traversal
                dfs(v, u, adj, tin, low, visited, bridges);
                
                // Upon return, u can reach whatever v can reach
                low[u] = min(low[u], low[v]);

                // Bridge Condition
                if (low[v] > tin[u]) {
                    bridges.push_back({u, v});
                }
            }
        }
    }

public:
    vector<vector<int>> criticalConnections(int n, vector<vector<int>>& connections) {
        vector<vector<int>> adj(n);
        for (const auto& e : connections) {
            adj[e[0]].push_back(e[1]);
            adj[e[1]].push_back(e[0]); // Undirected graph
        }

        vector<int> tin(n, -1), low(n, -1);
        vector<bool> visited(n, false);
        vector<vector<int>> bridges;
        timer = 0;

        // Loop handles disconnected graph components
        for (int i = 0; i < n; ++i) {
            if (!visited[i]) {
                dfs(i, -1, adj, tin, low, visited, bridges);
            }
        }
        return bridges;
    }
};

int main() {
    TarjanBridges solver;
    // Cycle (0-1-2) with a bridge to 3 (1-3)
    vector<vector<int>> edges = {{0, 1}, {1, 2}, {2, 0}, {1, 3}};
    auto bridges = solver.criticalConnections(4, edges);

    cout << "Bridges in graph:\n";
    for (const auto& b : bridges) {
        cout << b[0] << " -- " << b[1] << endl; // Output: 1 -- 3
    }
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Graph:** `0-1`, `1-2`, `2-0`, `1-3`.

1. **DFS(0, parent=-1)**: `tin[0]=1, low[0]=1`. Neighbors of 0: `1, 2`.
2. -> Visit **1**. **DFS(1, parent=0)**: `tin[1]=2, low[1]=2`. Neighbors of 1: `0, 2, 3`.
   - Neighbor `0`: is parent. Skip.
3. -> Visit **2**. **DFS(2, parent=1)**: `tin[2]=3, low[2]=3`. Neighbors of 2: `1, 0`.
   - Neighbor `1`: is parent. Skip.
   - Neighbor `0`: is visited! (Back-edge). `low[2] = min(3, tin[0]=1) = 1`.
   - Return to 1.
4. Back at 1. `low[1] = min(low[1]=2, low[2]=1) = 1`.
   - Bridge check `(1, 2)`: `low[2]=1 > tin[1]=2`? False. Not a bridge.
5. -> Visit **3**. **DFS(3, parent=1)**: `tin[3]=4, low[3]=4`. Neighbors of 3: `1`.
   - Neighbor `1`: is parent. Skip.
   - Return to 1.
6. Back at 1. `low[1] = min(low[1]=1, low[3]=4) = 1`.
   - Bridge check `(1, 3)`: `low[3]=4 > tin[1]=2`? **TRUE!** -> Add `[1, 3]` to bridges.
7. Return to 0. `low[0] = min(1, low[1]=1) = 1`.
   - Bridge check `(0, 1)`: `low[1]=1 > tin[0]=1`? False.

**Result:** `[[1, 3]]`.

---

## ⚠️ Common Interview Mistakes

1. **Using `low[v]` instead of `tin[v]` on Back-edges**: When a back-edge `(u, v)` is found, you MUST do `low[u] = min(low[u], tin[v])`. Doing `min(low[u], low[v])` is mathematically incorrect in Tarjan's for articulation points (though it happens to skate by for bridges, it's a terrible habit and conceptually wrong. The definition is "reachable via at most ONE back edge").
2. **Forgetting `v == parent` skip**: In an undirected graph, every edge goes both ways. If you just came from `A` to `B`, looking at `A` from `B` is not a cycle/back-edge. It's the exact same edge. You must `continue`.
3. **Graph Initialization**: LeetCode provides `connections` as an edge list. You must build the `adj` list yourself, ensuring you push edges in BOTH directions `adj[u].push_back(v)` and `adj[v].push_back(u)`.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(V + E)$. We visit every vertex exactly once, and inspect every edge exactly twice (once from each side).
- **Space Complexity:** $O(V + E)$ to store the adjacency list, plus $O(V)$ for `tin`, `low`, `visited` arrays, and the recursion stack.

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Does the order of DFS (which neighbor we pick first) affect the `tin` and `low` values?
**Answer:** Yes, the absolute values of `tin` and `low` will change drastically depending on neighbor traversal order. However, the *relative mathematical property* `low[v] > tin[u]` is an invariant. It will always correctly identify bridges regardless of DFS order.

### Q2: How does this differ from Kosaraju's Algorithm?
**Answer:** Kosaraju's finds Strongly Connected Components (SCCs) in a *Directed* graph using a two-pass DFS. Tarjan's Bridge algorithm works on *Undirected* graphs using a single-pass DFS. (Note: Tarjan also has an SCC algorithm for directed graphs, which is different from this bridge algorithm).

### Q3: What if the graph is disconnected to begin with?
**Answer:** The algorithm handles this flawlessly because of the outer `for` loop in `criticalConnections`. It will run a fresh DFS for every disconnected component. Bridges within those components will be correctly identified.

### Q4: Can an edge be a bridge if it is part of a cycle?
**Answer:** No. By definition, a cycle provides at least two different paths between any two nodes in that cycle. Removing any single edge in a cycle leaves the other path intact. Hence, no edge in a cycle can ever be a bridge.

### Q5: How would you find Articulation Points (Cut Vertices) using this?
**Answer:** Very similar logic! Instead of `low[v] > tin[u]`, the check for articulation points is `low[v] >= tin[u]` (with a special case for the root of the DFS tree needing > 1 child).

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 1192: Critical Connections in a Network](https://leetcode.com/problems/critical-connections-in-a-network/)** — The exact problem solved by this algorithm.
2. **[Leetcode 1489: Find Critical and Pseudo-Critical Edges in MST](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/)** — Bridges play a huge role here. An edge is critical in an MST if its removal disconnects the graph or forces a higher total cost.

---

## 🔗 Cross-Topic Connections
- **Articulation Points:** The sister algorithm to Bridges. Both rely on `tin` and `low` arrays.
- **Biconnected Components:** A graph without any articulation points is biconnected. Understanding bridges is step one to biconnectivity.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Find edges that, if deleted, disconnect the graph.
- **Data Structures:** `tin` (discovery time), `low` (lowest reachable discovery time).
- **Back-Edge Update:** If `v` visited and `v != parent` $\to$ `low[u] = min(low[u], tin[v])`.
- **Tree-Edge Update:** If `v` unvisited $\to$ `dfs(v, u)`, then `low[u] = min(low[u], low[v])`.
- **Condition:** It's a bridge if `low[v] > tin[u]`.
- **Time/Space:** $O(V + E)$ Time | $O(V + E)$ Space.
