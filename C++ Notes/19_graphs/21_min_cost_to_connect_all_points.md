# Lecture 131: Min Cost to Connect All Points (LeetCode 1584)

> **One-Line Purpose:** Connect 2D coordinates with a minimal Manhattan distance spanning tree using Prim's algorithm in $O(N^2)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #131  
> **Video ID:** `mEx8JJQJUs8`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=mEx8JJQJUs8)  
> **Duration:** 21:16  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Model geometric 2D point clouds as fully connected (complete) dense graphs.
- Understand Manhattan Distance as an edge weight.
- Optimize Prim's Algorithm from $O(E \log V)$ to $O(V^2)$ when $E \approx V^2$.
- Build an intuition for Minimum Spanning Trees (MST) in networking/wiring contexts.

---

## 🧠 Core Intuition — Why This Works

Imagine you are laying fiber optic cables to connect a set of buildings. You don't need a direct cable between every single pair of buildings; you just need every building to be connected to the grid *somehow*. To save money, you want the absolute minimum total length of cable.

This is the exact definition of a **Minimum Spanning Tree (MST)**.

**Why $O(N^2)$ Prim's instead of Kruskal's?**
Since every point can connect to every other point, this is a **Complete Graph**. 
Number of vertices $V = N$. Number of edges $E \approx N^2 / 2$.
- Kruskal's runs in $O(E \log E) = O(N^2 \log (N^2)) = O(N^2 \log N)$.
- Standard Prim's (with Min-Heap) runs in $O(E \log V) = O(N^2 \log N)$.
- **Optimized Prim's (Dense Graph):** By finding the minimum distance manually in an array (without a heap), we can do it in $O(V^2) = O(N^2)$. For complete graphs, dropping the heap logarithmic factor is strictly faster!

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Connect all X with minimum cost"**: Classic MST phrasing.
- **"Every point can connect to every other point"**: Implies a dense/complete graph.
- **"Manhattan distance" / $|x_1 - x_2| + |y_1 - y_2|$**: Used to implicitly calculate edge weights on the fly rather than storing a massive $N \times N$ adjacency matrix.

---

## 📐 Algorithm Walk-Through (Dense Prim's)

1. **Initialization**: 
   - `minDist` array of size $N$ initialized to $\infty$. (Tracks the shortest edge connecting an unvisited node to the MST).
   - `inMST` boolean array of size $N$ initialized to `false`.
   - Set `minDist[0] = 0` (start from the first point).
2. **Main Loop ($N$ times)**:
   - **Find Min**: Iterate through all $N$ nodes to find the unvisited node `u` with the smallest `minDist[u]`.
   - **Include in MST**: Mark `inMST[u] = true`. Add `minDist[u]` to our `totalCost`.
   - **Relax Neighbors**: For every *unvisited* node `v` from $0$ to $N-1$:
     - Calculate the Manhattan distance `dist` between `u` and `v`.
     - Update `minDist[v] = min(minDist[v], dist)`.
3. **Return**: `totalCost`.

*(Note: We never explicitly build the adjacency matrix. We calculate weights on demand!)*

---

## 💻 Complete C++ Implementation (Optimized Prim's $O(N^2)$)

```cpp
#include <vector>
#include <cmath>
#include <climits>
#include <iostream>

using namespace std;

class SolutionMinCostConnectPoints {
public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        int n = points.size();
        vector<int> minDist(n, INT_MAX);
        vector<bool> inMST(n, false);

        minDist[0] = 0;
        int totalCost = 0;

        for (int step = 0; step < n; ++step) {
            int u = -1;
            
            // 1. Find the unvisited node with the smallest distance to the MST
            for (int i = 0; i < n; ++i) {
                if (!inMST[i] && (u == -1 || minDist[i] < minDist[u])) {
                    u = i;
                }
            }

            // 2. Add it to the MST
            inMST[u] = true;
            totalCost += minDist[u];

            // 3. Relax distances to all remaining unvisited points
            for (int v = 0; v < n; ++v) {
                if (!inMST[v]) {
                    int dist = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1]);
                    minDist[v] = min(minDist[v], dist);
                }
            }
        }

        return totalCost;
    }
};

int main() {
    vector<vector<int>> points = {{0, 0}, {2, 2}, {3, 10}, {5, 2}, {7, 0}};
    SolutionMinCostConnectPoints solver;
    cout << "Min Cost: " << solver.minCostConnectPoints(points) << endl; // Output: 20
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Points:** `A(0,0)`, `B(2,2)`, `C(3,10)`, `D(5,2)`, `E(7,0)`. $N=5$.
Initialization: `minDist` = `[0, \infty, \infty, \infty, \infty]`

**Step 1:**
- Min unvisited is `A(0)`. `inMST[0] = true`. `totalCost = 0`.
- Relax neighbors:
  - `dist(A,B)` = $|0-2|+|0-2| = 4`. `minDist[1] = 4`.
  - `dist(A,C)` = 13. `minDist[2] = 13`.
  - `dist(A,D)` = 7. `minDist[3] = 7`.
  - `dist(A,E)` = 7. `minDist[4] = 7`.
- `minDist` = `[0, 4, 13, 7, 7]`

