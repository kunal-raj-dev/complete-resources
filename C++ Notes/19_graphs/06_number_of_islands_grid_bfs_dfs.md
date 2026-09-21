# Lecture 116: Number of Islands (LeetCode 200)

> **One-Line Purpose:** Count connected components in a 2D binary grid using BFS/DFS traversal with $O(M \times N)$ time and in-place grid sinking.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #116  
> **Video ID:** `AME6baBpswY`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=AME6baBpswY)  
> **Duration:** 17:05  
> **Status:** AUDITED  

---

## 🔵 Algorithmic Principle: "Island Sinking"
When encountering a `'1'` (land), increment the island counter and sink the entire connected landmass to `'0'` (water) via 4-directional DFS. This eliminates auxiliary `visited` memory.

```
Directions Array:
dRow = {-1, 1, 0, 0}
dCol = { 0, 0,-1, 1}
```

---

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <iostream>

using namespace std;

class SolutionNumberOfIslands {
private:
    void dfsSink(vector<vector<char>>& grid, int r, int c, int rows, int cols) {
        if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] != '1') {
            return;
        }

        // Sink current land cell
        grid[r][c] = '0';

        // 4-directional recursion
        dfsSink(grid, r + 1, c, rows, cols); // Down
        dfsSink(grid, r - 1, c, rows, cols); // Up
        dfsSink(grid, r, c + 1, rows, cols); // Right
        dfsSink(grid, r, c - 1, rows, cols); // Left
    }

public:
    int numIslands(vector<vector<char>>& grid) {
        if (grid.empty() || grid[0].empty()) return 0;

        int rows = grid.size();
        int cols = grid[0].size();
        int islandCount = 0;

        for (int r = 0; r < rows; ++r) {
            for (int c = 0; c < cols; ++c) {
                if (grid[r][c] == '1') {
                    islandCount++;
                    dfsSink(grid, r, c, rows, cols);
                }
            }
        }
        return islandCount;
    }
};

