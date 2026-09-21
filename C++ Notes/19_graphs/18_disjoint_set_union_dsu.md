# Lecture 128: Disjoint Set Union (DSU / Union-Find)

> **One-Line Purpose:** Maintain partitioned sets of elements and evaluate connectivity queries in nearly $O(1)$ amortized time using Path Compression and Union by Rank/Size.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #128  
> **Video ID:** `nnrjWxWMo3E`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=nnrjWxWMo3E)  
> **Duration:** 34:04  
> **Status:** AUDITED  

---

## 🔵 Two Optimizations
1. **Path Compression:** When executing `find(i)`, point every visited node directly to the set representative root:
   ```cpp
   parent[i] = find(parent[i]);
   ```
2. **Union by Rank / Size:** Always attach the shallower tree underneath the root of the deeper tree, preventing tall skewed trees.
Combining both bounds any sequence of $M$ operations on $N$ elements to $O(M \cdot \alpha(N))$, where $\alpha(N) \le 4$ for all practical universe sizes.

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>

using namespace std;

class DisjointSet {
private:
    vector<int> parent;
    vector<int> rank;

public:
    DisjointSet(int n) {
        parent.resize(n + 1);
        rank.assign(n + 1, 0);
        for (int i = 0; i <= n; ++i) parent[i] = i;
    }

    // Find with Path Compression
    int find(int u) {
        if (u == parent[u]) return u;
        return parent[u] = find(parent[u]); // Path compression
    }

    // Union by Rank
    bool unionByRank(int u, int v) {
        int rootU = find(u);
        int rootV = find(v);

        if (rootU == rootV) return false; // Already in same set!

        if (rank[rootU] < rank[rootV]) {
            parent[rootU] = rootV;
        } else if (rank[rootU] > rank[rootV]) {
            parent[rootV] = rootU;
        } else {
            parent[rootV] = rootU;
            rank[rootU]++;
        }
        return true;
    }

    bool isConnected(int u, int v) {
        return find(u) == find(v);
    }
};

