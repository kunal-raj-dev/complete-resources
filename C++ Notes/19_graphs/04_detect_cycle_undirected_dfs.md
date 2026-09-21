# Lecture 114: Detect Cycle in Undirected Graph using DFS

> **One-Line Purpose:** Detect cycles in undirected graphs by tracking the immediate parent vertex; encountering an already-visited non-parent neighbor confirms a back-edge and hence a cycle.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #114  
> **Video ID:** `OZClCpPQDR4`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=OZClCpPQDR4)  
> **Duration:** 19:45  
> **Status:** AUDITED  

---

## 🔵 Core Algorithmic Invariant
In an undirected graph, edge $(u, v)$ means $v$ can trivially go back to $u$. This trivial reversal is NOT a cycle.
A real cycle exists **if and only if** we reach an already visited neighbor $v$ such that $v \neq \text{parent}$.

```
    0 ----- 1
    |       |
    |       |
    3 ----- 2
DFS path: 0 -> 1 -> 2 -> 3. From 3, neighbor 0 is visited and 0 != parent (2) => CYCLE DETECTED!
```

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>

using namespace std;

class UndirectedCycleDFS {
private:
    int V;
    vector<vector<int>> adj;

    bool dfsCheck(int u, int parent, vector<bool>& visited) {
        visited[u] = true;

        for (int neighbor : adj[u]) {
            if (!visited[neighbor]) {
                if (dfsCheck(neighbor, u, visited)) return true;
            } else if (neighbor != parent) {
                // Visited neighbor that is not our direct parent => Back Edge!
                return true;
            }
        }
        return false;
    }

public:
    UndirectedCycleDFS(int vertices) : V(vertices), adj(vertices) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    bool hasCycle() {
        vector<bool> visited(V, false);
        for (int i = 0; i < V; ++i) {
            if (!visited[i]) {
                if (dfsCheck(i, -1, visited)) return true;
            }
        }
        return false;
    }
};

