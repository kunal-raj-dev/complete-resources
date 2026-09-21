# Lecture 135: Strongly Connected Components: Kosaraju's Algorithm

> **One-Line Purpose:** Partition a directed graph into its maximal Strongly Connected Components (SCCs) in $O(V + E)$ time using two DFS passes and graph transposition.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #135  
> **Video ID:** `lqY8TE0P1S8`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=lqY8TE0P1S8)  
> **Duration:** 26:26  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Define a Strongly Connected Component (SCC) in directed graphs.
- Understand how condensing SCCs converts any directed graph into a Directed Acyclic Graph (DAG).
- Grasp the magic of graph Transposition (reversing edges).
- Master the 3-step Kosaraju pipeline: Finish-Order Stack $\to$ Transpose $\to$ Collect.

---

## 🧠 Core Intuition — Why This Works

A **Strongly Connected Component (SCC)** is a group of nodes where you can reach *any* node from *any other* node in that group. (e.g., A cycle is an SCC).
If we treat each SCC as a giant "super-node", the overall graph becomes a DAG (no cycles between super-nodes).
In a DAG, if we start DFS from a "sink" (a node with no outgoing edges), we can't accidentally wander into another component. We will perfectly explore just that sink node/component.

**How do we find a sink SCC?**
1. **Pass 1 (Topological Finish Order):** We do a standard DFS and push nodes to a stack *after* finishing them. The node at the very top of the stack is guaranteed to be in a "Source" SCC of the condensed DAG. 
2. **Graph Inversion (Transpose $G^T$):** If we reverse every directed edge, a "Source" SCC becomes a "Sink" SCC!
3. **Pass 2 (Component Traversal):** We pop the top node from the stack (which is now in a Sink SCC in $G^T$). We run DFS. Because it's a sink, the DFS is trapped! It will only visit the nodes in that specific SCC. Once done, we pop the next unvisited node, which will be the next sink, and so on.

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Strongly connected"**: Direct keyword.
- **"Mutual reachability"**: "Can Alice reach Bob AND Bob reach Alice?"
- **"Condensation graph"**: Problems that ask you to find the minimum edges to make a whole graph strongly connected, or shortest path between clusters.

---

## 📐 Algorithm Walk-Through

1. **Pass 1 (Order by Finish Time)**:
   - Create a `stack<int> st` and a `visited` array.
   - For every unvisited node $i$, call `dfsFillOrder(i)`.
   - In `dfsFillOrder(u)`: mark visited, recurse on unvisited neighbors, and `st.push(u)` right before returning.
2. **Transpose the Graph**:
   - Create `adjT` (transposed adjacency list).
   - For every edge `u -> v` in the original graph, add `v -> u` to `adjT`. (This can be done while building the initial graph to save a loop).
3. **Pass 2 (Extract SCCs)**:
   - Reset the `visited` array to `false`.
   - While `st` is not empty:
     - Pop `u`.
     - If `u` is unvisited, create an empty `component` list and call `dfsCollect(u)` using `adjT`.
     - In `dfsCollect(u)`: mark visited, add to `component`, and recurse on unvisited neighbors in `adjT`.
     - Push the filled `component` into the final `sccs` list.

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <stack>

using namespace std;

class KosarajuSCC {
private:
    int V;
    vector<vector<int>> adj;
    vector<vector<int>> adjT; // Transpose graph

    // Step 1 DFS
    void dfsFillOrder(int u, vector<bool>& visited, stack<int>& st) {
        visited[u] = true;
        for (int v : adj[u]) {
            if (!visited[v]) dfsFillOrder(v, visited, st);
        }
        st.push(u); // Post-order push
    }

    // Step 3 DFS
    void dfsCollect(int u, vector<bool>& visited, vector<int>& component) {
        visited[u] = true;
        component.push_back(u);
        for (int v : adjT[u]) {
            if (!visited[v]) dfsCollect(v, visited, component);
        }
    }

public:
    KosarajuSCC(int vertices) : V(vertices), adj(vertices), adjT(vertices) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adjT[v].push_back(u); // Reverse edge built immediately
    }

    vector<vector<int>> getSCCs() {
        stack<int> st;
        vector<bool> visited(V, false);

        // Step 1: Push vertices to stack by finish time
        for (int i = 0; i < V; ++i) {
            if (!visited[i]) dfsFillOrder(i, visited, st);
        }

        // Step 2 & 3: Process transpose graph in stack order
        fill(visited.begin(), visited.end(), false);
        vector<vector<int>> sccs;

        while (!st.empty()) {
            int u = st.top();
            st.pop();

            if (!visited[u]) {
                vector<int> component;
                dfsCollect(u, visited, component);
                sccs.push_back(component);
            }
        }
        return sccs;
    }
};

