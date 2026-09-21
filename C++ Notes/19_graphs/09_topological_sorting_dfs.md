# Lecture 119: Topological Sorting in Graphs using DFS

> **One-Line Purpose:** Linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge $u \to v$, $u$ appears before $v$, using DFS post-order stack reversal.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #119  
> **Video ID:** `0WIINUY12Yg`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=0WIINUY12Yg)  
> **Duration:** 15:58  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Understand the definition and constraints of Topological Sort (DAGs only).
- Learn how Depth First Search (DFS) inherently captures dependency ordering.
- Discover how stack-based post-order tracking converts a tree into a directed sequence.
- Differentiate between cyclic and acyclic graph traversals in real-world compilation or scheduling tasks.

---

## 🧠 Core Intuition — Why This Works

Imagine you are putting on clothes. You must put on socks before shoes, and a shirt before a jacket. This is a real-world dependency graph.
If we map these dependencies:
`Socks -> Shoes`, `Shirt -> Jacket`

**Why DFS?** 
A node $u$ can only finish its DFS exploration after all its downstream prerequisites $v$ have completely finished. Hence, pushing nodes onto a stack upon recursive return guarantees that popping the stack yields dependencies in correct topological order.

**ASCII Visualization:**
```text
  (A) ---> (B) ---> (C)
    \               ^
     \             /
      \---> (D) --/
```
DFS starts at A. Goes to B, then C. C has no outgoing edges, so DFS for C finishes -> **Push C to Stack**.
Back to B. B's children are done -> **Push B to Stack**.
Back to A. Next child is D. Goes to D. D points to C (already visited). D is done -> **Push D to Stack**.
Back to A. A is done -> **Push A to Stack**.
Stack from top to bottom: `A, D, B, C` (a valid topological sort!)

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Course schedule" or "prerequisites"**: "Task A must be completed before Task B".
- **"Build systems" or "Compilation order"**: Resolving dependencies between modules or libraries.
- **"Alien Dictionary"**: Deducing character ordering based on a given set of sorted strings.
- **"DAG sequence processing"**: Finding the longest path in a DAG often requires topological sorting first to process nodes dynamically.
- **Key constraint**: The problem mentions "directed graph" without cycles, or implies sequential dependency.

---

## 📐 Algorithm Walk-Through

1. **Initialization**: Create a `visited` boolean array (or hash set) and a `stack` to store the final topological order.
2. **Global Traversal**: Iterate through all nodes (from `0` to `V-1`). If a node is not visited, initiate a DFS from it. This ensures disconnected components are fully processed.
3. **DFS Recursion**:
   - Mark the current node `u` as `visited`.
   - Iterate through all neighbors `v` of `u`. If `v` is unvisited, recursively call DFS on `v`.
4. **Post-Order Push**: After all children (dependencies) of `u` have been visited, push `u` onto the stack. This is the crucial step. A node is pushed only when everything reachable from it has been explored.
5. **Pop and Return**: After all nodes are processed, pop elements from the stack one by one and append them to the result list. This reversed finish-time order is the valid Topological Sort.

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <stack>

using namespace std;

class TopoSortDFS {
private:
    int V;
    vector<vector<int>> adj;

    void dfs(int u, vector<bool>& visited, stack<int>& st) {
        visited[u] = true;

        for (int v : adj[u]) {
            if (!visited[v]) {
                dfs(v, visited, st);
            }
        }

        st.push(u); // Push to stack upon backtracking
    }

public:
    TopoSortDFS(int vertices) : V(vertices), adj(vertices) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v); // u must precede v
    }

    vector<int> topologicalSort() {
        vector<bool> visited(V, false);
        stack<int> st;

        for (int i = 0; i < V; ++i) {
            if (!visited[i]) {
                dfs(i, visited, st);
            }
        }

        vector<int> result;
        while (!st.empty()) {
            result.push_back(st.top());
            st.pop();
        }
        return result;
    }
};

