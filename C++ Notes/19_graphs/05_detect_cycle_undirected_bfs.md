# Lecture 115: Detect Cycle in Undirected Graph using BFS

> **One-Line Purpose:** Detect cycles using BFS by enqueuing `(currentNode, parentNode)` pairs; visiting an already-visited non-parent indicates a cross-edge cycle.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #115  
> **Video ID:** `MIjOkApZ39g`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=MIjOkApZ39g)  
> **Duration:** 18:23  
> **Status:** AUDITED  

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <queue>

using namespace std;

class UndirectedCycleBFS {
private:
    int V;
    vector<vector<int>> adj;

    bool bfsCheck(int src, vector<bool>& visited) {
        // queue stores pair of <current_node, parent_node>
        queue<pair<int, int>> q;
        visited[src] = true;
        q.push({src, -1});

        while (!q.empty()) {
            auto [u, parent] = q.front();
            q.pop();

            for (int neighbor : adj[u]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    q.push({neighbor, u});
                } else if (neighbor != parent) {
                    return true; // Cross edge found
                }
            }
        }
        return false;
    }

public:
    UndirectedCycleBFS(int vertices) : V(vertices), adj(vertices) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    bool hasCycle() {
        vector<bool> visited(V, false);
        for (int i = 0; i < V; ++i) {
            if (!visited[i]) {
                if (bfsCheck(i, visited)) return true;
            }
        }
        return false;
    }
};