int main() {
    KosarajuSCC g(5);
    // Cycle: 0 -> 2 -> 1 -> 0
    g.addEdge(1, 0);
    g.addEdge(0, 2);
    g.addEdge(2, 1);
    // Edge to another component
    g.addEdge(0, 3);
    // 3 -> 4
    g.addEdge(3, 4);

    auto sccs = g.getSCCs();
    cout << "Strongly Connected Components Count: " << sccs.size() << endl; // Output: 3
    for (size_t i = 0; i < sccs.size(); ++i) {
        cout << "SCC " << i + 1 << ": ";
        for (int node : sccs[i]) cout << node << " ";
        cout << endl;
    }
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Graph:** `1->0`, `0->2`, `2->1` (SCC 1). `0->3` (Bridge). `3->4` (SCC 2, SCC 3).
Vertices: 0, 1, 2, 3, 4.

**Pass 1 (Fill Order):**
- DFS(0): visits 2, visits 1. 1 has no unvisited neighbors. Push 1. Return to 2. Push 2. Return to 0. Visits 3, visits 4. 4 has no neighbors. Push 4. Return to 3. Push 3. Return to 0. Push 0.
- `stack` (top to bottom): `[0, 3, 4, 2, 1]`

**Transpose Graph (`adjT`):**
- `0->1`, `2->0`, `1->2`, `3->0`, `4->3`

**Pass 2 (Collect):**
- Pop `0`. Unvisited. `dfsCollect(0)` on `adjT`:
  - Visited 0. Goes to 1. Visited 1. Goes to 2. Visited 2. Goes to 0 (visited). 
  - Component 1: `[0, 1, 2]`.
- Pop `3`. Unvisited. `dfsCollect(3)` on `adjT`:
  - Visited 3. Goes to 0 (visited).
  - Component 2: `[3]`.
- Pop `4`. Unvisited. `dfsCollect(4)` on `adjT`:
  - Visited 4. Goes to 3 (visited).
  - Component 3: `[4]`.
- Pop `2`. Visited.
- Pop `1`. Visited.

**Result:** `[0,1,2]`, `[3]`, `[4]`. Correct!

---

## ⚠️ Common Interview Mistakes

1. **Forgetting to Reset the Visited Array**: The biggest bug is finishing Pass 1 and forgetting to do `fill(visited.begin(), visited.end(), false);` before starting Pass 2.
2. **Using the Original Graph in Pass 2**: Calling `dfsCollect` but accidentally looping over `adj[u]` instead of `adjT[u]`.
3. **Misunderstanding the Stack**: The stack does NOT store topological sort if the graph has cycles (topological sort doesn't exist for cyclic graphs). It specifically stores the *finish times*, ensuring the source SCC components are at the top.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(V + E)$. Building the transpose takes $O(V + E)$. Pass 1 takes $O(V + E)$. Pass 2 takes $O(V + E)$. Total is strictly linear.
- **Space Complexity:** $O(V + E)$ for the transposed adjacency list `adjT`. $O(V)$ for the stack and visited array.

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Can we use BFS instead of DFS?
**Answer:** In Pass 2 (Collect on transpose), yes, you can use BFS to flood-fill the component. But in Pass 1 (Fill Order), NO. BFS does not give you "finish times". You must use DFS post-order to determine which component is a sink/source.

### Q2: How does Kosaraju compare to Tarjan's SCC algorithm?
**Answer:** Tarjan's SCC algorithm finds SCCs in a SINGLE pass using `tin` and `low` arrays, and no transpose is needed. 
- Kosaraju is easier to understand and code for many people.
- Tarjan's is technically faster by a constant factor because it avoids building `adjT` and skips the second pass. Both are $O(V + E)$.

### Q3: What happens if the graph is undirected?
**Answer:** An undirected graph is technically its own transpose. Any connected component in an undirected graph is inherently strongly connected (you can walk back across any edge). SCC algorithms are explicitly for Directed graphs. For undirected, just use a basic BFS/DFS component counter.

### Q4: If the graph is already a DAG (no cycles), what does Kosaraju output?
**Answer:** It will output exactly $V$ components. Every single node will be its own Strongly Connected Component of size 1.

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 207: Course Schedule](https://leetcode.com/problems/course-schedule/)** — Finding an SCC of size > 1 is identical to detecting a cycle.
2. **[Leetcode 1483: Kth Ancestor of a Tree Node](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/)** — Tangentially related as graph structural queries, but SCC condensation is often a preprocessing step in hard graph routing DP problems.

---

## 🔗 Cross-Topic Connections
- **Topological Sort:** Pass 1 of Kosaraju IS a Topological Sort (if the graph were a DAG).
- **Tarjan's Bridges:** Just like Tarjan's, Kosaraju relies heavily on DFS tree properties.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Group nodes into maximal mutually reachable sets.
- **Step 1:** DFS on original graph. Push to stack `st` AFTER exploring neighbors.
- **Step 2:** Reverse all edges to create Transpose Graph `adjT`.
- **Step 3:** While stack is not empty, pop `u`. If unvisited, DFS on `adjT` to collect 1 full SCC.
- **Why Transpose?** It turns Source SCCs into Sink SCCs, trapping DFS inside the component.
- **Time/Space:** $O(V + E)$ Time | $O(V + E)$ Space.