int main() {
    TopoSortDFS g(6);
    g.addEdge(5, 2);
    g.addEdge(5, 0);
    g.addEdge(4, 0);
    g.addEdge(4, 1);
    g.addEdge(2, 3);
    g.addEdge(3, 1);

    vector<int> order = g.topologicalSort();
    cout << "Topological Order: ";
    for (int x : order) cout << x << " ";
    cout << endl;
    return 0;
}
```

---

## 🔍 Dry Run Trace

Let's trace the graph given in `main()`:
Nodes: `0, 1, 2, 3, 4, 5`
Edges: `5->2, 5->0, 4->0, 4->1, 2->3, 3->1`

1. Loop `i` from 0 to 5.
2. `i = 0`: `visited[0] = false`. Call `dfs(0)`.
   - `0` has no outgoing edges.
   - Stack: `[0]` (top is 0)
3. `i = 1`: `visited[1] = false`. Call `dfs(1)`.
   - `1` has no outgoing edges.
   - Stack: `[0, 1]` (top is 1)
4. `i = 2`: `visited[2] = false`. Call `dfs(2)`.
   - Neighbors of `2`: `3`. `3` is unvisited.
   - Call `dfs(3)`.
     - Neighbors of `3`: `1`. `1` is visited. Done.
     - Push `3` to stack. Stack: `[0, 1, 3]`
   - Push `2` to stack. Stack: `[0, 1, 3, 2]`
5. `i = 3`: visited. Skip.
6. `i = 4`: `visited[4] = false`. Call `dfs(4)`.
   - Neighbors of `4`: `0`, `1`. Both are visited. Done.
   - Push `4` to stack. Stack: `[0, 1, 3, 2, 4]`
7. `i = 5`: `visited[5] = false`. Call `dfs(5)`.
   - Neighbors of `5`: `2`, `0`. Both are visited. Done.
   - Push `5` to stack. Stack: `[0, 1, 3, 2, 4, 5]`

Result: Pop from stack: `5, 4, 2, 3, 1, 0`
*(Note: Output may vary slightly based on edge insertion order, e.g., `4, 5, 2, 3, 1, 0` is also valid).*

---

## ⚠️ Common Interview Mistakes

1. **Applying it to Cyclic Graphs**: Topological sorting is mathematically undefined for cyclic graphs. If a cycle exists, standard DFS topo sort doesn't explicitly fail but returns an invalid ordering. Usually, cycle detection is needed as a preliminary step.
2. **Forgetting to check `visited` array**: Pushing elements directly without ensuring unvisited status leads to redundant recursions or infinite loops.
3. **Using a Queue instead of Stack for DFS post-order**: A queue appended normally will result in a completely reversed/incorrect topological order when printed out directly.
4. **Disconnected Graph Handle**: Assuming starting at node `0` is enough. You MUST have the outer loop iterating through all `V` nodes to ensure disconnected DAG components are covered.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(V + E)$ where $V$ is vertices and $E$ is edges. We visit each vertex exactly once, and iterate through all its neighbors exactly once.
- **Space Complexity:** $O(V)$ auxiliary stack for recursion, $O(V)$ for the `visited` array, and $O(V)$ for the manual `stack` to store the order. Total space: $O(V)$.

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Can a graph have multiple topological sorts?
**Answer:** Yes. A DAG will have a unique topological sort only if there is a directed path containing all vertices (a Hamiltonian path). If two vertices don't have a direct/indirect dependency path between them, their relative order is interchangeable, resulting in multiple valid sorts.

### Q2: What happens if the graph is undirected?
**Answer:** Topological Sort relies strictly on parent-child dependency arrows. In an undirected graph, edges have no direction, meaning dependencies go both ways (cycle between two nodes). Topo Sort is impossible.

### Q3: How do we modify this DFS method to detect cycles simultaneously?
**Answer:** Introduce a `recStack` (or `path` visited array) in addition to the standard `visited` array. When traversing, mark `recStack[u] = true`. If you encounter a neighbor where `recStack[v] == true`, a cycle exists. Don't forget to unmark `recStack[u] = false` when backtracking. 

### Q4: Which one is better: Kahn’s Algorithm (BFS) or DFS for Topological Sort?
**Answer:** Both run in $O(V + E)$. 
- **Kahn's BFS** is often preferred in interviews when the problem requires cycle detection combined with sorting, or when generating lexicographically smallest sorts (using a Priority Queue instead of a normal Queue).
- **DFS** is simpler to write and takes slightly less code space if only a pure sort is needed.

### Q5: Can Topological sort find the shortest path in a DAG?
**Answer:** Yes! Instead of Dijkstra ($O(E \log V)$), if the graph is a DAG, you can find the shortest path in $O(V+E)$. First, compute the topological order. Then, initialize distances to infinity. Iterate through nodes in topological order, and relax their edges. Since you visit nodes dependency-first, distances update correctly in linear time.

### Q6: If you process the nodes without a stack (just printing post-DFS), what order do you get?
**Answer:** You get a reverse topological order. When a node's DFS finishes, it is "safest" to put it at the very end. By saving them and then reversing the list (which a stack implicitly does by LIFO), we get the correct forward sequence.

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 207: Course Schedule](https://leetcode.com/problems/course-schedule/)** — (Requires Cycle Detection along with concepts of topo sort).
2. **[Leetcode 210: Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)** — (Direct application of Topological Sort, return the ordering).
3. **[Leetcode 269: Alien Dictionary (Premium)](https://leetcode.com/problems/alien-dictionary/)** — (Google favorite: build a graph of character dependencies and run topo sort).
4. **[Leetcode 329: Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/)** — (Can be modeled as finding longest path in a DAG).

---

## 🔗 Cross-Topic Connections
- **Dynamic Programming (DP on DAGs):** Many DP state transitions implicitly form a DAG. Solving problems using DP often visits subproblems in topological order without explicitly defining graph edges.
- **Cycle Detection:** Topo sort naturally pairs with Directed Cycle Detection algorithms.
- **Shortest/Longest Paths:** Topo sorting is uniquely powerful for finding shortest and longest paths in $O(V+E)$ time on directed graphs, bypassing Dijkstra/Bellman-Ford.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Order nodes such that all edges $u \to v$ go from left to right.
- **Constraints:** Graph must be Directed and Acyclic (DAG).
- **Core DFS Logic:** "Don't write me down until all my children are written down."
- **Data Structures:** `visited` array + `stack` (LIFO).
- **Crucial Step:** Push to stack strictly AFTER the loop traversing all neighbors ends (post-order).
- **Time/Space:** $O(V + E)$ Time | $O(V)$ Space.
