# Lecture 118: Detect Cycle in Directed Graph using DFS

> **One-Line Purpose:** Detect cycles in directed graphs by maintaining a recursion call stack array (`inStack`); encountering a neighbor currently active in the call stack proves a directed cycle.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #118  
> **Video ID:** `AcppN5XFt24`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=AcppN5XFt24)  
> **Duration:** 15:59  
> **Status:** AUDITED  

---

## 🔵 Algorithmic Principle: The `inStack` Array
In directed graphs, an already visited node is NOT necessarily part of a cycle (e.g. cross-edges or forward edges). A cycle exists **only if** the visited node is an ancestor in the active call stack path.

```
0 -> 1 -> 2
|         ^
+---------+ (Not a cycle! 0->2 is a forward edge, 2 is visited but unwound from stack)

0 -> 1 -> 2 -> 0 (CYCLE! 2 points back to 0 which is still active in stack)
```

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>

using namespace std;

class DirectedCycleDFS {
private:
    int V;
    vector<vector<int>> adj;

    bool dfsCheck(int u, vector<bool>& visited, vector<bool>& inStack) {
        visited[u] = true;
        inStack[u] = true;

        for (int v : adj[u]) {
            if (!visited[v]) {
                if (dfsCheck(v, visited, inStack)) return true;
            } else if (inStack[v]) {
                // Back-edge pointing to an active recursion ancestor
                return true;
            }
        }

        inStack[u] = false; // Unwind stack
        return false;
    }

public:
    DirectedCycleDFS(int vertices) : V(vertices), adj(vertices) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v); // Directed edge u -> v
    }

    bool hasCycle() {
        vector<bool> visited(V, false);
        vector<bool> inStack(V, false);

        for (int i = 0; i < V; ++i) {
            if (!visited[i]) {
                if (dfsCheck(i, visited, inStack)) return true;
            }
        }
        return false;
    }
};

