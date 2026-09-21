# Lecture 130: Number of Provinces (LeetCode 547)

> **One-Line Purpose:** Determine the total number of connected components in an adjacency-matrix graph using Disjoint Set Union or DFS.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #130  
> **Video ID:** `J1yCPIP-K8s`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=J1yCPIP-K8s)  
> **Duration:** 12:35  
> **Status:** AUDITED  

---

## 💻 Complete C++ Implementation (DSU Approach)

```cpp
#include <vector>
#include <iostream>

using namespace std;

class SolutionProvinces {
private:
    vector<int> parent;
    int components;

    int find(int i) {
        if (i == parent[i]) return i;
        return parent[i] = find(parent[i]);
    }

    void unite(int i, int j) {
        int rootI = find(i);
        int rootJ = find(j);
        if (rootI != rootJ) {
            parent[rootI] = rootJ;
            components--;
        }
    }

public:
    int findCircleNum(vector<vector<int>>& isConnected) {
        int n = isConnected.size();
        parent.resize(n);
        for (int i = 0; i < n; ++i) parent[i] = i;
        components = n;

        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                if (isConnected[i][j] == 1) {
                    unite(i, j);
                }
            }
        }
        return components;
    }
};

int main() {
    vector<vector<int>> isConnected = {
        {1, 1, 0},
        {1, 1, 0},
        {0, 0, 1}
    };
    SolutionProvinces solver;
    cout << "Provinces: " << solver.findCircleNum(isConnected) << endl; // Output: 2
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N^2 \alpha(N))$ matrix scan.
- **Space Complexity:** $O(N)$ parent array.

---

## 🧠 Core Intuition — Why This Works

**Real-World Analogy:** Think of $N$ cities on a map. The matrix `isConnected[i][j] = 1` means city $i$ and city $j$ are directly connected. A "province" is a maximal group of cities where you can travel from any city to any other (possibly through intermediate cities). We need to count how many such isolated groups exist.

This is exactly the **connected components** problem. DSU is ideal here: start with $N$ isolated components, then merge components for each `isConnected[i][j] = 1` edge. The final `components` count is the answer.

**ASCII Visualization:**
```
isConnected matrix (3x3):
    0  1  2
0 [ 1, 1, 0 ]    → 0 and 1 are directly connected
1 [ 1, 1, 0 ]    → 1 and 0 are directly connected (symmetric)
2 [ 0, 0, 1 ]    → 2 is isolated

Initial DSU: {0} {1} {2}  → 3 components

Process (0,1): unite(0,1) → {0,1} {2}  → 2 components
Process (0,2): isConnected[0][2]=0 → skip
Process (1,2): isConnected[1][2]=0 → skip

Answer: 2 provinces ({0,1} and {2}) ✓
```

**Alternative DFS approach:**
```cpp
// DFS version - simpler to reason about, same complexity
int findCircleNum(vector<vector<int>>& isConnected) {
    int n = isConnected.size();
    vector<bool> visited(n, false);
    int provinces = 0;
    for (int i = 0; i < n; ++i) {
        if (!visited[i]) {
            dfs(i, isConnected, visited);
            provinces++;
        }
    }
    return provinces;
}
void dfs(int u, vector<vector<int>>& mat, vector<bool>& visited) {
    visited[u] = true;
    for (int v = 0; v < mat.size(); ++v)
        if (mat[u][v] == 1 && !visited[v]) dfs(v, mat, visited);
}
```

---

## 🎯 Pattern Recognition — When to Use This

**Keyword triggers from problem statements:**
- "How many groups / clusters / provinces / components?"
- "Friend circles" — classic alias for this exact problem
- Input is an **adjacency matrix** (symmetric, diagonal all 1s)
- "Are students/cities/accounts in the same group?"

**DSU vs DFS for this problem:**
| Approach | Complexity | When to prefer |
|---|---|---|
| DSU | $O(N^2 \alpha(N))$ | Dynamic queries, need component sizes |
| DFS/BFS | $O(N^2)$ | Single query, simpler code |

---

## 🔍 Dry Run Trace

**Input:** `isConnected = [[1,0,0],[0,1,1],[0,1,1]]`

```
n = 3, parent = [0,1,2], components = 3

Process i=0, j=1: isConnected[0][1]=0 → skip
Process i=0, j=2: isConnected[0][2]=0 → skip
Process i=1, j=2: isConnected[1][2]=1 → unite(1,2)
  find(1)=1, find(2)=2, different → parent[1]=2, components=2