int main() {
    UndirectedCycleDFS g(4);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(2, 3);
    g.addEdge(3, 0);

    cout << "Cycle present: " << (g.hasCycle() ? "YES" : "NO") << endl;
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(V + E)$
- **Space Complexity:** $O(V)$ call stack + visited array.

---

## 🧠 Core Intuition — Why This Works

### Real-World Analogy: Leaving Breadcrumbs
Imagine walking through a forest, leaving breadcrumbs on every path you visit. If you ever reach a spot that already has breadcrumbs — and it wasn't the spot you just came from — you've walked in a circle. The "parent" exclusion accounts for the fact that the path you came from will always look like a "visited neighbor" in an undirected graph (since edges go both ways).

```
No Cycle Graph (Tree):        Cycle Graph:
                              
  0 --- 1 --- 3               0 --- 1
        |                     |     |
        2                     3 --- 2

DFS from 0:                   DFS from 0:
  visit(0, parent=-1)           visit(0, parent=-1)
  visit(1, parent=0)            visit(1, parent=0)
  visit(3, parent=1)            visit(2, parent=1)
    neighbor 1 = parent → skip    visit(3, parent=2)
  visit(2, parent=1)              neighbor 0: visited AND 0 != parent(2)
    neighbors: 1 (parent, skip)   → CYCLE DETECTED ✓
  No back edge found → NO CYCLE
```

### Key Insight: Why Parent Tracking (Not Just Visited) is Needed
In an undirected graph, every edge $u-v$ creates **two directed arcs**: $u \to v$ and $v \to u$. When DFS visits $v$ from $u$, the arc $v \to u$ immediately looks like a "back edge to a visited node." Without parent tracking, we'd falsely detect a cycle everywhere. The parent check filters out this trivial reflection.

**What about multi-edges?** If there are two edges between $u$ and $v$ (multigraph), the parent check by node ID fails — we'd miss the second parallel edge. The fix: track `parentEdgeIndex` instead of `parentNode`. See the Common Interview Mistakes section.

---

## 🎯 Pattern Recognition — When to Use This Algorithm

| Signal | Algorithm |
|---|---|
| "Does this undirected graph have a cycle?" | DFS with parent tracking (this file) |
| "Does this directed graph have a cycle?" | DFS with `inStack` array (File 08) |
| "Can all courses be taken?" | Directed cycle detection → Kahn's / DFS inStack |
| "Is this graph a tree?" | Tree iff connected AND no cycle (V-1 edges + no cycle) |
| "Find if graph is bipartite" | BFS/DFS 2-coloring (fails if odd cycle exists) |

### DFS Cycle (Undirected) vs DFS Cycle (Directed)
| Property | Undirected | Directed |
|---|---|---|
| Extra state needed | `parent` node | `inStack[]` boolean array |
| Back edge condition | `visited[v] && v != parent` | `visited[v] && inStack[v]` |
| Edge traversal | Both directions natural | One direction only |
| Why different? | Trivial reversal is NOT a cycle | Cross/forward edges exist; only back edges = cycle |

---

## 📐 Algorithm Walk-Through

**Invariant:** When `dfsCheck(u, parent, visited)` is called, `visited[u]` is set to `true` immediately. For every neighbor `w` of `u`: if `w` is unvisited, recurse into it. If `w` is visited and `w != parent`, a back-edge exists → cycle.

**Concrete trace on cycle graph `0-1-2-3-0`:**
```
Call: dfsCheck(0, -1, visited)
  visited[0] = true
  Neighbor 1: unvisited → dfsCheck(1, 0, visited)
    visited[1] = true
    Neighbor 0: visited, but 0 == parent(0) → SKIP
    Neighbor 2: unvisited → dfsCheck(2, 1, visited)
      visited[2] = true
      Neighbor 1: visited, but 1 == parent(1) → SKIP
      Neighbor 3: unvisited → dfsCheck(3, 2, visited)
        visited[3] = true
        Neighbor 2: visited, but 2 == parent(2) → SKIP
        Neighbor 0: visited, 0 != parent(2) → CYCLE! return true
```

---

## ⚠️ Common Interview Mistakes

### 1. Forgetting to Handle Disconnected Graphs
```cpp
// ❌ Only checks one component
if (dfsCheck(0, -1, visited)) return true;

// ✅ Must check all components
for (int i = 0; i < V; ++i)
    if (!visited[i] && dfsCheck(i, -1, visited)) return true;
```

### 2. Parent Check Fails for Multigraphs
If there are two parallel edges between $u$ and $v$, the DFS will see $v$'s "other edge back to $u$" and think it found a cycle — but the same parent check by node ID will prevent detecting the second edge.

```cpp
// ❌ Fails for multigraph: 0==(two edges)==1
// When at 1 (parent=0), adj[1] = [0, 0]
// First 0: visited && 0 == parent → skip
// Second 0: visited && 0 == parent → skip (MISS! should detect cycle)

// ✅ Fix: Track parentEdgeIndex
bool dfsCheck(int u, int parentEdge, vector<bool>& visited,
              vector<vector<pair<int,int>>>& adj) {
    visited[u] = true;
    for (auto [v, edgeIdx] : adj[u]) {
        if (!visited[v]) {
            if (dfsCheck(v, edgeIdx, visited, adj)) return true;
        } else if (edgeIdx != parentEdge) {
            return true; // True back edge, not trivial reversal
        }
    }
    return false;
}
```

### 3. Using `visited` Instead of `parent` for Cycle Detection
```cpp
// ❌ WRONG for undirected graphs — always detects false cycle
bool dfsCheck(int u, vector<bool>& visited) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (visited[v]) return true; // False! This fires on the parent too
        dfsCheck(v, visited);
    }
    return false;
}
```

### 4. Stack Overflow on Dense Graphs
For $V = 10^5$ in a path graph, recursion depth = $V$. Use iterative DFS for production code.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Why does the parent-tracking condition `neighbor != parent` work for cycle detection in undirected graphs?

**Answer:** In an undirected graph, every edge $(u, v)$ is stored in both `adj[u]` (as $v$) and `adj[v]` (as $u$). When DFS visits $v$ from $u$, the edge $v \to u$ appears as a "visited neighbor" immediately. Without parent filtering, this trivial reversal would always trigger a false cycle detection.

The parent check `neighbor != parent` filters out this one guaranteed "visited but not a real back-edge" case. Any **other** visited neighbor (that isn't the direct parent) must be a genuinely distinct ancestor in the DFS tree — meaning DFS reached it via a completely different path, forming a cycle.

### Q2: [Edge Case] Does the algorithm work correctly for a self-loop edge `(u, u)`?

**Answer:** Yes, with a subtle observation: when processing neighbors of $u$, we encounter $u$ itself as a neighbor. Since `visited[u] = true` (set at function entry) and `u != parent (-1 or some other node)`, the condition `visited[u] && u != parent` evaluates to `true`, correctly detecting the self-loop as a cycle.

However, if you initialize `parent = u` (by mistake), self-loops would be missed. Always initialize parent as `-1` for the root.

### Q3: [Bug Prediction] What happens if you forget to pass `parent` and always use `parent = -1`?
```cpp
bool dfsCheck(int u, vector<bool>& visited) {
    visited[u] = true;
    for (int neighbor : adj[u]) {
        if (!visited[neighbor]) {
            if (dfsCheck(neighbor, visited)) return true; // No parent passed!
        } else {
            return true; // WRONG: fires on the parent!
        }
    }
    return false;
}
```
**Answer:** This would return `true` (cycle detected) for **every edge** in the graph, even in a simple tree. When DFS visits $v$ from $u$, $u$ is already visited. Without the parent check, seeing $u$ as a visited neighbor immediately returns `true`. The graph `0-1` (a single edge, no cycle) would incorrectly report a cycle.

### Q4: [Extension] How would you modify this to not just detect but also print the cycle?

**Answer:** Track the DFS path using a `path` vector and a `pathIndex` array that stores each node's position in the current path:

```cpp
bool dfsCheck(int u, int parent, vector<bool>& visited,
              vector<int>& path, vector<int>& pathPos) {
    visited[u] = true;
    pathPos[u] = path.size();
    path.push_back(u);

    for (int v : adj[u]) {
        if (!visited[v]) {
            if (dfsCheck(v, u, visited, path, pathPos)) return true;
        } else if (v != parent) {
            // Print cycle from v to u via path
            cout << "Cycle: ";
            for (int i = pathPos[v]; i < path.size(); ++i)
                cout << path[i] << " ";
            cout << v << endl;
            return true;
        }
    }

    path.pop_back();
    return false;
}
```

### Q5: [Conceptual] What is the relationship between "graph has a cycle" and "graph is a tree"?

**Answer:** An undirected connected graph is a **tree** if and only if:
1. It has exactly $V - 1$ edges, AND
2. It is connected (or equivalently, has no cycles).

Any two of these three properties (connected, $V-1$ edges, acyclic) imply the third. So:
- Connected + $V-1$ edges → no cycle (it's a tree).
- Connected + has cycle → more than $V-1$ edges.
- Acyclic + $V-1$ edges → connected (spanning tree).

In interviews, the cycle detection algorithm above can verify the "acyclic" condition. Combined with a connectivity check, you can verify if a graph is a tree.

### Q6: [Comparison] When would you prefer BFS-based cycle detection (File 05) over DFS-based (this file)?

**Answer:** Both are $O(V + E)$ and equally correct. Preference depends on context:
- **DFS** is natural when you're already using DFS for other purposes (e.g., also computing DFS tree, SCC, etc.). Recursion is concise.
- **BFS** avoids stack overflow risk for large graphs since it's iterative. If $V = 10^6$, BFS is safer.
- **DFS** is preferred when you need to find and print the actual cycle (path tracking is straightforward in DFS).
- **BFS** with `(node, parent)` pairs in the queue is conceptually simpler for some people to reason about in interviews.

### Q7: [Proof] Prove that in an undirected graph, a cycle exists if and only if DFS finds a back edge.

**Answer:**
**($\Rightarrow$) If a cycle exists, DFS finds a back edge:**
Let $v_1 - v_2 - \cdots - v_k - v_1$ be a cycle. DFS enters this cycle at some vertex $v_i$. It follows the cycle path until it reaches $v_j$ whose neighbor $v_i$ is already visited (and $v_i \neq \text{parent}(v_j)$). This is a back edge.

**($\Leftarrow$) If DFS finds a back edge, a cycle exists:**
A back edge $(u, v)$ means $v$ is an ancestor of $u$ in the DFS tree. The DFS tree path from $v$ to $u$ plus the edge $(u, v)$ forms a cycle. ∎

---

## 🏆 Related LeetCode Problems

| # | Problem | Approach Hint |
|---|---|---|
| 684 | Redundant Connection | Find the extra edge creating a cycle (Union-Find or DFS) |
| 261 | Graph Valid Tree | Check connected + acyclic (DFS cycle detection) |
| 785 | Is Graph Bipartite? | DFS 2-coloring; odd cycle means non-bipartite |
| 207 | Course Schedule | Directed cycle detection (use `inStack`, not parent) |
| 323 | Number of Connected Components | DFS/Union-Find to count components |

---

## 🔗 Cross-Topic Connections

- **DFS (File 03):** Cycle detection is DFS with extra `parent` tracking — build on the base DFS pattern.
- **BFS Cycle Detection (File 05):** Same problem, iterative BFS flavor — tracks `(node, parent)` pairs in queue.
- **Directed Cycle Detection (File 08):** Replace `parent` with `inStack[]` for directed graphs.
- **Union-Find (DSU):** Alternative $O(\alpha(V))$ per query approach — when two nodes in the same edge share the same root, a cycle is found.
- **Topological Sort:** Only applicable to DAGs — cycle detection is a prerequisite.
- **Bipartiteness:** An undirected graph is bipartite iff it has **no odd-length cycle** — tested via 2-coloring DFS.

---

## ⚡ 2-Minute Revision Flash Card

- **Condition for cycle:** `visited[neighbor] == true && neighbor != parent` → back edge found → cycle.
- **Why parent tracking?** Undirected edges appear in both directions; the trivial reversal must be excluded.
- **Multi-edge graphs** require tracking `parentEdgeIndex`, not just `parentNode`.
- **Always loop over all components:** `for (int i=0; i<V; ++i) if (!visited[i]) dfsCheck(i, -1, ...)`.
- **Time & Space:** $O(V + E)$ time; $O(V)$ space for visited array and recursion stack.
