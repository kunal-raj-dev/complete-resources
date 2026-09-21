# Lecture 129: Kruskal's Algorithm: Minimum Spanning Tree

> **One-Line Purpose:** Find the Minimum Spanning Tree by sorting all edges by ascending weight and greedily adding edges that do not form cycles using Disjoint Set Union in $O(E \log E)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #129  
> **Video ID:** `inoM6jwj1CA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=inoM6jwj1CA)  
> **Duration:** 29:07  
> **Status:** AUDITED  

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct Edge {
    int u, v, weight;
    bool operator<(const Edge& other) const {
        return weight < other.weight;
    }
};

class KruskalMST {
private:
    vector<int> parent;
    vector<int> rank;

    int find(int i) {
        if (i == parent[i]) return i;
        return parent[i] = find(parent[i]);
    }

    bool unite(int u, int v) {
        int rootU = find(u);
        int rootV = find(v);
        if (rootU == rootV) return false;

        if (rank[rootU] < rank[rootV]) parent[rootU] = rootV;
        else if (rank[rootU] > rank[rootV]) parent[rootV] = rootU;
        else {
            parent[rootV] = rootU;
            rank[rootU]++;
        }
        return true;
    }

public:
    int minimumSpanningTree(int V, vector<Edge>& edges) {
        sort(edges.begin(), edges.end()); // O(E log E)

        parent.resize(V);
        rank.assign(V, 0);
        for (int i = 0; i < V; ++i) parent[i] = i;

        int totalWeight = 0;
        int edgesUsed = 0;

        for (const auto& e : edges) {
            if (unite(e.u, e.v)) {
                totalWeight += e.weight;
                edgesUsed++;
                if (edgesUsed == V - 1) break;
            }
        }

        return totalWeight;
    }
};

int main() {
    int V = 4;
    vector<Edge> edges = {
        {0, 1, 10}, {0, 2, 6}, {0, 3, 5},
        {1, 3, 15}, {2, 3, 4}
    };

    KruskalMST solver;
    cout << "Kruskal MST Cost: " << solver.minimumSpanningTree(V, edges) << endl; // Output: 19
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(E \log E)$ sorting dominate $O(E \alpha(V))$ DSU operations.
- **Space Complexity:** $O(V)$ for DSU parent and rank tables.

---

## 🧠 Core Intuition — Why This Works

**Real-World Analogy:** Imagine building the cheapest highway network between $V$ cities. You have a list of all possible roads with their construction costs. Kruskal says: **sort roads by cost, cheapest first. For each road, build it UNLESS it creates a redundant connection** (a "shortcut" between cities already reachable by existing roads). Stop when all cities are connected.

The "cycle detection" is key: if $u$ and $v$ are already connected (same DSU component), adding edge $(u,v)$ would create a cycle. We skip it. This greedy approach is provably optimal by the **Cycle Property**: for any cycle $C$, the maximum-weight edge in $C$ is NOT in any MST (assuming unique weights).

**ASCII Visualization — Step-by-Step:**
```
Edges sorted by weight:
(2,3,4) (0,3,5) (0,2,6) (0,1,10) (1,3,15)

Initial: each city is its own component
{0} {1} {2} {3}

Step 1: Process (2,3,4):
  find(2)=2, find(3)=3 → DIFFERENT! → Add edge, MST cost=4
  Components: {0} {1} {2,3}

  0       1       2---3
                  (cost 4)

Step 2: Process (0,3,5):
  find(0)=0, find(3)=3 (root of {2,3})=2 or 3? Let's say 3
  DIFFERENT! → Add edge, MST cost=9
  Components: {0,2,3} {1}

  0---3---2       1
    (5) (4)

Step 3: Process (0,2,6):
  find(0)=root of {0,2,3}, find(2)=same root → SAME! → SKIP (would form cycle)

Step 4: Process (0,1,10):
  find(0)=root of {0,2,3}, find(1)=1 → DIFFERENT! → Add edge, MST cost=19
  Components: {0,1,2,3}

  0---3---2
  |   (5)(4)
  1
 (10)