Final components = 2 (Province 1: {0}, Province 2: {1,2})
```

---

## ⚠️ Common Interview Mistakes

1. **Using the full matrix (not upper triangle):** Since `isConnected[i][j] == isConnected[j][i]` (symmetric), iterating `j` from `0` to `n-1` instead of `i+1` to `n-1` causes every edge to be processed twice. With DSU this is harmless (unite is idempotent), but it's cleaner and faster to use `j = i+1`.

2. **Forgetting diagonal:** `isConnected[i][i] = 1` always. If you iterate from `j=0`, you'll try to `unite(i,i)` which is always the same component — harmless but wasteful.

3. **Not resetting state between test cases:** In competitive programming with multiple test cases, `parent` and `components` must be re-initialized each time.

4. **DFS stack overflow on large N:** For $N = 200$ (LeetCode constraint), DFS recursion depth can reach 200 — fine. But for larger N, use iterative DFS or BFS.

---

## 🔥 Interview Q&A — Google/Amazon/Meta Level

### Q1: [Conceptual] What's the difference between "Number of Provinces" (LC 547) and "Number of Islands" (LC 200)?
**Answer:** Both count connected components but with different representations:
- **Number of Provinces (547):** Input is an **$N \times N$ adjacency matrix** where `isConnected[i][j]=1` means nodes $i$ and $j$ are connected. Nodes are abstract (cities/friends). Time: $O(N^2)$ to process all matrix entries.
- **Number of Islands (200):** Input is a **grid** where each cell is a node. Edges are implicit (adjacent cells that are both '1'). Time: $O(M \times N)$ to scan the grid.
Both use the same underlying algorithm (DFS/BFS/DSU to count components), but the graph representation differs.

### Q2: [Extension] How would you answer "How many nodes are in the same province as node X?" efficiently?
**Answer:** Use DSU with union by **size**:
```cpp
vector<int> size(n, 1); // Track component sizes
// In unite: size[rootJ] += size[rootI]; (or vice versa)
// Query: return size[find(X)];
```
This adds $O(1)$ extra work per union and gives $O(\alpha(N))$ per size query.

### Q3: [Output Prediction] What does the DSU code print for this input?
```cpp
vector<vector<int>> mat = {{1,1,1},{1,1,1},{1,1,1}};
```
**Answer:** `1`. All three cities are mutually connected: (0,1), (0,2), and (1,2) are all 1. Processing:
- unite(0,1): components = 2
- unite(0,2): find(0) and find(2): 0's root is where 1 pointed, 2 is separate → merge, components = 1
- unite(1,2): find(1) and find(2) → same root → skip
Final: `1` province.

### Q4: [Extension] This problem has a symmetric adjacency matrix. What if the edges were directed?
**Answer:** With directed edges, "provinces" become **strongly connected components** (SCCs), not weakly connected components. Two cities are in the same directed province only if you can travel from A to B AND from B to A. Use **Kosaraju's algorithm** instead of DSU. If the question asks for weakly connected components (ignoring direction), treat edges as undirected and use DSU/DFS as before.

### Q5: [System Design] You receive 10 million "friendship" events (A and B are friends). After each event, answer: "how many friend circles exist?" Design the solution.
**Answer:** Use DSU with union by size. Per event: `unite(A, B)` in $O(\alpha(N))$. Track `components` count, decrementing when a successful union occurs. Answer is `components` after each event. Space: $O(N)$ for parent and size arrays. This handles 10M events in nearly linear time — far better than running DFS/BFS after each event ($O(N+M)$ per event = $O(NM)$ total).

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Approach |
|---|---|---|
| 547 | Number of Provinces | This problem — DSU or DFS |
| 200 | Number of Islands | DFS/BFS on 2D grid |
| 695 | Max Area of Island | DFS + area counting |
| 684 | Redundant Connection | DSU cycle detection |
| 721 | Accounts Merge | DSU + HashMap for email grouping |

---

## 🔗 Cross-Topic Connections

- **DSU (Lecture 128):** Direct application — this problem is essentially "DSU in one function"
- **BFS/DFS Connected Components:** Alternative approach; DFS solution is cleaner but DSU handles dynamic queries better
- **Tarjan's SCC:** For directed graph version where "province" means strongly connected
- **Graph Representation:** This problem uses adjacency matrix; most other graph problems use adjacency list
- **Floyd-Warshall:** Also works on adjacency matrix; could compute reachability but overkill at $O(N^3)$

---

## ⚡ 2-Minute Revision Flash Card

- **Problem:** Count connected components in an adjacency matrix graph
- **DSU approach:** Start with N components; `unite(i,j)` for each `isConnected[i][j]=1`; decrement count per successful union
- **DFS approach:** Loop over unvisited nodes, DFS each → each DFS tree = one province
- **Complexity:** $O(N^2)$ to scan matrix (both approaches)
- **Key insight:** Only scan upper triangle ($j > i$) since matrix is symmetric
