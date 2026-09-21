# Lecture 136: Floyd-Warshall Algorithm: All-Pairs Shortest Path

> **One-Line Purpose:** Compute shortest distances between every pair of vertices in a directed/undirected weighted graph via dynamic programming over intermediate nodes in $O(V^3)$ time and detect negative cycles.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #136  
> **Video ID:** `iZBXd-vjHUA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=iZBXd-vjHUA)  
> **Duration:** 27:36  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Master the ultimate All-Pairs Shortest Path (APSP) algorithm.
- Understand the DP state transition: "Is it shorter to go from A to B directly, or via K?"
- Recognize why the `k` (intermediate node) loop MUST be the outermost loop.
- Learn how to detect Negative Weight Cycles trivially from the resulting matrix.

---

## 🧠 Core Intuition — Why This Works

If you want to drive from City A to City B, you check the direct highway. But maybe going through City K is faster!
Floyd-Warshall takes this idea and scales it up using Dynamic Programming.

Let $dp[i][j]$ denote the shortest path from $i$ to $j$.
We iteratively allow a new city `k` to be used as a layover.
For every pair of cities $(i, j)$, we ask:
> "Hey, we just unlocked city $k$ as a valid layover. Is the path $i \to k \to j$ shorter than the current best path $i \to j$?"

$$dp[i][j] = \min(dp[i][j], dp[i][k] + dp[k][j])$$

If we do this for $k = 0$, then $k = 1$, all the way to $k = V-1$, by the end, we have checked all possible combinations of layovers.

**Negative Cycle Detection:**
A path from a node to itself $dp[i][i]$ is 0. If there is a negative cycle, going around that cycle and returning to $i$ will result in a negative total distance. So after running the algorithm, if *any* $dp[i][i] < 0$, the graph contains a negative cycle!

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Shortest path between all pairs"**: Direct keyword.
- **"Dense Graph ($V \le 400$)"**: $O(V^3)$ is slow. It will TLE if $V > 500$. If you see $V \le 400$ and you need paths, Floyd-Warshall is the intended solution.
- **"Transitive Closure"**: Reachability graphs (can A reach B eventually?) is a variation of this where `min` becomes `||` and `+` becomes `&&`.

---

## 📐 Algorithm Walk-Through

1. **Matrix Initialization**:
   - Create a $V \times V$ matrix `matrix`.
   - Set `matrix[i][i] = 0`.
   - Set `matrix[i][j] = weight` if an edge exists.
   - Set `matrix[i][j] = \infty` if no edge exists.
2. **The 3 Nested Loops**:
   - **Outer Loop `k` (0 to V-1)**: The intermediate "layover" node being unlocked.
   - **Middle Loop `i` (0 to V-1)**: The source node.
   - **Inner Loop `j` (0 to V-1)**: The destination node.
3. **Relaxation**:
   - `if (matrix[i][k] != \infty && matrix[k][j] != \infty)`
   - `matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])`
4. **Validation**:
   - Loop `i` from 0 to V-1. If `matrix[i][i] < 0`, flag negative cycle.

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int INF = 1e9; // Avoid INT_MAX to prevent integer overflow during addition

class FloydWarshall {
public:
    static void computeAPSP(vector<vector<int>>& matrix) {
        int V = matrix.size();

        // k MUST be the outermost loop!
        for (int k = 0; k < V; ++k) {
            for (int i = 0; i < V; ++i) {
                for (int j = 0; j < V; ++j) {
                    // Prevent overflow by checking INF before adding
                    if (matrix[i][k] != INF && matrix[k][j] != INF) {
                        matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j]);
                    }
                }
            }
        }
    }

    static bool hasNegativeCycle(const vector<vector<int>>& matrix) {
        int V = matrix.size();
        for (int i = 0; i < V; ++i) {
            if (matrix[i][i] < 0) return true;
        }
        return false;
    }
};

int main() {
    int V = 4;
    // Initial adjacency matrix representation
    vector<vector<int>> matrix = {
        {0,   3,   INF, 5},
        {2,   0,   INF, 4},
        {INF, 1,   0,   INF},
        {INF, INF, 2,   0}
    };

    FloydWarshall::computeAPSP(matrix);

    cout << "All-Pairs Shortest Path Matrix:\n";
    for (int i = 0; i < V; ++i) {
        for (int j = 0; j < V; ++j) {
            if (matrix[i][j] == INF) cout << "INF\t";
            else cout << matrix[i][j] << "\t";
        }
        cout << "\n";
    }
    
    if (FloydWarshall::hasNegativeCycle(matrix)) {
        cout << "\nWarning: Negative Cycle Detected!\n";
    }
    
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Graph Matrix Initial:**
```text
  0   1   2   3