int main() {
    UndirectedCycleBFS g(3);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(2, 0);

    cout << "Cycle present: " << (g.hasCycle() ? "YES" : "NO") << endl;
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(V + E)$
- **Space Complexity:** $O(V)$ queue and visited array.

---

## 🧠 Core Intuition — Why This Works

### Real-World Analogy: Exploring a City Block by Block
Imagine exploring a city. You send search parties outward from your starting point, block by block (BFS layers). Each search party member knows who sent them (their "parent"). If a search party arrives at a city block already visited by **someone else's party** (not their own sender), they've found a shortcut — a cycle.

```
Cycle Graph: 0 - 1 - 2 - 0 (triangle)

BFS from node 0:
  Queue: [(0, -1)]   visited: {0}

  Pop (0, -1):
    Neighbor 1: unvisited → push (1, 0), mark visited
    Neighbor 2: unvisited → push (2, 0), mark visited
  Queue: [(1,0), (2,0)]   visited: {0,1,2}

  Pop (1, 0):
    Neighbor 0: visited, 0 == parent → SKIP (trivial reversal)
    Neighbor 2: visited, 2 != parent(0) → CYCLE DETECTED! ✓

No Cycle Graph: 0 - 1 - 2 (path)

  Pop (0, -1): push (1, 0)
  Pop (1, 0): neighbor 0 == parent → skip; push (2, 1)
  Pop (2, 1): neighbor 1 == parent → skip
  Queue empty → NO CYCLE ✓
```

### The Key Insight: Pairing Every Node with Its BFS Parent
Unlike regular BFS where we only track `visited[]`, cycle detection BFS tracks `(node, parent)` pairs in the queue. This is necessary because:
- When node $v$ is visited, its neighbor $u$ (its BFS parent) is already marked visited.
- Without the parent field, we'd trigger a false cycle on every edge.
- The parent field acts as the "direction we came from" filter.

---

## 🎯 Pattern Recognition — When to Use This Algorithm

**Use BFS cycle detection when:**
- You need an **iterative** (non-recursive) cycle check — avoids stack overflow for large $V$.
- The graph is undirected and you're already computing BFS distances.
- Interviewer specifically asks for BFS approach.

**Use DFS cycle detection (File 04) when:**
- You're already building a DFS framework for other purposes.
- You need to **print the actual cycle** (path tracking is simpler with DFS).

**Use Union-Find (DSU) when:**
- You're processing edges one by one (online cycle detection).
- You need the fastest per-query performance: $O(\alpha(V))$ amortized.

### Cycle Detection Algorithm Comparison
| Method | Time | Space | Recursive? | Finds cycle path? |
|---|---|---|---|---|
| DFS + parent | $O(V+E)$ | $O(V)$ | Yes | Yes (with path array) |
| BFS + parent pair | $O(V+E)$ | $O(V)$ | No | Harder |
| Union-Find | $O(E \cdot \alpha(V))$ | $O(V)$ | No | No |

---

## 📐 Algorithm Walk-Through

**Step-by-step for graph with 4 nodes `0-1, 1-2, 2-3, 3-0` (square):**

| Step | Queue | Visited | Action |
|---|---|---|---|
| Init | `[(0,-1)]` | `{0}` | Push source with parent -1 |
| Pop `(0,-1)` | `[(1,0),(3,0)]` | `{0,1,3}` | Neighbors 1,3 unvisited → enqueue |
| Pop `(1,0)` | `[(3,0),(2,1)]` | `{0,1,2,3}` | Neighbor 0 = parent → skip; 2 unvisited → enqueue |
| Pop `(3,0)` | `[(2,1)]` | `{0,1,2,3}` | Neighbor 0 = parent → skip; neighbor 2: **visited AND 2 ≠ parent(0)** → **CYCLE!** |

Result: **CYCLE DETECTED** ✓

---

## ⚠️ Common Interview Mistakes

### 1. Storing Only Node (Not Parent) in Queue
```cpp
// ❌ WRONG — can't determine parent during BFS pop
queue<int> q;  // No parent info!
q.push(src);
// ...
for (int neighbor : adj[u]) {
    if (visited[neighbor]) return true; // FALSE POSITIVE everywhere!
}
```
**Fix:** Always store `pair<int,int>` (node, parent) or maintain a separate `parent[]` array.

### 2. Using a Separate `parent[]` Array (Subtle Bug)
```cpp
// ⚠️ Works but has a subtle issue for disconnected graphs
vector<int> parent(V, -1);
// ...
// parent[u] is set when u is pushed, not when it's popped
// For disconnected graphs, multiple BFS calls reuse the same array — OK if initialized fresh
```
The `pair<int,int>` in the queue approach is cleaner and self-contained.

### 3. Checking `neighbor != parent` with Node ID (Fails for Multigraphs)
Same as DFS approach — if two parallel edges exist between $u$ and $v$, the second edge would be invisible. Fix: store edge indices.

### 4. Not Handling Disconnected Graphs
```cpp
// ❌ WRONG — only checks one component
bfsCheck(0, visited);

// ✅ CORRECT
for (int i = 0; i < V; ++i)
    if (!visited[i] && bfsCheck(i, visited)) return true;
```

### 5. Marking Visited After Pop (Queue Bloat)
Same as regular BFS — mark `visited[neighbor] = true` **before** pushing to queue, not after popping.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Why does BFS-based cycle detection store `(node, parent)` pairs instead of just using a `parent[]` array?

**Answer:** Both approaches work, but they have a subtle difference in multi-component graphs:

**`parent[]` array approach:** Requires resetting or reinitializing for each BFS call on disconnected components, or carefully ensuring previous components' parent values don't interfere.

**`(node, parent)` pair in queue approach:** The parent information is self-contained within each queue entry. When we pop `(u, p)`, we know exactly who `p` is for this specific traversal context, regardless of other BFS calls. This is more robust and avoids the "stale parent" bug.

In interviews, the `pair<int,int>` approach is preferred for clarity.

### Q2: [Comparison] BFS vs DFS for cycle detection in undirected graphs — which is better?

**Answer:** Both are $O(V + E)$ time and $O(V)$ space. The differences are:

- **Stack overflow risk:** DFS is recursive (unless iterative), so for $V = 10^5$ in a path graph, it overflows. BFS is iterative and safe.
- **Finding cycle path:** DFS naturally tracks the current path. BFS would need extra bookkeeping to reconstruct the cycle.
- **Code simplicity:** DFS is slightly more compact. BFS queue with pairs is more explicit.
- **Practical preference:** For coding interviews, both are acceptable. For production on large graphs, BFS is safer.

### Q3: [Proof] Prove that BFS-based cycle detection is correct — i.e., it returns true iff a cycle exists.

**Answer:**
**($\Rightarrow$) If a cycle exists, BFS detects it:**
Let $C = v_1 - v_2 - \cdots - v_k - v_1$ be a cycle. BFS will eventually process all nodes on $C$. Consider the BFS tree: some node $v_i$ on the cycle will have a BFS tree edge to $v_{i+1}$. The "return edge" $v_k - v_1$ is a non-tree edge connecting two already-visited nodes where $v_1 \neq \text{parent}(v_k)$ in the BFS tree. This triggers the condition. ∎

**($\Leftarrow$) If BFS detects a cycle, one exists:**
BFS returns `true` only when it finds a `neighbor` that is (1) already visited and (2) not the current node's parent. The already-visited neighbor was discovered via a completely different BFS path. The current path from source to `u` plus the edge `u - neighbor` plus the BFS path from source to `neighbor` forms a cycle. ∎

### Q4: [Bug Prediction] What does this code output for graph `0-1, 1-2` (path, no cycle)?
```cpp
bool bfsCheck(int src, vector<bool>& visited) {
    queue<int> q;  // Only stores node, NOT parent!
    visited[src] = true;
    q.push(src);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (!visited[v]) {
                visited[v] = true;
                q.push(v);
            } else {
                return true; // No parent check!
            }
        }
    }
    return false;
}
```
**Answer:** Returns `true` (falsely reports a cycle) for the path `0-1-2`. When processing node 1, neighbor 0 is already visited. Without the parent check, `else { return true; }` fires immediately. Output: `Cycle present: YES` — **WRONG**. The path `0-1-2` has no cycle.

### Q5: [Extension] How would you use BFS cycle detection to find if a graph is a valid tree?

**Answer:** A connected undirected graph is a tree if and only if it has no cycle. Algorithm:
1. Run BFS from any node. Track if `hasCycle()` returns false.
2. Also verify all $V$ nodes were visited (graph is connected).
3. If both conditions hold → it's a tree.

```cpp
bool isTree(int V, vector<vector<int>>& adj) {
    vector<bool> visited(V, false);
    if (bfsCheck(0, visited)) return false;  // Has cycle
    for (int i = 0; i < V; ++i)
        if (!visited[i]) return false;  // Disconnected
    return true;
}
```

Alternative: A tree has exactly $V-1$ edges. Check edge count + connectivity.

### Q6: [Complexity Deep-Dive] Why is the space complexity $O(V)$ and not $O(V + E)$ for BFS cycle detection?

**Answer:** The BFS queue holds at most $V$ entries at any time. Even though there are $E$ edges, each node is enqueued **at most once** (because we mark `visited[neighbor] = true` before enqueueing). So the queue size is bounded by $V$, not $E$.

The visited array is $O(V)$. The `parent` information is stored per queue entry (pair), so it's also bounded by $V$ queue entries. Total: $O(V)$.

This is different from the adjacency list storage itself, which is $O(V + E)$ — but that's input space, not algorithm space.

### Q7: [Advanced] Can you detect cycles in a directed graph using BFS with the parent-pair technique?

**Answer:** **No, not directly.** The parent-pair technique is specific to undirected graphs because it exploits the fact that every undirected edge creates a trivial "back edge" that must be filtered.

In directed graphs, an edge $u \to v$ does NOT create a corresponding edge $v \to u$. So BFS won't encounter the trivial back-edge problem. However, BFS on a directed graph cannot distinguish between cross edges and back edges (both are already-visited nodes). BFS would miss cycles reachable only via directed paths.

For directed cycle detection, use:
- **DFS with `inStack[]`** (File 08) — detects back edges correctly.
- **Kahn's algorithm** — if `topoOrder.size() < V`, a cycle exists (File 13).

---

## 🏆 Related LeetCode Problems

| # | Problem | Approach Hint |
|---|---|---|
| 261 | Graph Valid Tree | BFS cycle detection + connectivity check |
| 684 | Redundant Connection | Find extra edge — use Union-Find or BFS |
| 785 | Is Graph Bipartite? | BFS 2-coloring; odd cycle = non-bipartite |
| 200 | Number of Islands | BFS component flooding |
| 323 | Number of Connected Components | BFS/DFS component count |

---

## 🔗 Cross-Topic Connections

- **DFS Cycle Detection (File 04):** Same problem, recursive DFS. BFS avoids stack overflow.
- **Directed Cycle Detection (File 08):** Different algorithm needed — `inStack[]` instead of parent.
- **Kahn's Topo Sort (File 13):** Detects directed cycles as a side-effect of BFS in-degree reduction.
- **Union-Find:** Can detect undirected cycles in $O(\alpha(V))$ per edge — preferred for Kruskal's MST.
- **Bipartite Check:** BFS 2-coloring is essentially cycle detection for **odd-length cycles** specifically.
- **BFS (File 02):** This algorithm is BFS augmented with parent tracking — understand BFS first.

---

## ⚡ 2-Minute Revision Flash Card

- **Key trick:** Store `(node, parent)` pairs in the BFS queue — not just the node.
- **Cycle condition:** `visited[neighbor] == true AND neighbor != parent` → cycle found.
- **Handles disconnected graphs:** Loop `for (int i=0; i<V; ++i) if (!visited[i]) bfsCheck(i, ...)`.
- **Advantage over DFS:** Fully iterative — no recursion stack overflow risk for large $V$.
- **Time & Space:** $O(V + E)$ time; $O(V)$ space (queue holds at most $V$ entries).