int main() {
    DirectedCycleDFS g(4);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(2, 3);
    g.addEdge(3, 1); // Directed cycle: 1 -> 2 -> 3 -> 1

    cout << "Directed Cycle: " << (g.hasCycle() ? "YES" : "NO") << endl;
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(V + E)$
- **Space Complexity:** $O(V)$ for `visited`, `inStack`, and recursive stack.

---

## 🧠 Core Intuition — Why This Works

### Real-World Analogy: Task Dependencies with Deadlock
Imagine a software build system where tasks have dependencies (directed edges). A **cycle** = a deadlock: Task A needs Task B, Task B needs Task C, Task C needs Task A — nothing can ever start.

`inStack[u] = true` means "Task $u$ is currently being worked on (its dependencies haven't all been resolved yet)." If while resolving $u$'s dependencies we reach a task that is **already being worked on**, we have a circular dependency — a deadlock.

```
No Cycle (DAG):              Cycle Present:

0 → 1 → 3                   0 → 1 → 2
    ↓                            ↑   |
    2                            +---+
    
DFS(0): inStack={0}          DFS(0): inStack={0}
  DFS(1): inStack={0,1}        DFS(1): inStack={0,1}
    DFS(3): inStack={0,1,3}      DFS(2): inStack={0,1,2}
      No neighbors → return         neighbor 1: visited AND inStack[1]=true
    inStack[3]=false                 → CYCLE DETECTED! ✓
    DFS(2): inStack={0,1,2}
      No unvisited/inStack neighbors
    inStack[2]=false
  inStack[1]=false
inStack[0]=false
→ NO CYCLE
```

### The Key Insight: `visited` vs `inStack` — Why Both Are Needed
- `visited[v] = true` means: "We have already **completely processed** $v$ in some previous DFS call tree." It's a globally complete node.
- `inStack[v] = true` means: "We are **currently inside** the DFS call for $v$; it hasn't returned yet."

**Why `visited` alone fails:** Consider a diamond shape `0→1, 0→2, 1→3, 2→3`. When DFS processes path `0→1→3`, it marks `3` as visited. Then when processing path `0→2→3`, it sees `3` as visited. Without `inStack`, it would falsely report a cycle. But `3` is NOT in the current stack when path `0→2→3` hits it — `inStack[3] = false` after the first subtree returns. So no cycle.

| Node state | `visited` | `inStack` | What it means |
|---|---|---|---|
| Never seen | `false` | `false` | Unprocessed |
| Currently in DFS call | `true` | `true` | Ancestor in current path |
| Fully processed | `true` | `false` | Completed, not in current stack |

---

## 🎯 Pattern Recognition — When to Use This Algorithm

| Signal | Algorithm |
|---|---|
| "Detect cycle in **directed** graph" | DFS with `inStack[]` (this file) |
| "Detect cycle in **undirected** graph" | DFS with parent tracking (File 04) |
| "Can all tasks/courses be completed?" | Directed cycle detection (File 10, 08) |
| "Is the graph a DAG?" | Directed cycle detection (no cycle = DAG) |
| "Topological sort feasible?" | Only if DAG (no directed cycle) |

### Why Can't We Use the Undirected Approach (Parent Tracking)?
In a directed graph, edges are one-way. There is no trivial "reverse edge" problem like in undirected graphs. However, there ARE **cross edges** and **forward edges** that point to already-visited nodes without forming cycles. Parent tracking only solves the undirected trivial-reversal problem — it doesn't handle directed cross/forward edges.

The `inStack` approach correctly handles all directed edge types:
- **Back edge** `(u→v)` where `inStack[v]=true`: CYCLE.
- **Forward/Cross edge** `(u→v)` where `visited[v]=true && inStack[v]=false`: NOT a cycle.

---

## 📐 Algorithm Walk-Through

**Step-by-step for `0→1→2→3→1` (cycle at 1-2-3):**

```
hasCycle() called:
  i=0: not visited → dfsCheck(0, ...)
    visited[0]=true, inStack[0]=true
    neighbor 1: not visited → dfsCheck(1, ...)
      visited[1]=true, inStack[1]=true
      neighbor 2: not visited → dfsCheck(2, ...)
        visited[2]=true, inStack[2]=true
        neighbor 3: not visited → dfsCheck(3, ...)
          visited[3]=true, inStack[3]=true
          neighbor 1: visited=true AND inStack[1]=true → RETURN TRUE!
        dfsCheck(3) returns true → dfsCheck(2) returns true
      → dfsCheck(1) returns true → dfsCheck(0) returns true
  hasCycle() returns TRUE ✓
```

---

## ⚠️ Common Interview Mistakes

### 1. Forgetting to Unwind `inStack` on Return
```cpp
// ❌ WRONG — never sets inStack[u] = false after DFS returns
bool dfsCheck(int u, ...) {
    visited[u] = inStack[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) dfsCheck(v, ...);
        else if (inStack[v]) return true;
    }
    // Missing: inStack[u] = false!
    return false;
}
// Result: All subsequent nodes appear "in stack" → false cycle everywhere
```

### 2. Checking `visited[v]` Instead of `inStack[v]`
```cpp
// ❌ WRONG for directed graphs — cross/forward edges trigger false positive
} else if (visited[v]) { // Should be inStack[v]!
    return true;
}
// Example: 0→1, 0→2, 1→2 (diamond). DFS visits 2 via 1, marks visited.
// Then 0→2 sees visited[2]=true → FALSE CYCLE REPORTED
```

### 3. Using the Undirected Cycle Algorithm (Parent Tracking) on Directed Graphs
The parent-tracking technique (`neighbor != parent`) is designed exclusively for undirected graphs. For directed graphs, there is no "trivial reverse edge" to filter — use `inStack[]` instead.

### 4. Forgetting Disconnected Components
```cpp
// ❌ Only checks one component
dfsCheck(0, visited, inStack);

// ✅ Check all components
for (int i = 0; i < V; ++i)
    if (!visited[i] && dfsCheck(i, visited, inStack)) return true;
```

### 5. Not Handling Self-Loops
A self-loop `u → u` is a trivial cycle. The algorithm handles it correctly:
- `visited[u] = inStack[u] = true`
- neighbor `u`: `visited[u] = true` AND `inStack[u] = true` → returns `true`. ✓

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Why do we need BOTH `visited[]` and `inStack[]` arrays? Can we use just one?

**Answer:** We need both because they convey different information:

- `visited[v] = true` means: DFS has **fully completed** processing of $v$ (all its descendants explored). Using `visited` alone to detect cycles would cause false positives: cross/forward edges point to already-visited nodes that are NOT in the current path.

- `inStack[v] = true` means: $v$ is an **active ancestor** in the current DFS recursion chain. A back edge to an `inStack` node = a cycle.

Using only `inStack`: If we don't maintain `visited`, we'd re-enter completed nodes in subsequent DFS calls from the outer loop, wasting $O(V \times E)$ time.

Using only `visited` for cycle detection: Would produce false positives in DAGs with cross/forward edges (see Mistake #2 above).

**Minimal alternative:** You can use a **3-state** array instead of two boolean arrays:
- `0` = unvisited
- `1` = in current DFS stack (inStack)
- `2` = fully processed (visited, not in stack)

```cpp
bool dfsCheck(int u, vector<int>& color) {
    color[u] = 1; // Mark as "in stack"
    for (int v : adj[u]) {
        if (color[v] == 1) return true;       // Back edge = cycle
        if (color[v] == 0 && dfsCheck(v, color)) return true;
    }
    color[u] = 2; // Mark as "fully processed"
    return false;
}
```

### Q2: [Proof] Prove that `inStack[v] == true` when processing a neighbor $v$ from $u$ implies a directed cycle.

**Answer:**
- `inStack[v] = true` means the DFS call for $v$ is still active (hasn't returned).
- This means there is a DFS tree path from $v$ to $u$: $v = w_1 \to w_2 \to \cdots \to w_k = u$ (since DFS called $u$ during $v$'s unfinished exploration).
- The directed edge $u \to v$ (currently being explored) combined with the DFS path $v \to \cdots \to u$ forms a directed cycle: $v \to \cdots \to u \to v$. ∎

**Contrapositive:** If `inStack[v] == false` when we see a visited $v$, then $v$ has already completely returned from DFS. By the Parenthesis Theorem, $v$ is NOT an ancestor of $u$ in the current DFS path. So no directed cycle via $u \to v$ exists.

### Q3: [Comparison] Directed cycle detection via DFS (`inStack`) vs Kahn's algorithm — when to prefer which?

**Answer:**
| Criterion | DFS + inStack | Kahn's (BFS in-degree) |
|---|---|---|
| Implementation | Recursive (stack overflow risk) | Iterative (safer) |
| Additional output | DFS tree, timestamps | Topological order |
| Cycle path | Traceable via call stack | Not directly |
| Memory | $O(V)$ + recursion stack | $O(V + E)$ |
| Preferred when | Also need topological sort via DFS | Need explicit topo order as output |
| Parallelism | Harder to parallelize | Easier (process all in-degree 0 simultaneously) |

For **pure cycle detection**, both are equivalent. Kahn's is often preferred in production for large graphs due to the iterative (non-recursive) nature.

### Q4: [Bug Prediction] What cycle does this code report for `0→1→2→0`?
```cpp
bool dfsCheck(int u, vector<int>& color) {
    color[u] = 1;
    for (int v : adj[u]) {
        if (color[v] == 0) {
            if (dfsCheck(v, color)) return true;
        } else if (color[v] == 1) {
            cout << "Cycle ends at node: " << v << endl;
            return true;
        }
    }
    color[u] = 2;
    return false;
}
// Graph: 0->1->2->0
```
**Answer:** Output: `Cycle ends at node: 0`. When DFS reaches node 2 and explores its neighbor 0, `color[0] = 1` (0 is still in the stack). The message prints "Cycle ends at node: 0", meaning the cycle `0→1→2→0` is detected. Node 0 is the entry point of the cycle.

### Q5: [Extension] How would you find and print the actual cycle in a directed graph?

**Answer:** Maintain a `path` stack alongside `inStack`:

```cpp
bool dfsCheck(int u, vector<bool>& visited, vector<bool>& inStack,
              vector<int>& path) {
    visited[u] = inStack[u] = true;
    path.push_back(u);

    for (int v : adj[u]) {
        if (!visited[v]) {
            if (dfsCheck(v, visited, inStack, path)) return true;
        } else if (inStack[v]) {
            // Print cycle: find v in path, print from v to end
            cout << "Cycle: ";
            bool printing = false;
            for (int node : path) {
                if (node == v) printing = true;
                if (printing) cout << node << " ";
            }
            cout << v << endl; // Complete the cycle
            return true;
        }
    }

    path.pop_back();
    inStack[u] = false;
    return false;
}
```

### Q6: [Complexity] What is the worst-case space complexity for directed cycle DFS on a graph where all vertices form a single chain?

**Answer:** For a chain $0 \to 1 \to 2 \to \cdots \to V-1$:
- DFS call stack depth = $V$ (one call per node in the chain).
- `visited[]` array: $O(V)$.
- `inStack[]` array: $O(V)$.
- Recursion call stack: $O(V)$ frames.

Total space: $O(V)$. For $V = 10^5$ this may cause a stack overflow with default OS stack limits (~1-8 MB). Solution: implement iterative DFS or use Kahn's algorithm.

### Q7: [Advanced] Can Kahn's algorithm detect cycles in a graph that is NOT a DAG, and does it tell you which nodes form the cycle?

**Answer:** Kahn's algorithm detects the **presence** of a cycle (via `topoOrder.size() < V`), but does NOT directly identify which specific nodes form the cycle.

The nodes NOT appearing in `topoOrder` are exactly the nodes involved in cycles (they never reached in-degree 0). However, this set may include nodes that are merely **reachable** from a cycle without being part of it (descendants of cycle nodes also won't be processed if their only path through the cycle).

To find the **exact cycle nodes**: after Kahn's, collect nodes with `inDegree[v] > 0` — these are nodes whose in-degrees were never reduced to zero, meaning they're either in the cycle or only reachable through cycle nodes. For the exact cycle path, DFS with `inStack[]` is more direct.

---

## 🏆 Related LeetCode Problems

| # | Problem | Approach Hint |
|---|---|---|
| 207 | Course Schedule | Directed cycle detection; return true if no cycle |
| 210 | Course Schedule II | Topological sort (only if no cycle) |
| 802 | Find Eventual Safe States | Nodes NOT part of cycles; reverse DFS |
| 684 | Redundant Connection | Undirected cycle — use Union-Find instead |
| 1059 | All Paths from Source Lead to Destination | DFS + state coloring |

---

## 🔗 Cross-Topic Connections

- **DFS (File 03):** Directed cycle detection is DFS augmented with `inStack[]` — master base DFS first.
- **Undirected Cycle DFS (File 04):** Same DFS framework but uses `parent` instead of `inStack` — fundamentally different semantics.
- **Topological Sort DFS (File 09):** Works ONLY on DAGs. Directed cycle detection is its prerequisite. Same DFS structure.
- **Kahn's Algorithm (File 13):** BFS alternative for cycle detection — `topoOrder.size() < V` implies cycle.
- **Course Schedule (File 10):** Direct application of directed cycle detection.
- **SCC (Kosaraju/Tarjan):** Uses DFS with timestamps; cycles within SCCs are the reason SCCs form.

---

## ⚡ 2-Minute Revision Flash Card

- **Key arrays:** `visited[]` (globally completed) + `inStack[]` (currently active in DFS path) — both needed.
- **Cycle condition:** `inStack[v] == true` when processing a neighbor $v$ → back edge → directed cycle.
- **Always unwind:** `inStack[u] = false` when `dfsCheck(u)` returns — critical or everything looks cyclic.
- **vs. Undirected:** Directed uses `inStack`; undirected uses `parent` — different problems, different tools.
- **Alternative:** 3-color DFS: `0=unvisited`, `1=in-stack`, `2=done` — one array instead of two.