0 0   3   ∞   5
1 2   0   ∞   4
2 ∞   1   0   ∞
3 ∞   ∞   2   0
```

**k = 0 (Unlocking node 0 as intermediate)**:
- `i=1, j=3`: Can we go `1 -> 0 -> 3`? 
  - `matrix[1][0] + matrix[0][3] = 2 + 5 = 7`.
  - Current `matrix[1][3]` is 4. `min(4, 7) = 4`. No change.
- `i=1, j=1`: `1 -> 0 -> 1`? `2 + 3 = 5`. `min(0, 5) = 0`. No change.

**k = 1 (Unlocking node 1 as intermediate)**:
- `i=0, j=2`: `0 -> 1 -> 2`? 
  - `matrix[0][1] + matrix[1][2] = 3 + \infty`. No change.
- `i=2, j=0`: `2 -> 1 -> 0`? 
  - `matrix[2][1] + matrix[1][0] = 1 + 2 = 3`. 
  - Current is $\infty$. Update `matrix[2][0] = 3`.
- `i=2, j=3`: `2 -> 1 -> 3`? 
  - `1 + 4 = 5`. Update `matrix[2][3] = 5`.

*(... skips k=2, k=3 for brevity, but matrix updates propagate)*

**Final Matrix:**
```text
0  3  7  5 
2  0  6  4 
3  1  0  5 
5  3  2  0 
```

---

## ⚠️ Common Interview Mistakes

1. **Loop Order (The biggest mistake!)**: Writing the loops as `i`, `j`, `k` instead of `k`, `i`, `j`. If `k` is inside, you only check 1-hop combinations and lock the result, missing paths that require multiple intermediate jumps. `k` **MUST** be the outermost loop.
2. **Integer Overflow with `INT_MAX`**: If you initialize missing edges as `INT_MAX`, and then do `matrix[i][k] + matrix[k][j]`, it will overflow into a massive negative number. Always use `1e9` or check `!= INF` before adding.
3. **Using Floyd-Warshall on Large Graphs**: Running an $O(V^3)$ algorithm when $V = 10^5$ will instantly TLE. If you only need Single-Source, use Dijkstra ($O(E \log V)$) or Bellman-Ford ($O(VE)$).

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $\Theta(V^3)$. Three strictly nested loops from $0$ to $V-1$.
- **Space Complexity:** $O(1)$ auxiliary space if we modify the given adjacency matrix in-place. Otherwise $O(V^2)$ to store the matrix.

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Why must the `k` loop be outermost?
**Answer:** It's DP State definition. `dp[k][i][j]` depends on `dp[k-1][i][k]` and `dp[k-1][k][j]`. By placing `k` on the outside, we guarantee that all paths using nodes $\{0 \dots k-1\}$ are fully computed and finalized before we attempt to use node $k$ as a layover. If `k` was inside, we'd use unfinalized values.

### Q2: What if we want to reconstruct the actual shortest path, not just the distance?
**Answer:** Introduce a `Next[V][V]` matrix initialized to `Next[i][j] = j`. Inside the relaxation step, when `matrix[i][k] + matrix[k][j]` is chosen, update `Next[i][j] = Next[i][k]`. You can then traverse from `i` to `j` by continually doing `u = Next[u][j]`.

### Q3: How does this compare to running Dijkstra V times?
**Answer:** Running Dijkstra from every node takes $O(V \cdot E \log V)$. On a dense graph ($E \approx V^2$), this is $O(V^3 \log V)$, making Floyd-Warshall strictly faster and much simpler to write. However, on a sparse graph ($E \approx V$), Dijkstra $V$ times is $O(V^2 \log V)$, which crushes Floyd-Warshall's $O(V^3)$. Also, Dijkstra fails on negative edges.

### Q4: How is this used for Transitive Closure?
**Answer:** Instead of distances, use a boolean matrix where `adj[i][j] = true` if an edge exists. The DP equation becomes `matrix[i][j] = matrix[i][j] || (matrix[i][k] && matrix[k][j])`. This tells you if a path exists between *any* two nodes.

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 1334: Find the City With the Smallest Number of Neighbors at a Threshold Distance](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/)** — Textbook Floyd-Warshall problem since $V \le 100$ and you need all-pairs distances.
2. **[Leetcode 399: Evaluate Division](https://leetcode.com/problems/evaluate-division/)** — Can be solved beautifully with Floyd-Warshall using multiplication instead of addition for the transitive closure of equations.

---

## 🔗 Cross-Topic Connections
- **Dynamic Programming:** This is purely a 3D DP space-optimized to 2D.
- **Bellman-Ford:** The single-source counterpart for handling negative weights.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Shortest path between ALL pairs of nodes.
- **Algorithm:** 3 nested loops. 
- **CRITICAL:** `k` (intermediate node) MUST be the outermost loop. `for(k) for(i) for(j)`.
- **Relaxation:** `dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])`.
- **Negative Cycles:** Exists if `dp[i][i] < 0` at the end.
- **Time/Space:** $\Theta(V^3)$ Time | $O(V^2)$ Space (for matrix).