int main() {
    vector<vector<char>> grid = {
        {'1', '1', '0', '0', '0'},
        {'1', '1', '0', '0', '0'},
        {'0', '0', '1', '0', '0'},
        {'0', '0', '0', '1', '1'}
    };

    SolutionNumberOfIslands solver;
    cout << "Total Islands: " << solver.numIslands(grid) << endl; // Output: 3
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(M \times N)$ since every cell is visited at most 5 times (once in driver loops, 4 times from adjacent recursive checks).
- **Space Complexity:** $O(M \times N)$ worst-case recursion stack (e.g. grid filled entirely with land).

---

## 🧠 Core Intuition — Why This Works

### Real-World Analogy: Counting Continents on a Map
Imagine flying over Earth and counting continents. You spot a landmass, land on it, and explore every connected piece of land (marking it "explored" as you go). When you've explored all connected land, you take off and fly until you spot another unexplored landmass. The total number of "landing and exploring" events = number of islands.

The "sinking" trick (changing `'1'` → `'0'`) serves as an in-place visited marker — no auxiliary memory needed.

```
Initial Grid:           After sinking island 1:   After sinking island 2:
1 1 0 0 0               0 0 0 0 0                 0 0 0 0 0
1 1 0 0 0   island1→    0 0 0 0 0   island2→      0 0 0 0 0
0 0 1 0 0               0 0 1 0 0                 0 0 0 0 0
0 0 0 1 1               0 0 0 1 1                 0 0 0 1 1

Count=1                 Count=2                   Count=3 (island3 = {(3,3),(3,4)})

DFS Recursion Tree for Island 1 starting at (0,0):
  dfsSink(0,0) → sink → recurse:
    dfsSink(1,0) → sink → recurse:
      dfsSink(2,0) → out-of-bounds or '0' → return
      dfsSink(0,0) → already '0' → return
      dfsSink(1,1) → sink → recurse:
        dfsSink(2,1) → '0' → return
        dfsSink(0,1) → sink → recurse:
          all 4 neighbors '0' or OOB → return
        dfsSink(1,2) → '0' → return
        dfsSink(1,0) → already '0' → return
```

### The Key Insight: Grid as an Implicit Graph
There is no explicit adjacency list. The grid IS the graph:
- **Nodes:** Every cell `(r, c)`.
- **Edges:** 4-directional adjacency (up/down/left/right) between cells of the same type.
- **Connected component:** A maximal set of connected `'1'` cells = one island.

Counting islands = counting connected components of `'1'` cells.

---

## 🎯 Pattern Recognition — When to Use This Algorithm

| Problem Cue | Algorithm |
|---|---|
| "Count connected regions in a grid" | DFS/BFS component counting |
| "Number of islands / provinces / components" | Multi-component grid DFS |
| "Maximum area of island" | DFS returning component size |
| "Surrounded regions (fill)" | DFS from borders, then invert |
| "Connected cells that share a value" | DFS flood from matching cells |

### Grid Problems vs Graph Problems
Grid problems ARE graph problems — the grid provides implicit edges. The key adaptation:
- Replace adjacency list with bounds checking + 4-directional (or 8-directional) neighbor enumeration.
- Replace `visited[]` with either an explicit `visited[M][N]` matrix or in-place modification (`'1'` → `'0'`).

### When to Use 4-directional vs 8-directional?
- **4-directional** (up/down/left/right): "Islands" problem, "Flood Fill" — cells connect only along sides.
- **8-directional** (+ diagonals): Some variants ask "including diagonals" — use 8 directions in that case.

---

## 📐 Algorithm Walk-Through

**Invariant:** When `dfsSink(r, c)` is called, `grid[r][c]` is `'1'`. It immediately becomes `'0'`, so it cannot be visited again from any direction.

**Step-by-step trace for the 4×5 grid:**
1. Driver loop hits `(0,0)` = `'1'` → `islandCount = 1`, call `dfsSink(0,0)`.
2. `dfsSink(0,0)`: sink `(0,0)`, recurse to `(1,0)`, `(-1,0)→OOB`, `(0,1)`, `(0,-1)→OOB`.
3. Eventually sinks all of `{(0,0),(0,1),(1,0),(1,1)}` — island 1 fully sunk.
4. Driver loop continues; `(0,0)` through `(1,1)` are now `'0'` → skip.
5. Hits `(2,2)` = `'1'` → `islandCount = 2`, sink `{(2,2)}`.
6. Hits `(3,3)` = `'1'` → `islandCount = 3`, sink `{(3,3),(3,4)}`.
7. Final answer: `3`.

---

## 💻 BFS Alternative Implementation

```cpp
#include <vector>
#include <queue>
using namespace std;

class SolutionBFS {
public:
    int numIslands(vector<vector<char>>& grid) {
        if (grid.empty()) return 0;
        int rows = grid.size(), cols = grid[0].size();
        int count = 0;
        int dr[] = {-1, 1, 0, 0};
        int dc[] = {0, 0, -1, 1};

        for (int r = 0; r < rows; ++r) {
            for (int c = 0; c < cols; ++c) {
                if (grid[r][c] == '1') {
                    count++;
                    queue<pair<int,int>> q;
                    q.push({r, c});
                    grid[r][c] = '0'; // Sink immediately on enqueue

                    while (!q.empty()) {
                        auto [cr, cc] = q.front(); q.pop();
                        for (int d = 0; d < 4; ++d) {
                            int nr = cr + dr[d], nc = cc + dc[d];
                            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols
                                && grid[nr][nc] == '1') {
                                grid[nr][nc] = '0'; // Sink on enqueue
                                q.push({nr, nc});
                            }
                        }
                    }
                }
            }
        }
        return count;
    }
};
```

**BFS vs DFS for Islands:**
- BFS avoids recursion stack overflow — safer for huge grids ($M \times N = 10^6$).
- DFS is more concise.
- Both are $O(M \times N)$ time and space.

---

## ⚠️ Common Interview Mistakes

### 1. Forgetting to Sink the Current Cell Before Recursing
```cpp
// ❌ WRONG — infinite recursion! dfsSink(r,c) calls itself
void dfsSink(grid, r, c, ...) {
    for 4 directions:
        dfsSink(grid, r+dr, c+dc, ...); // Never marks current cell!
}

// ✅ CORRECT — sink first, then recurse
void dfsSink(grid, r, c, ...) {
    grid[r][c] = '0'; // Mark BEFORE recursing
    for 4 directions: ...
}
```

### 2. Off-by-One in Bounds Checking
```cpp
// ❌ WRONG — uses '<=' instead of '<'
if (r < 0 || r <= rows || c < 0 || c <= cols) return;
// Grid is 0-indexed: valid rows are [0, rows-1], so check r >= rows

// ✅ CORRECT
if (r < 0 || r >= rows || c < 0 || c >= cols) return;
```

### 3. Checking `grid[r][c] != '1'` AFTER bounds check (correct order)
The condition must be: `OOB OR not_land`. If you check `grid[r][c]` before bounds, you get undefined behavior (array out-of-bounds access).

### 4. Modifying the Input Grid Without Restoring It
The "sinking" approach permanently modifies the input. If the caller expects the grid unchanged:
```cpp
// ✅ Restore after counting (or use a separate visited matrix)
vector<vector<bool>> visited(rows, vector<bool>(cols, false));
// Use visited[][] instead of sinking
```

### 5. Using 8-Directional When Problem Says 4-Directional
Read the problem statement carefully — "horizontally or vertically adjacent" = 4-directional only. Diagonals are a separate case.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] How does "Number of Islands" relate to counting connected components in a general graph?