int main() {
    DisjointSet ds(5);
    ds.unionByRank(1, 2);
    ds.unionByRank(2, 3);

    cout << "1 and 3 connected: " << (ds.isConnected(1, 3) ? "YES" : "NO") << endl; // YES
    cout << "1 and 4 connected: " << (ds.isConnected(1, 4) ? "YES" : "NO") << endl; // NO
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(\alpha(N))$ amortized per operation.
- **Space Complexity:** $O(N)$ for `parent` and `rank` vectors.

---

## 🧠 Core Intuition — Why This Works

**Real-World Analogy:** Think of DSU as a **corporate org chart with self-reorganization**. Each employee reports to their manager, who reports to their manager's manager, and so on. The CEO is the "root" (set representative). When two companies merge (union), the smaller company's CEO reports to the larger company's CEO. Over time, "path compression" means every employee learns to report directly to the ultimate CEO, flattening the hierarchy to near-constant depth.

**Path Compression — Before and After:**
```
BEFORE path compression (find(5) starting from node 5):

parent: 0→0, 1→0, 2→1, 3→2, 4→3, 5→4

     0          ← root
     |
     1
     |
     2
     |
     3
     |
     4
     |
     5          ← find(5) walks up 5 steps

AFTER find(5) with path compression:

     0          ← root
   / | \ \ \
  1  2  3  4  5  ← ALL nodes point directly to root!

parent: 0→0, 1→0, 2→0, 3→0, 4→0, 5→0
Every future find() on any of these nodes = O(1)
```

**Union by Rank — Preventing Skewed Trees:**
```
NAIVE UNION (no rank) — can create O(N) deep chain:
union(1,2): 1→2
union(2,3): 1→2→3
union(3,4): 1→2→3→4   ← O(N) find depth!

UNION BY RANK — always attach smaller rank under larger rank:
union(1,2): rank[1]=rank[2]=0 → 2→1, rank[1]++  (1 becomes root)
union(3,4): rank[3]=rank[4]=0 → 4→3, rank[3]++  (3 becomes root)
union(1,3): rank[1]=rank[3]=1 → 3→1, rank[1]++

       1         ← root, rank=2
      / \
     2   3
         |
         4
Max depth = 2 = log(N). This is the O(log N) guarantee.
```

**Why $\alpha(N)$?** The inverse Ackermann function grows SO slowly that $\alpha(N) \leq 4$ for any $N \leq 10^{80}$ (larger than atoms in observable universe). For all competitive programming purposes, each operation is effectively $O(1)$.

---

## 🎯 Pattern Recognition — When to Use This

**Keyword triggers from problem statements:**
- "Connected components" + dynamic additions of edges
- "Are nodes X and Y in the same group/island/province?"
- "Detect cycle in undirected graph"
- "Kruskal's MST" (DSU is the backbone)
- "Number of islands" + online queries
- "Redundant connection" (adding an edge that creates a cycle)
- "Accounts merge" / "Friend circles" / "Provinces"

**DSU vs DFS/BFS:**
| Scenario | Prefer |
|---|---|
| Static graph, single query | DFS/BFS |
| Dynamic edge additions + repeated queries | **DSU** |
| Need to UNDO unions | Weighted DSU with rollback (offline) |
| Need actual path/component members | DFS/BFS (DSU only gives root) |

---

## 🔍 Dry Run Trace

**Operations:** `union(1,2)`, `union(3,4)`, `union(2,4)`, `find(1)`, `isConnected(1,3)`

```
Initial: parent = [0,1,2,3,4,5], rank = [0,0,0,0,0,0]

union(1,2):
  find(1)=1, find(2)=2. rank equal → parent[2]=1, rank[1]=1
  parent = [0,1,1,3,4,5]

union(3,4):
  find(3)=3, find(4)=4. rank equal → parent[4]=3, rank[3]=1
  parent = [0,1,1,3,3,5]

union(2,4):
  find(2): parent[2]=1, parent[1]=1 → root=1 (path: 2→1)
  find(4): parent[4]=3, parent[3]=3 → root=3 (path: 4→3)
  rank[1]=rank[3]=1 (equal) → parent[3]=1, rank[1]=2
  parent = [0,1,1,1,3,5]  ← 3's parent is now 1

find(1) = 1 (already root) → O(1)

isConnected(1,3):
  find(1)=1
  find(3): parent[3]=1 → root=1. PATH COMPRESSION: parent[3]=1 (already!)
  1 == 1 → TRUE (they are connected!)

After all operations, parent = [0,1,1,1,3,5]
                                      ↑
                              3 directly points to root 1
                              Next find(4): 4→3→1, compressed to 4→1
```

---

## ⚠️ Common Interview Mistakes

1. **Using only Path Compression (no Union by Rank):** Path compression alone gives $O(\log N)$ amortized. Without union by rank, the tree can become a chain. The **combination** gives $O(\alpha(N))$.

2. **Using only Union by Rank (no Path Compression):** Union by rank alone gives $O(\log N)$ per operation — still good, but not optimal. Always use both.

3. **Off-by-one in initialization:** If nodes are 1-indexed, initialize `parent` of size `n+1` and loop from 0 to n inclusive. Missing node 0 or n is a common bug.

4. **Checking cycle with wrong condition:**
   ```cpp
   // WRONG: unite returns void, checking if same set BEFORE union
   if (!ds.unionByRank(u, v)) { /* cycle detected */ }  // Actually correct!
   // But forgetting to CHECK the return value of unionByRank:
   ds.unionByRank(u, v);  // Bug: silently ignores cycle!
   ```
   `unionByRank` returns `false` when both nodes are already in the same set (cycle!). Always use the return value.

5. **Calling find() multiple times on same node:** Each call may do path compression differently. Always store the result: `int rootU = find(u); int rootV = find(v);`

6. **Union by Size vs Union by Rank:** Union by size tracks actual subtree size; union by rank tracks tree height upper bound. Both give the same $O(\alpha(N))$ complexity but union by size is slightly more cache-friendly in practice. Competitive programming tends to use union by rank.

---

## 🔥 Interview Q&A — Google/Amazon/Meta Level

### Q1: [Proof] Prove that union by rank alone gives O(log N) depth.
**Answer:** **Claim:** After any sequence of unions by rank, the height of a tree with rank $r$ has at least $2^r$ nodes.  
**Proof by induction:** Base: rank 0 tree has 1 node $\geq 2^0 = 1$. ✓  
**Inductive step:** When we merge two trees of rank $r$ (resulting in rank $r+1$), each has $\geq 2^r$ nodes, so the merged tree has $\geq 2^r + 2^r = 2^{r+1}$ nodes. ✓  
**Consequence:** A tree of rank $r$ has at least $2^r$ nodes, so rank $\leq \log_2 N$. Since find() cost = depth ≤ rank, find is $O(\log N)$ with union by rank alone.

### Q2: [Conceptual] What happens if you use only path compression without union by rank?
**Answer:** Path compression alone gives $O(\log N)$ amortized per operation (not $O(\alpha(N))$). Without union by rank, unions can create chains of depth $O(N)$. The first `find()` on the deepest node takes $O(N)$ and compresses the path. But without rank control, future unions may re-create deep chains. Tarjan proved that path compression alone gives $O(M \log N)$ for $M$ operations — good but not optimal. The combination with union by rank achieves the theoretical optimal $O(M \alpha(N))$.

### Q3: [Extension] How would you implement DSU that supports UNDO (rollback) operations?
**Answer:** Standard path compression makes rollback impossible (it destroys the original tree structure). Solution: Use **union by rank WITHOUT path compression**. Track a history stack of `(node, old_parent, old_rank)` tuples for each union operation. To rollback, pop from the stack and restore. This gives $O(\log N)$ per operation (no path compression) but supports offline undo. This technique is used in "offline dynamic connectivity" problems where edges are both added and removed.

### Q4: [Output Prediction] What does this buggy DSU output?
```cpp
DisjointSet ds(4);
ds.unionByRank(1, 2);
ds.unionByRank(1, 3);
ds.unionByRank(1, 4);
// Now find(4) — what's the parent chain?
cout << ds.find(4); // What's the parent[4]?
```
**Answer:** `parent[2]=1` (rank[1] becomes 1), `parent[3]=1` (rank stays 1 since rank[1]>rank[3]=0 wait — rank[3]=0, rank[1]=1, so parent[3]=1), `parent[4]=1` (rank[1]=1 > rank[4]=0, so parent[4]=1). Every node directly points to 1. `find(4)` returns 1 after following `4→1`. With path compression, this is already optimal after the first find.

### Q5: [System Design] Design a system to detect if a new friendship connection makes two previously unconnected social network clusters merge. Support 10M users with O(1) amortized per query.
**Answer:** Use DSU with path compression + union by rank. `union(userA, userB)` merges their components; returns `true` if they were separate (merger event), `false` if already connected. Additional feature: track component size in a `size[]` array updated during union. Total space: $O(N) = O(10M)$ which is ~80MB for int arrays — fine. For persistence (checking "what was the state 3 months ago"), use offline DSU with rollback (union by rank only, no path compression) or a persistent data structure. For real-time queries, the standard DSU gives $O(\alpha(N)) \approx O(1)$ amortized.

### Q6: [Conceptual] What is the difference between Union by Rank and Union by Size?
**Answer:** 
- **Union by Rank:** `rank` is an upper bound on tree height. When merging equal-rank trees, attach one under the other and increment the new root's rank. Rank may overestimate actual height (after path compression flattens things).
- **Union by Size:** `size` tracks actual number of nodes. Always attach smaller tree under larger tree's root. Update: `size[rootBig] += size[rootSmall]`.
- **Performance:** Both give the same $O(\alpha(N))$ complexity when combined with path compression. Union by size is more intuitive and used in problems where you need to know component sizes (e.g., "max component size after each union").

### Q7: [Coding] Implement DSU with union by size and a method to return the size of any node's component.
```cpp
class DSU {
    vector<int> parent, size;
public:
    DSU(int n) : parent(n), size(n, 1) {
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int x) {
        if (x != parent[x]) parent[x] = find(parent[x]);
        return parent[x];
    }
    bool unite(int x, int y) {
        x = find(x); y = find(y);
        if (x == y) return false;
        if (size[x] < size[y]) swap(x, y);
        parent[y] = x;
        size[x] += size[y];
        return true;
    }
    int componentSize(int x) { return size[find(x)]; }
};
```
**Answer:** The `size` array stores component size only at the root. `componentSize(x)` first finds the root via `find(x)` (with path compression), then returns `size[root]`. Sizes of non-root nodes become meaningless after unions but we never read them directly.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Approach |
|---|---|---|
| 547 | Number of Provinces | DSU or DFS to count connected components |
| 684 | Redundant Connection | DSU — first edge causing `find(u)==find(v)` is redundant |
| 721 | Accounts Merge | DSU on email nodes; group by root |
| 990 | Satisfiability of Equality Equations | DSU with '==' edges; verify '!=' edges after |
| 1202 | Smallest String With Swaps | DSU groups swappable indices; sort each group |

---

## 🔗 Cross-Topic Connections

- **Kruskal's MST:** DSU is the cycle-detection backbone; `unionByRank` returns false → edge creates cycle → skip it
- **Graph Connectivity:** DSU answers "are X and Y connected?" in $O(\alpha(N))$; equivalent to BFS/DFS component checking but faster for repeated queries
- **Percolation Problem:** Classic application; detect when a grid "percolates" (top connects to bottom) as cells are opened — each cell is a DSU node, opening a cell unions it with open neighbors
- **Tarjan's Algorithms:** Use DFS timestamp arrays instead of DSU for bridge/AP detection; different mechanism, same "connectivity" theme
- **Network Flow:** Sometimes uses DSU to merge nodes or track augmenting paths in union-find trees

---

## ⚡ 2-Minute Revision Flash Card

- **Two optimizations:** Path compression (flatten to root) + Union by rank (attach smaller tree under deeper root)
- **Combined complexity:** $O(\alpha(N)) \approx O(1)$ amortized — $\alpha(4) \leq$ even for $N = 10^{80}$
- **`find(u)`:** Returns root of component; path compresses on the way up
- **`unionByRank(u,v)`:** Returns `false` if already same set → cycle detection!
- **When to use:** Dynamic connectivity, Kruskal's MST, cycle detection in undirected graphs
