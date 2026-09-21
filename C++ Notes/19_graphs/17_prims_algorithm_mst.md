# Lecture 127: Prim's Algorithm: Minimum Spanning Tree

> **One-Line Purpose:** Greedily grow a minimum spanning tree from an arbitrary start vertex by always picking the minimum-weight cut edge using a Min-Heap in $O((V + E) \log V)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #127  
> **Video ID:** `Sflh1z6cIMk`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=Sflh1z6cIMk)  
> **Duration:** 26:07  
> **Status:** AUDITED  

---

## 🔵 Core Cut-Property Intuition
A **Spanning Tree** of connected undirected graph $G=(V,E)$ is an acyclic subgraph connecting all $V$ vertices with exactly $V - 1$ edges.
**Cut Property:** For any cut partition $(S, V \setminus S)$, the minimum weight edge crossing the cut strictly belongs to the Minimum Spanning Tree. Prim's algorithm starts with $S = \{0\}$ and iteratively adds the cheapest crossing edge into $S$.

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <queue>

using namespace std;

// Pair: <weight, vertex>
typedef pair<int, int> pii;

class PrimsAlgorithm {
public:
    static int spanningTree(int V, const vector<vector<pair<int, int>>>& adj) {
        priority_queue<pii, vector<pii>, greater<pii>> pq;
        vector<bool> inMST(V, false);

        // Start with vertex 0, weight 0
        pq.push({0, 0});
        int totalWeight = 0;
        int edgesCount = 0;

        while (!pq.empty() && edgesCount < V) {
            auto [wt, u] = pq.top();
            pq.pop();

            if (inMST[u]) continue; // Skip if already part of MST

            inMST[u] = true;
            totalWeight += wt;
            edgesCount++;

            for (const auto& edge : adj[u]) {
                int v = edge.first;
                int weight = edge.second;

                if (!inMST[v]) {
                    pq.push({weight, v});
                }
            }
        }

        return totalWeight;
    }
};

int main() {
    int V = 4;
    vector<vector<pair<int, int>>> adj(V);
    // u, v, weight
    auto addEdge = [&](int u, int v, int w) {
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    };

    addEdge(0, 1, 10);
    addEdge(0, 2, 6);
    addEdge(0, 3, 5);
    addEdge(1, 3, 15);
    addEdge(2, 3, 4);

    cout << "Total MST Cost (Prim's): " << PrimsAlgorithm::spanningTree(V, adj) << endl; // Output: 19 (5 + 4 + 10)
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O((V + E) \log V)$
- **Space Complexity:** $O(V + E)$

---

## 🧠 Core Intuition — Why This Works

**Real-World Analogy:** Imagine you're building a network of water pipes across cities. You start in one city, and at every step you ask: "What's the cheapest pipe I can lay to connect ONE more unconnected city to my existing network?" You greedily pick the cheapest extension. This is Prim's — always expanding the cheapest frontier edge.

**The Cut Property (formal):** If we have a partition of vertices into set $S$ (in MST) and $V \setminus S$ (not yet), the lightest edge crossing the cut **must** be in the MST. Why? By exchange argument: if the MST uses a heavier crossing edge, swapping it for the lighter one yields a cheaper spanning tree — contradiction.

**ASCII Visualization:**
```
        10
   0 -------- 1
   |\          |
  6| \5       |15
   |   \      |
   2 ---\ --- 3
    \  4  \  /
     -------/

Step 1: S={0}, frontier edges: {(0,1,10),(0,2,6),(0,3,5)}
         Pick cheapest: (0,3,5) → MST cost = 5
         
Step 2: S={0,3}, frontier edges: {(0,1,10),(0,2,6),(3,2,4),(3,1,15)}
         Pick cheapest: (3,2,4) → MST cost = 9
         
Step 3: S={0,3,2}, frontier edges: {(0,1,10),(2,0,6 stale),(3,1,15)}
         Pick cheapest: (0,1,10) → MST cost = 19
         
MST Edges: {(0,3,5), (3,2,4), (0,1,10)}, Total = 19
```

---

## 🎯 Pattern Recognition — When to Use This

**Keyword triggers from problem statements:**
- "Minimum cost to connect all nodes"
- "Minimum spanning tree"
- "Cheapest way to build roads/pipes/cables connecting all cities"
- "Minimize total edge weight of connected subgraph"

**Choose Prim's (over Kruskal's) when:**
- **Dense graph:** $E \approx V^2$ — Prim's $O(V^2)$ matrix version beats Kruskal's $O(E \log E) = O(V^2 \log V)$
- Graph is given as **adjacency matrix** (common in grid problems)
- You need the MST construction **online** (streaming edges)