**Answer:** They are identical problems. The grid is an implicit undirected graph where:
- Nodes = cells $(r, c)$
- Edges = 4-directional adjacency between land cells (`'1'`)

Counting islands = counting connected components of land cells. The driver loop `for r, for c: if grid[r][c]=='1': count++; flood(r,c)` is identical in structure to the general graph component counter `for i in [0,V): if !visited[i]: count++; dfs(i)`.

The only difference: instead of an adjacency list, we have bounds-checked directional exploration.

### Q2: [Extension] How do you find the maximum area island? Modify the DFS.

**Answer:** Instead of returning `void`, return the count of cells sunk:

```cpp
int dfsSinkCount(vector<vector<char>>& grid, int r, int c, int rows, int cols) {
    if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] != '1')
        return 0;
    grid[r][c] = '0';
    return 1 + dfsSinkCount(grid, r+1, c, rows, cols)
             + dfsSinkCount(grid, r-1, c, rows, cols)
             + dfsSinkCount(grid, r, c+1, rows, cols)
             + dfsSinkCount(grid, r, c-1, rows, cols);
}

int maxAreaOfIsland(vector<vector<char>>& grid) {
    int maxArea = 0, rows = grid.size(), cols = grid[0].size();
    for (int r = 0; r < rows; ++r)
        for (int c = 0; c < cols; ++c)
            if (grid[r][c] == '1')
                maxArea = max(maxArea, dfsSinkCount(grid, r, c, rows, cols));
    return maxArea;
}
```
This is LeetCode 695 — a direct extension.

### Q3: [Variant] How would you count islands if diagonal connections also count (8-connectivity)?

**Answer:** Change the 4-directional loops to 8-directional:
```cpp
int dr[] = {-1,-1,-1, 0, 0, 1, 1, 1};
int dc[] = {-1, 0, 1,-1, 1,-1, 0, 1};
```
The algorithm remains identical — just enumerate 8 neighbors instead of 4.

### Q4: [Bug Prediction] What happens with this code on a 3×3 all-`'1'` grid?
```cpp
int numIslands(vector<vector<char>>& grid) {
    int count = 0;
    for (int r = 0; r < grid.size(); ++r)
        for (int c = 0; c < grid[0].size(); ++c)
            if (grid[r][c] == '1') {
                count++;
                // Forgot to call dfsSink!
            }
    return count;
}
```
**Answer:** Returns `9` (counts every `'1'` cell as a separate island). Without the flood-fill call to sink connected land, each individual cell is counted as its own island. The expected answer is `1` (one big island). Missing the flood-fill is one of the most common bugs.

