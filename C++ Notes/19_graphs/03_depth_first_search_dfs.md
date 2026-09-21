# Lecture 113: Depth-First Search (DFS) Traversal

> **One-Line Purpose:** Traverse graphs deeply along each branch using recursion / call stack backtracking before unwinding, achieving $O(V + E)$ linear time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #113  
> **Video ID:** `3czYbhac160`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=3czYbhac160)  
> **Duration:** 14:03  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Understanding recursive call-stack unwinding for graph paths.
- Comparison of traversal tree shapes (DFS deep path vs BFS flat level).
- Correct component iteration to handle forest / disconnected graphs.

---

## 🔵 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>

using namespace std;

class DFSGraph {
private:
    int V;
    vector<vector<int>> adj;

    void dfsRecursive(int u, vector<bool>& visited, vector<int>& order) {
        visited[u] = true;
        order.push_back(u);

        for (int v : adj[u]) {
            if (!visited[v]) {
                dfsRecursive(v, visited, order);
            }
        }
    }

public:
    DFSGraph(int vertices) : V(vertices), adj(vertices) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    vector<int> dfsTraversal() {
        vector<bool> visited(V, false);
        vector<int> order;

        for (int i = 0; i < V; ++i) {
            if (!visited[i]) {
                dfsRecursive(i, visited, order);
            }
        }
        return order;
    }
};

int main() {
    DFSGraph g(5);
    g.addEdge(0, 1);
    g.addEdge(0, 2);
    g.addEdge(1, 3);
    g.addEdge(2, 4);

    vector<int> res = g.dfsTraversal();
    cout << "DFS Order: ";
    for (int node : res) cout << node << " ";
    cout << endl;
    return 0;
}
```

---

## 🔍 Trace & Backtracking Mechanics
When visiting node `0`, it descends into `1`, then `3`. Since `3` has no unvisited neighbors, the call stack returns to `1`, then unwinds to `0`, which then branches down to `2` and `4`.
- **Time Complexity:** $O(V + E)$
- **Space Complexity:** $O(V)$ stack space in worst-case linear graph (skewed line graph).

---

## 🧠 Core Intuition — Why This Works

### Real-World Analogy: Exploring a Maze
Imagine navigating a maze. You always walk forward until you hit a dead end. When blocked, you backtrack to the last junction and try the next unexplored passage. DFS is this exact strategy — commit fully to one branch, then systematically unwind.

```
Graph:                  DFS Call Tree:
                        
  0                     dfs(0)
 / \                    ├── dfs(1)
1   2                   │   └── dfs(3)  ← dead end, backtrack
|   |                   └── dfs(2)
3   4                       └── dfs(4)  ← dead end, backtrack

DFS Path:  0 → 1 → 3 (backtrack) → 0 → 2 → 4
Output:    [0, 1, 3, 2, 4]