edgesUsed = V-1 = 3 → DONE! MST cost = 19 ✓
```

---

## 🎯 Pattern Recognition — When to Use This

**Keyword triggers from problem statements:**
- "Minimum spanning tree" on a **sparse graph**
- "Minimum cost to connect all nodes" with edge list input
- "Find redundant edge in spanning tree" (Kruskal's naturally identifies the cycle-causing edge)
- Already have a **sorted edge list**
- Problems where you need to process edges from cheapest to most expensive (greedy by weight)

**Kruskal's vs Prim's Decision:**
| Criterion | Kruskal's | Prim's |
|---|---|---|
| Graph density | Sparse ($E \ll V^2$) | Dense ($E \approx V^2$) |
| Input format | Edge list | Adjacency list/matrix |
| Implementation | Simpler with DSU | Needs min-heap |
| Already sorted? | $O(E\alpha(V))$ | No advantage |
| Disconnected graphs | Finds forest, easy to detect | Requires multiple starts |

---

## 🔍 Dry Run Trace

**Input:** V=4, edges: `{(2,3,4), (0,3,5), (0,2,6), (0,1,10), (1,3,15)}` (already sorted)

```
parent=[0,1,2,3], rank=[0,0,0,0], totalWeight=0, edgesUsed=0

Process (2,3,4):
  find(2)=2, find(3)=3 ≠ → unite: parent[3]=2, rank[2]=1
  parent=[0,1,2,2], totalWeight=4, edgesUsed=1

Process (0,3,5):
  find(0)=0, find(3): parent[3]=2, parent[2]=2 → root=2 ≠ 0
  unite: rank[0]=0 < rank[2]=1 → parent[0]=2
  parent=[2,1,2,2], totalWeight=9, edgesUsed=2

Process (0,2,6):
  find(0): parent[0]=2, parent[2]=2 → root=2 (path compress: parent[0]=2 ✓)
  find(2)=2 → SAME ROOT! Skip (cycle)

Process (0,1,10):
  find(0)=2, find(1)=1 ≠ → unite: rank[2]=1 > rank[1]=0 → parent[1]=2
  parent=[2,2,2,2], totalWeight=19, edgesUsed=3