**Step 2:**
- Min unvisited is `B(1)` (cost 4). `inMST[1] = true`. `totalCost = 4`.
- Relax neighbors of B:
  - `dist(B,C)` = $|2-3|+|2-10| = 9$. `minDist[2] = min(13, 9) = 9`.
  - `dist(B,D)` = $|2-5|+|2-2| = 3$. `minDist[3] = min(7, 3) = 3`.
  - `dist(B,E)` = $|2-7|+|2-0| = 7$. `minDist[4] = min(7, 7) = 7`.
- `minDist` = `[0, 4, 9, 3, 7]`

**Step 3:**
- Min unvisited is `D(3)` (cost 3). `inMST[3] = true`. `totalCost = 4 + 3 = 7`.
- Relax neighbors of D:
  - `dist(D,C)` = 10. `minDist[2] = min(9, 10) = 9`.
  - `dist(D,E)` = 4. `minDist[4] = min(7, 4) = 4`.
- `minDist` = `[0, 4, 9, 3, 4]`

**Step 4:**
- Min unvisited is `E(4)` (cost 4). `inMST[4] = true`. `totalCost = 7 + 4 = 11`.
- Relax neighbors of E:
  - `dist(E,C)` = 14. `minDist[2] = min(9, 14) = 9`.

**Step 5:**
- Min unvisited is `C(2)` (cost 9). `inMST[2] = true`. `totalCost = 11 + 9 = 20`.

**Final Cost:** 20.

---

## ⚠️ Common Interview Mistakes

1. **Using a Priority Queue (Heap)**: Most students auto-code Prim's using `priority_queue`. Here, pushing $O(N^2)$ edges to a heap causes $O(N^2 \log N)$ time and $O(N^2)$ space (Memory Limit Exceeded on LeetCode for $N=1000$). The $O(N^2)$ array approach uses $O(N)$ space and runs faster.
2. **Pre-computing the Adjacency Matrix**: Creating an $N \times N$ matrix to store distances before running Prim's will cost $O(N^2)$ space. Calculate distances on the fly to keep space at $O(N)$.
3. **Confusing Prim's and Dijkstra's**: Dijkstra relaxes paths from the *source* (`dist[u] + weight < dist[v]`). Prim's relaxes the path to the *tree itself* (`weight < minDist[v]`). Don't add the current path sum!

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N^2)$. The outer loop runs $N$ times. Finding the minimum takes $O(N)$. Relaxing takes $O(N)$. $N \times (N + N) = O(N^2)$.
- **Space Complexity:** $O(N)$ for `minDist` and `inMST` arrays. Very memory efficient!

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Would Kruskal's algorithm work here?
**Answer:** Yes, but it would be suboptimal. You would have to generate all $\frac{N(N-1)}{2}$ edges, sort them in $O(E \log E) = O(N^2 \log N)$ time, and then apply Union-Find. Not only is it slower logarithmically, but generating all edges requires $O(N^2)$ space.

### Q2: What if the points were in 3D or D-dimensional space?
**Answer:** The algorithm remains exactly the same. You just update the distance calculation formula to sum the absolute differences across all $D$ dimensions. The time complexity becomes $O(D \cdot N^2)$.

### Q3: How do you trace/reconstruct the actual edges of the MST?
**Answer:** Introduce a `parent` array of size $N$. When you update `minDist[v] = dist` during the relaxation step, simultaneously update `parent[v] = u`. The MST edges will be `(parent[i], i)` for $i \neq 0$.

### Q4: If a new point is added dynamically, can we update the MST efficiently?
**Answer:** This is a hard problem (Dynamic MST). Generally, adding a node requires checking the distance to all existing nodes $O(N)$, adding it to the MST, and potentially finding the maximum edge on the cycle it forms to remove it. This takes $O(N)$ time, rather than a full $O(N^2)$ recalculation.

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 1135: Connecting Cities With Minimum Cost (Premium)](https://leetcode.com/problems/connecting-cities-with-minimum-cost/)** — Standard MST where edges are given explicitly.
2. **[Leetcode 1168: Optimize Water Distribution in a Village (Premium)](https://leetcode.com/problems/optimize-water-distribution-in-a-village/)** — MST with a twist (virtual "source" node for building wells).
3. **[Leetcode 1489: Find Critical and Pseudo-Critical Edges in MST](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/)** — Deeper MST properties using Kruskal's.

---

## 🔗 Cross-Topic Connections
- **Greedy Algorithms:** Both Prim's and Kruskal's are fundamentally greedy algorithms that make locally optimal choices (cheapest edge) that guarantee a globally optimal spanning tree.
- **Dijkstra's Algorithm:** Prim's array-optimized version is structurally identical to array-optimized Dijkstra's, differing only in the relaxation equation.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** MST of a complete graph given $N$ coordinates.
- **Why Array-Prim's?** Avoids $O(N^2 \log N)$ time and $O(N^2)$ space of heap-based Prim/Kruskal.
- **Algorithm (Greedy):** 
  1. Start at node 0.
  2. Pick the unvisited node closest to the *current MST*.
  3. Mark visited, add distance to cost.
  4. Update distances from the new node to all remaining unvisited nodes.
- **Distance:** Calculate "on the fly", don't store in a matrix.
- **Time / Space:** $O(N^2)$ Time | $O(N)$ Space.