Call Stack Progression:
[dfs(0)]
[dfs(0), dfs(1)]
[dfs(0), dfs(1), dfs(3)]  ← 3 has no unvisited neighbor
[dfs(0), dfs(1)]           ← return from dfs(3)
[dfs(0)]                   ← return from dfs(1)
[dfs(0), dfs(2)]
[dfs(0), dfs(2), dfs(4)]  ← 4 has no unvisited neighbor
[dfs(0), dfs(2)]           ← return from dfs(4)
[dfs(0)]                   ← return from dfs(2)
[]                         ← return from dfs(0), DONE
```

### The Key Insight: DFS Discovery/Finish Timestamps
In advanced DFS (used in algorithms like Tarjan's and Kosaraju's), each node $u$ gets two timestamps:
- **`disc[u]`** — when DFS first visits $u$ (discovery time)
- **`fin[u]`** — when DFS finishes all descendants of $u$ (finish time)

The relationship: for any ancestor $u$ of $v$: $\text{disc}[u] < \text{disc}[v] < \text{fin}[v] < \text{fin}[u]$ (parenthesis theorem). This nesting structure is what makes DFS powerful for cycle detection, SCC computation, and topological sorting.

---

## 🎯 Pattern Recognition — When to Use DFS

| Problem Cue | Why DFS Fits |
|---|---|
| "All paths from source to destination" | DFS naturally enumerates all paths |
| "Detect cycle in graph" | DFS back-edges directly reveal cycles |
| "Topological sort" | DFS post-order gives reverse topological order |
| "Connected components / Islands" | DFS floods a component completely |
| "Strongly connected components" | Kosaraju's / Tarjan's algorithms use DFS |
| "Maze solving / game tree exploration" | DFS exhausts one path before trying next |
| "Tree problems (preorder/inorder/postorder)" | DFS on trees = traversal orders |

### DFS vs BFS at a Glance
| Property | DFS | BFS |
|---|---|---|
| Data structure | Recursion/Stack (LIFO) | Queue (FIFO) |
| Memory | $O(\text{depth})$ | $O(\text{width})$ |
| Shortest path? | ❌ No | ✅ Yes (unweighted) |
| Cycle detection | ✅ Via back-edge / inStack | ✅ Via parent tracking |
| Topological sort | ✅ Post-order reversal | ✅ Kahn's (in-degree) |
| Natural for | Deep problems, trees, SCCs | Shortest path, levels, spreading |

---

## 📐 Algorithm Walk-Through

**Invariant maintained:** Once `visited[u] = true`, node $u$ is never re-entered. When `dfsRecursive(u, ...)` returns, **all** nodes reachable from $u$ through unvisited paths have been visited.

**Step-by-step for graph `0-1, 0-2, 1-3, 2-4`:**
1. `dfs(0)`: mark 0 visited, output `[0]`
2. Neighbor 1 unvisited → recurse: `dfs(1)`: mark 1 visited, output `[0,1]`
3. Neighbor 3 unvisited → recurse: `dfs(3)`: mark 3 visited, output `[0,1,3]`
4. Neighbor 1 already visited → no recurse. `dfs(3)` returns.
5. `dfs(1)` returns. Back in `dfs(0)`, next neighbor 2 unvisited.
6. `dfs(2)`: mark 2 visited, output `[0,1,3,2]`
7. Neighbor 4 unvisited → `dfs(4)`: mark 4, output `[0,1,3,2,4]`
8. `dfs(4)` returns. `dfs(2)` returns. `dfs(0)` returns.

---

## 💻 Iterative DFS Implementation (Interview Variant)

Recursive DFS can cause stack overflow on large graphs ($V \approx 10^5$). The iterative version uses an explicit stack:

```cpp
#include <iostream>
#include <vector>
#include <stack>
using namespace std;

vector<int> dfsIterative(int src, vector<vector<int>>& adj, int V) {
    vector<bool> visited(V, false);
    vector<int> order;
    stack<int> st;

    st.push(src);

    while (!st.empty()) {
        int u = st.top(); st.pop();

        if (visited[u]) continue; // Skip if already visited
        visited[u] = true;
        order.push_back(u);

        // Push neighbors in reverse order to mimic recursive DFS order
        for (int i = adj[u].size() - 1; i >= 0; --i) {
            if (!visited[adj[u][i]]) {
                st.push(adj[u][i]);
            }
        }
    }
    return order;
}
```

> **Note:** Iterative DFS marks visited on **pop** (unlike BFS which marks on push). This is because the stack may hold stale entries. Alternatively, mark on push and skip duplicates on pop.

---

## ⚠️ Common Interview Mistakes

### 1. Stack Overflow on Deep Recursion
For graphs with $V = 10^5$ nodes in a linear chain, recursive DFS will exceed the default stack size (~1-8 MB). Interviewers may ask you to implement the iterative version.

### 2. Forgetting to Handle Disconnected Components
```cpp
// ❌ WRONG — only visits nodes reachable from vertex 0
dfsRecursive(0, visited, order);

// ✅ CORRECT — handles all components
for (int i = 0; i < V; ++i)
    if (!visited[i]) dfsRecursive(i, visited, order);