edgesUsed == V-1=3 → BREAK
Final MST cost = 19 ✓
```

---

## ⚠️ Common Interview Mistakes

1. **Sorting by wrong field:** Always sort by `weight`, not by `u` or `v`. The comparator must compare `weight` only:
   ```cpp
   // WRONG: sorts by u first (lexicographic)
   bool operator<(const Edge& o) const { return u < o.u; }
   // CORRECT: sorts by weight
   bool operator<(const Edge& o) const { return weight < o.weight; }
   ```

2. **Forgetting early termination:** After adding $V-1$ edges, the MST is complete. Without `if (edgesUsed == V-1) break;`, we wastefully process all remaining edges.

3. **Re-initializing DSU for each call:** In competitive programming, the `parent` and `rank` vectors must be reset for each test case. If using a class, reset in the `minimumSpanningTree` function, not in the constructor.

4. **Disconnected graph:** If the graph has multiple components, Kruskal's builds a **minimum spanning forest** (one tree per component). `edgesUsed` will be `< V-1`. Always check connectivity.

5. **Duplicate edges:** If the input has duplicate edges (same u, v, different weights), Kruskal's naturally handles them — only the cheapest one (processed first) could be added.

6. **Negative edge weights:** Kruskal's handles negative weights correctly! The sort still works, and the MST with negative edges just has a potentially negative total weight.

---

## 🔥 Interview Q&A — Google/Amazon/Meta Level

### Q1: [Proof] Why is Kruskal's greedy approach correct (Cycle Property proof)?
**Answer:** **Cycle Property:** For any cycle $C$ in graph $G$, the maximum weight edge $e^*$ in $C$ is NOT in any MST (assuming unique weights). **Proof:** Suppose for contradiction that MST $T$ contains $e^* = (u,v)$ with weight $w^*$. Since $T$ is a tree, removing $e^*$ splits $T$ into two components $T_1$ and $T_2$. Since the cycle $C$ contains both $u$ and $v$, there must be another edge $e' \in C \setminus T$ connecting $T_1$ and $T_2$ with weight $w' < w^*$ (since $e^*$ is the max in $C$). Replacing $e^*$ with $e'$ gives a spanning tree with smaller total weight — contradicting $T$ being the MST. Therefore $e^*$ is not in any MST. Kruskal's skips exactly the maximum edge of each cycle (the edge that would complete it), so it's correct.

### Q2: [Comparison] Kruskal's $O(E \log E)$ vs Prim's $O((V+E)\log V)$ — which is faster asymptotically?
**Answer:** 
- $E \log E \approx E \log V^2 = 2E \log V = O(E \log V)$
- So Kruskal's is $O(E \log V)$ and Prim's heap is $O((V+E)\log V)$
- For sparse graphs ($E = O(V)$): Both are $O(V \log V)$
- For dense graphs ($E = O(V^2)$): Kruskal's is $O(V^2 \log V)$; Prim's with array is $O(V^2)$ — Prim's wins!
- With Fibonacci heap: Prim's achieves $O(E + V \log V)$, theoretically optimal
- **Practical conclusion:** For sparse graphs, both are similar. For dense graphs, use Prim's $O(V^2)$ array version.

### Q3: [Extension] How do you find all MSTs when edge weights may not be unique?
**Answer:** When weights are not unique, multiple MSTs may exist. The "matroid intersection" theory tells us that all MSTs have the same multiset of edge weights. To enumerate all MSTs: find one MST, then for each non-MST edge $e$, find the path in the MST between $e$'s endpoints (the "fundamental cycle"). Any edge in this cycle with the same weight as $e$ can be swapped with $e$ to produce another valid MST. This generates all MSTs by pairwise swaps of equal-weight edge pairs.

### Q4: [Critical Edge] How do you find if edge $(u,v,w)$ is in EVERY possible MST?
**Answer:** Edge $(u,v,w)$ is in every MST if and only if it is the **unique** minimum weight edge crossing some cut, or more precisely: it is the unique minimum weight edge in the fundamental cycle of any spanning tree. Algorithm: Find the MST. If the edge is in the MST, check if there's another edge with the same weight connecting the same two components. If no such edge exists, it's "critical" (in every MST). This is a key idea behind LeetCode 1489 (Critical and Pseudo-Critical Edges in MST).

### Q5: [Coding] How would you modify Kruskal's to return the actual MST edges, not just the total weight?
```cpp
vector<Edge> getMSTEdges(int V, vector<Edge>& edges) {
    sort(edges.begin(), edges.end());
    // ... DSU initialization ...
    vector<Edge> mstEdges;
    for (const auto& e : edges) {
        if (unite(e.u, e.v)) {
            mstEdges.push_back(e);
            if ((int)mstEdges.size() == V - 1) break;
        }
    }
    return mstEdges; // V-1 edges forming the MST
}
```

### Q6: [Debugging] What does this code print for a disconnected graph with 4 vertices and only 2 edges?
```cpp
vector<Edge> edges = {{0,1,5}, {2,3,3}};
KruskalMST solver;
cout << solver.minimumSpanningTree(4, edges);
```
**Answer:** Prints `8`. The code adds both edges (since they connect different components), giving `totalWeight = 5+3 = 8`. But `edgesUsed = 2 ≠ V-1 = 3`, meaning the graph is disconnected (forms a **spanning forest** with 2 trees, not a spanning tree). The code doesn't detect this — it returns the forest cost. To detect disconnectedness: check `if (edgesUsed < V-1)` after the loop.

### Q7: [Conceptual] Why is DSU preferred over DFS for cycle detection in Kruskal's?
**Answer:** For each edge in Kruskal's, we need to check "do $u$ and $v$ already belong to the same component?" Options:
- **DFS:** $O(V+E)$ per edge → Total $O(E(V+E))$ — way too slow.
- **Simple adjacency list search:** $O(V)$ per edge → Total $O(EV)$ — still slow.
- **DSU:** $O(\alpha(V))$ per edge → Total $O(E\alpha(V))$ — essentially $O(E)$.
DSU's near-constant time per query is the reason Kruskal's overall complexity is dominated by the sort ($O(E \log E)$) rather than the union-find operations.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Approach |
|---|---|---|
| 1135 | Connecting Cities With Minimum Cost | Classic Kruskal's MST |
| 1489 | Find Critical and Pseudo-Critical Edges | Kruskal's + edge inclusion/exclusion testing |
| 684 | Redundant Connection | Kruskal's — first edge where `unite()` returns false |
| 1061 | Lexicographically Smallest Equivalent String | DSU with lexicographic root preference |
| 1631 | Path With Minimum Effort | Binary search + Kruskal-style edge processing |

---

## 🔗 Cross-Topic Connections

- **DSU:** The heart of Kruskal's — cycle detection via `find()` comparison
- **Prim's Algorithm:** Complementary MST approach; vertex-centric vs edge-centric
- **Sorting:** Kruskal's is fundamentally a sorted-edge-greedy algorithm
- **Cycle Property / Cut Property:** Theoretical foundation proving correctness
- **Borůvka's Algorithm:** Third MST algorithm; useful for parallel computation
- **Spanning Forest:** When graph is disconnected, Kruskal's naturally finds the minimum spanning forest

---

## ⚡ 2-Minute Revision Flash Card

- **3 Steps:** Sort edges by weight → iterate edges → use DSU to skip cycle-forming edges
- **Complexity:** $O(E \log E)$ sort + $O(E\alpha(V))$ DSU = $O(E \log E)$ total
- **Cycle detection:** `unite(u,v)` returns `false` → same component → skip edge
- **Termination:** Stop after exactly $V-1$ edges added (spanning tree complete)
- **Best for:** Sparse graphs, edge-list input, when DSU already available