### Q5: [System Design] If the grid is distributed across multiple machines (very large map), how would you count islands?

**Answer:** This is a distributed connected components problem. Approach:
1. **Partition:** Split the grid into vertical or horizontal strips across machines.
2. **Local computation:** Each machine runs island detection on its strip, treating border cells as "boundary islands."
3. **Merge phase:** Use a distributed Union-Find (or send boundary cell labels to a coordinator). Merge islands that share border cells across machine boundaries.
4. **Final count:** After merging, the number of root components = total islands.

This is related to the "MapReduce graph connectivity" problem. In practice, tools like Apache Spark's GraphX handle this via label propagation algorithms.

### Q6: [Complexity] Why is the time complexity $O(M \times N)$ even though DFS is called for each `'1'` cell?

**Answer:** The key insight is **amortized analysis**. Each cell `(r, c)` can be visited by DFS at most **once** — after being sunk to `'0'`, it's never visited again. Therefore:
- Total number of `dfsSink` calls = $M \times N$ (one per cell at most).
- Each call does $O(1)$ work (4 neighbor checks + sink).
- Total: $O(M \times N)$.

The driver loop itself is also $O(M \times N)$. So the overall complexity is $O(M \times N)$, not $O((M \times N)^2)$.

### Q7: [Comparison] Number of Islands vs Flood Fill — key differences?

**Answer:**
| Property | Number of Islands | Flood Fill |
|---|---|---|
| Goal | Count connected components | Recolor one connected component |
| Trigger | Count every new `'1'` found | Single starting cell `(sr, sc)` |
| What to flood | Every component | Only the component containing `(sr, sc)` |
| Output | Integer (count) | Modified grid |
| Stopping condition | Different value or OOB | Different `oldColor` or OOB |

Number of Islands floods **many** components (counting each). Flood Fill floods **exactly one** component. Flood Fill is a subroutine that Number of Islands could use (where the "flood" sinks each island).

---

## 🏆 Related LeetCode Problems

| # | Problem | Approach Hint |
|---|---|---|
| 695 | Max Area of Island | DFS returning cell count per component |
| 733 | Flood Fill | Single-component DFS recoloring |
| 130 | Surrounded Regions | DFS from borders to mark safe cells, flip rest |
| 1020 | Number of Enclaves | DFS from borders, count remaining land |
| 417 | Pacific Atlantic Water Flow | Reverse DFS from both oceans, find intersection |

---

## 🔗 Cross-Topic Connections

- **DFS (File 03):** Islands problem IS multi-component DFS on an implicit graph.
- **BFS (File 02):** BFS alternative for flooding each island — safer for deep recursion.
- **Flood Fill (File 12):** Islands problem generalized to `'0'`/`'1'` instead of color values.
- **Rotting Oranges (File 07):** Multi-source BFS on a grid — the same 4-directional grid framework.
- **Connected Components:** Islands problem in disguise — same algorithm as general graph component counting.
- **Union-Find (DSU):** Alternative approach for islands — union adjacent `'1'` cells; final answer = number of DSU roots.

---

## ⚡ 2-Minute Revision Flash Card

- **Grid = Implicit Graph:** cells are nodes; 4-directional adjacency = edges.
- **Algorithm:** For each unvisited `'1'`, increment count and DFS/BFS-sink the entire component.
- **In-place marking:** Change `'1'` → `'0'` to avoid a separate `visited[M][N]` array.
- **Bounds check FIRST:** Always check `r<0 || r>=rows || c<0 || c>=cols` before accessing `grid[r][c]`.
- **Time & Space:** $O(M \times N)$ time; $O(M \times N)$ recursion stack in worst case (all land, use BFS to avoid overflow).