```

### 3. Confusing DFS Tree Edge Types
In a DFS of an **undirected** graph, there are only two edge types:
- **Tree edge:** Edge used in DFS traversal (to unvisited node)
- **Back edge:** Edge to an already-visited ancestor (indicates a cycle)

In a **directed** graph, there are four types: tree, back, forward, cross. Only **back edges** indicate cycles.

### 4. Not Passing `visited` by Reference
```cpp
// ❌ WRONG — each recursive call gets its own copy of visited!
void dfs(int u, vector<bool> visited) { ... }

// ✅ CORRECT — shared state across all recursive calls
void dfs(int u, vector<bool>& visited) { ... }
```

### 5. Modifying the Adjacency List During Traversal
Never push/pop from `adj[u]` while iterating over it in DFS. Use a separate variable if the graph is dynamic.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] What are DFS discovery and finish times, and what is the Parenthesis Theorem?

**Answer:** In DFS, we assign two timestamps to every node $u$:
- `disc[u]`: the time when DFS first calls `dfs(u)` — the "opening parenthesis"
- `fin[u]`: the time when `dfs(u)` returns — the "closing parenthesis"

**Parenthesis Theorem:** For any two nodes $u$ and $v$, exactly one of these holds:
1. The intervals $[\text{disc}[u], \text{fin}[u]]$ and $[\text{disc}[v], \text{fin}[v]]$ are completely disjoint → $u$ and $v$ are in different subtrees.
2. One interval is entirely nested inside the other → the node with the larger interval is an **ancestor** of the other.

This theorem is the foundation for classifying DFS edges (tree, back, forward, cross) and is used in Tarjan's SCC algorithm.

### Q2: [Edge Classification] What are the four types of edges in a directed DFS, and which one indicates a cycle?

**Answer:** During DFS of a directed graph, every edge $(u, v)$ is one of:
1. **Tree edge:** $v$ is unvisited when $(u,v)$ is explored. $v$ becomes a child of $u$.
2. **Back edge:** $v$ is an ancestor of $u$ in the DFS tree (`inStack[v] == true`). **This indicates a cycle.**
3. **Forward edge:** $v$ is a descendant of $u$ but already visited (and not in stack). (`disc[u] < disc[v]`)
4. **Cross edge:** $v$ is neither ancestor nor descendant — it's in a completely different DFS subtree already finished. (`disc[v] < disc[u]` and `fin[v] < disc[u]`)

Note: In **undirected** graphs, there are only tree edges and back edges (no forward/cross edges).

### Q3: [Proof] Why does DFS post-order produce a reverse topological ordering for a DAG?

**Answer:** In a DAG, if there's an edge $u \to v$, then $v$ must appear **after** $u$ in topological order. In DFS:
- When we call `dfs(u)`, we recursively call `dfs(v)` for all neighbors $v$.
- `dfs(v)` must **complete** (finish time assigned) before `dfs(u)` can return.
- Therefore: $\text{fin}[v] < \text{fin}[u]$.

When we push nodes onto a stack at finish time, $v$ is pushed before $u$. Popping the stack gives $u$ before $v$ — exactly the topological order where $u$ precedes $v$ (as required by the edge $u \to v$). ∎

### Q4: [Bug Prediction] What does this DFS code output for graph `0-1-2-0` (triangle)?
```cpp
void dfs(int u, vector<vector<int>>& adj, vector<bool>& visited) {
    cout << u << " ";
    for (int v : adj[u])
        if (!visited[v]) {
            visited[v] = true;
            dfs(v, adj, visited);
        }
}
// visited[0] set to true, dfs(0) called
```
**Answer:** Output is `0 1 2`. But there's a subtle bug: `visited[0]` is set to true before calling `dfs(0)`, but the code only marks `visited[v] = true` inside the loop for *children*, not for the root `u` itself. If called from a loop without pre-marking the root, the root would never be marked. The correct pattern: mark `visited[u] = true` at the **start of dfs(u)**.

### Q5: [Extension] How would you use DFS to detect articulation points (cut vertices)?

**Answer:** An articulation point is a vertex whose removal disconnects the graph. Using DFS, we track:
- `disc[u]`: discovery time
- `low[u]`: minimum discovery time reachable from the subtree of $u$ (via back edges)

A vertex $u$ is an articulation point if:
1. $u$ is the DFS root and has ≥ 2 children in the DFS tree.
2. $u$ is not the root and has a child $v$ such that $\text{low}[v] \geq \text{disc}[u]$ (i.e., no back edge from $v$'s subtree reaches above $u$).

This runs in $O(V + E)$ — a beautiful application of DFS timestamps.

### Q6: [Complexity] What is the space complexity of DFS on a complete graph $K_V$ (every vertex connected to every other)?

**Answer:** In $K_V$, DFS from vertex 0 visits all $V$ vertices before backtracking. The maximum depth of the DFS call stack is $V-1$ (a Hamiltonian path in the DFS tree). Space = $O(V)$ for the call stack + $O(V)$ for the visited array = $O(V)$.

The key insight: DFS call stack depth = maximum DFS tree depth, which is at most $V-1$ regardless of the number of edges $E$. Space is $O(V)$, not $O(E)$.

### Q7: [System Design] How would you use DFS to find all SCCs (Strongly Connected Components) via Kosaraju's algorithm?

**Answer:** Kosaraju's algorithm uses two DFS passes:

**Pass 1:** Run DFS on the original graph. Push nodes to a stack in **finish time order** (post-order).

**Pass 2:** Transpose the graph (reverse all edges). Pop nodes from the stack and run DFS on the transposed graph from each unvisited node. Each DFS call in Pass 2 discovers one SCC.

**Why it works:** In the original graph, if node $u$ finishes last (highest finish time), $u$ is the "root" of an SCC that can reach all others. In the transposed graph, following edges from $u$ reaches only nodes in $u$'s own SCC (since original-graph paths are reversed). Each Pass-2 DFS therefore floods exactly one SCC.

Time: $O(V + E)$. Used in compiler dependency analysis and web crawlers.

---

## 🏆 Related LeetCode Problems

| # | Problem | Approach Hint |
|---|---|---|
| 200 | Number of Islands | DFS sinks each island component |
| 133 | Clone Graph | DFS with hash map for node mapping |
| 695 | Max Area of Island | DFS returns component size |
| 417 | Pacific Atlantic Water Flow | Reverse DFS from both ocean borders |
| 207 | Course Schedule | DFS cycle detection with `inStack` array |

---

## 🔗 Cross-Topic Connections

- **Topological Sort:** DFS post-order = reverse topological order for DAGs (File 09).
- **Cycle Detection:** DFS with `inStack` detects directed cycles (File 08); parent tracking detects undirected cycles (File 04).
- **Flood Fill / Islands:** DFS naturally "floods" connected components (Files 06, 12).
- **Kosaraju's SCC:** Two-pass DFS on original + transposed graph.
- **Tarjan's SCC:** Single-pass DFS with `low` values — more efficient than Kosaraju's.
- **Bridges & Articulation Points:** DFS with `disc` and `low` arrays.
- **BFS vs DFS trade-off:** BFS = shortest path; DFS = deep structural properties.

---

## ⚡ 2-Minute Revision Flash Card

- **DFS uses the call stack (recursion) or an explicit stack** — mark `visited[u] = true` at the **start** of `dfs(u)`.
- **Two key timestamps:** `disc[u]` (entry) and `fin[u]` (exit) — Parenthesis Theorem nests ancestors around descendants.
- **Post-order push** to a stack → pop gives topological order for DAGs.
- **Back edge = cycle** in directed graphs; in undirected graphs, visiting a non-parent visited node = cycle.
- **Time & Space:** $O(V + E)$ time; $O(V)$ stack depth — but may overflow for $V \approx 10^5$; use iterative DFS.