**Choose Kruskal's (over Prim's) when:**
- **Sparse graph:** $E \ll V^2$
- Edges are given as a sorted **edge list**
- You already have DSU infrastructure from another subproblem

---

## 🔍 Dry Run Trace

**Graph:** 4 vertices, edges: `(0,1,10), (0,2,6), (0,3,5), (1,3,15), (2,3,4)`

```
Initial: inMST = [F,F,F,F], pq = {(0,0)}, totalWeight = 0

Iteration 1:
  Pop (0,0): Mark 0 in MST. Push neighbors: (10,1),(6,2),(5,3)
  pq = {(5,3),(6,2),(10,1)}, total = 0

Iteration 2:
  Pop (5,3): Mark 3 in MST. Push neighbors: (15,1),(4,2) [0 already in]
  pq = {(4,2),(6,2),(10,1),(15,1)}, total = 5

Iteration 3:
  Pop (4,2): Mark 2 in MST. Push neighbors: (6,0 already in)
  pq = {(6,2 stale),(10,1),(15,1)}, total = 9

Iteration 4:
  Pop (6,2): 2 already inMST → SKIP
  Pop (10,1): Mark 1 in MST. total = 19

All V=4 vertices in MST. Final cost = 19 ✓
```

---

## ⚠️ Common Interview Mistakes

1. **Not checking `inMST[u]` after popping from heap:** The min-heap can contain STALE entries (outdated edge weights for a vertex that's already been added). Skipping the `if (inMST[u]) continue;` check causes double-counting.

2. **Stopping condition confusion:** Loop should run until `edgesCount == V` or the heap is empty (not until `edgesCount == V-1` edges added, because we add the dummy `{0,0}` edge for the start vertex too).

3. **Adding both directions when processing:** When you add edges of vertex `u` to the heap, only add edges to vertices NOT in MST. Forgetting `if (!inMST[v])` bloats the heap but doesn't cause wrong answers due to the `inMST` check on pop.

4. **Dense graph with heap:** For dense graphs ($E = O(V^2)$), using a heap gives $O(V^2 \log V)$ but the $O(V^2)$ array-based Prim's is better. The min-cost-connect-all-points problem (LeetCode 1584) specifically benefits from the $O(N^2)$ variant.

5. **Prim's on disconnected graphs:** Standard Prim's fails silently on disconnected graphs. Must check if all vertices were added to MST after the loop.

---

## 🔥 Interview Q&A — Google/Amazon/Meta Level

### Q1: [Conceptual] Why does the Cut Property guarantee Prim's algorithm is correct?
**Answer:** The Cut Property states: for any cut $(S, V \setminus S)$ of a graph, if edge $e$ is the minimum weight edge crossing the cut, then $e$ belongs to some MST. Prim's algorithm maintains the invariant: at every step, $S$ contains vertices already in the MST, and we pick the minimum edge crossing the cut. By the Cut Property, this edge always belongs to the MST. Since we add $V-1$ such edges (each time increasing $|S|$ by 1), we build the complete MST. The exchange argument proof: assume the MST $T$ doesn't contain minimum crossing edge $e = (u,v)$. Adding $e$ to $T$ creates a cycle. This cycle must contain another crossing edge $e'$ (since both endpoints of $e'$ are on different sides of the cut). Replace $e'$ with $e$ in $T$: the result is a spanning tree with smaller total weight — contradicting $T$ being the MST. So $e$ must be in $T$.

### Q2: [Comparison] Prim's vs Kruskal's — complexity analysis when graph is dense vs sparse?
**Answer:** 
- **Sparse graph** ($E = O(V)$): Kruskal's $O(E \log E) = O(V \log V)$ beats Prim's heap $O((V+E)\log V) = O(V \log V)$. Similar but Kruskal's simpler.
- **Dense graph** ($E = O(V^2)$): Kruskal's $O(E \log E) = O(V^2 \log V)$. Prim's with heap $O((V+E)\log V) = O(V^2 \log V)$. But Prim's with array/no-heap: $O(V^2)$ — much better!
- **With Fibonacci heap:** Prim's achieves $O(E + V \log V)$, which is optimal for dense graphs and theoretically beats Kruskal's on all graph types. However, Fibonacci heaps have large constants and are rarely used in practice.

### Q3: [Extension] How would you modify Prim's to also output the MST edges (not just total weight)?
**Answer:** Track the parent of each vertex:
```cpp
vector<int> parent(V, -1);
vector<int> key(V, INT_MAX); // Minimum edge weight to reach vertex
// When relaxing: if (weight < key[v]) { key[v] = weight; parent[v] = u; }
// MST edges: (parent[v], v) for all v != src
```
This is the standard "parent array" trick used in the classical Prim's implementation (not the heap-based one above).

### Q4: [Debugging] What's wrong with this condition?
```cpp
while (!pq.empty() && edgesCount < V - 1) {
```
**Answer:** It stops after $V-2$ edges are added (loop condition `edgesCount < V-1` exits when `edgesCount == V-1`... actually wait). Let's trace: we start with `edgesCount=0` and push `{0,0}`. When we pop `(0,0)`, we mark vertex 0 in MST and increment `edgesCount` to 1. We need `V` vertices total, so we need to pop `V` times. The condition should be `edgesCount < V`. Using `< V-1` would cause us to exit after adding $V-2$ edges, leaving the last vertex unprocessed and returning a wrong answer.

### Q5: [System Design] Design a network topology optimizer for a data center with 1000 servers. Which MST algorithm and which data structure would you use?
**Answer:** For a data center, the graph is typically dense (all servers can potentially connect to all others, $E \approx V^2/2 = 500,000$ edges). I'd use **Prim's algorithm with an adjacency matrix and array-based key tracking** in $O(V^2) = O(10^6)$ time — no heap needed since scanning the key array is $O(V)$ per step. Edge weights could be latency, bandwidth cost, or cable length. For real data centers, we'd also consider: redundancy requirements (find MST + backup paths), bandwidth constraints (not just minimum spanning tree but minimum bottleneck), and multi-commodity flow. The MST gives the cheapest single-connected tree; for resilience, we'd compute a 2-edge-connected spanning subgraph.

### Q6: [Proof] Why does Prim's always produce a tree (no cycles)?
**Answer:** We mark each vertex `inMST` when it's added. When processing vertex $u$, we only push edges $(u,v)$ where `!inMST[v]`. When popping vertex $v$, if `inMST[v]` is already true, we skip it. Therefore, each vertex is added to the MST **exactly once**. A graph on $V$ vertices with $V-1$ edges and no vertex added twice is necessarily acyclic (tree). The MST contains exactly $V-1$ edges connecting all $V$ vertices with no cycles = spanning tree.

### Q7: [Extension] Can Prim's handle negative edge weights?
**Answer:** Yes! Unlike Dijkstra's algorithm, Prim's correctness doesn't depend on edge weights being non-negative. The Cut Property works regardless of sign. The min-heap still correctly identifies the minimum-weight crossing edge. However, the "total weight" could become negative if many negative edges exist — that's fine. The algorithm still terminates correctly. This is one advantage Prim's has over Dijkstra's.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Approach |
|---|---|---|
| 1584 | Min Cost to Connect All Points | Prim's $O(N^2)$ on fully connected graph with Manhattan distances |
| 1135 | Connecting Cities With Minimum Cost | Kruskal's or Prim's classic MST |
| 1168 | Optimize Water Distribution in a Village | Add virtual node + MST (Prim's/Kruskal's) |
| 1489 | Find Critical and Pseudo-Critical Edges in MST | MST + edge inclusion/exclusion |
| 778 | Swim in Rising Water | Binary search + MST or Dijkstra |

---

## 🔗 Cross-Topic Connections

- **Kruskal's Algorithm:** Edge-centric MST; complement to Prim's vertex-centric approach
- **Dijkstra's Algorithm:** Structurally similar (min-heap + visited array) but for shortest paths, not MST. Key difference: Dijkstra accumulates total path cost; Prim's only cares about the individual edge weight
- **DSU:** Used in Kruskal's for cycle detection; Prim's doesn't need DSU
- **Cut Property / Cycle Property:** Theoretical foundation for both MST algorithms
- **BFS:** Prim's on unweighted graphs reduces to BFS (all edges weight 1)

---

## ⚡ 2-Minute Revision Flash Card

- **MST:** $V-1$ edges connecting all $V$ vertices with minimum total weight
- **Prim's:** Min-heap + `inMST` array; always pick cheapest edge to unexplored vertex
- **Key invariant:** Set $S$ grows one vertex at a time; always pick min cut edge
- **Complexity:** $O((V+E)\log V)$ with binary heap; $O(V^2)$ with array (better for dense graphs)
- **Prefer over Kruskal's:** Dense graphs, adjacency matrix input, online construction
