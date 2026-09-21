# Lecture 48: Rat in a Maze: Grid Pathfinding & Visited State (GFG Classical)

> **One-Line Purpose:** Master 4-directional 2D matrix pathfinding using recursive backtracking, establishing in-place visited cell marking and generating lexicographically sorted traversal paths.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #48  
> **Video ID:** `D8Yze9CDDAw`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=D8Yze9CDDAw)  
> **Duration:** 32:45  
> **Transcript:** `.transcripts/12_recursion_and_backtracking/048_Rat_in_a_Maze_Problem___Backtracking.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- How to model 2D grid pathfinding from source `(0, 0)` to destination `(n-1, n-1)` as a state-space search tree.
- Why cyclic loops occur in grid exploration and how **Visited Tracking** prevents infinite recursion.
- How to mark cells in-place (`maze[r][c] = 0`) to achieve $O(1)$ auxiliary state memory without an extra boolean matrix.
- How to generate all valid paths in strict **lexicographical order**: Down ('D'), Left ('L'), Right ('R'), Up ('U').
- How state un-marking (`maze[r][c] = 1`) during backtracking preserves valid alternative routes.

---

## 🔵 Lecture Context

Rat in a Maze is the foundational grid backtracking problem. It directly prepares you for Word Search (LeetCode 79), Number of Islands (LeetCode 200), and Robot Room Cleaner.

---

## 1. Problem Statement

A rat is positioned at `(0, 0)` in an $N \times N$ binary grid `maze` and wants to reach the destination `(N-1, N-1)`.
- `maze[i][j] == 1`: Open cell (the rat can walk here).
- `maze[i][j] == 0`: Blocked cell (wall / obstacle).

The rat can move in 4 directions:
- Down: `(r + 1, c)` with move label `'D'`
- Left: `(r, c - 1)` with move label `'L'`
- Right: `(r, c + 1)` with move label `'R'`
- Up: `(r - 1, c)` with move label `'U'`

**Goal:** Return all unique paths the rat can take in lexicographical order. If no path exists, return an empty list.

---

## 2. Core Idea: Exploration with Cycle Prevention

If the rat moves Down to `(1, 0)` and then immediately moves Up back to `(0, 0)`, it enters an infinite cycle.
To prevent this:
1. When entering cell `(r, c)`, mark it visited (set `maze[r][c] = 0` or `visited[r][c] = true`).
2. Explore moves in exact alphabetical order: `'D'`, `'L'`, `'R'`, `'U'`.
3. When backtracking out of `(r, c)`, unmark it (restore `maze[r][c] = 1`).

---

## 3. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

class Solution {
public:
    void solve(vector<vector<int>>& maze, int r, int c, int n, string& path, vector<string>& result) {
        // Base Case: Destination reached
        if (r == n - 1 && c == n - 1) {
            result.push_back(path);
            return;
        }

        // Mark current cell as visited (temporarily block it)
        maze[r][c] = 0;

        // 1. Down ('D'): (r + 1, c)
        if (r + 1 < n && maze[r + 1][c] == 1) {
            path.push_back('D');
            solve(maze, r + 1, c, n, path, result);
            path.pop_back(); // Backtrack
        }

        // 2. Left ('L'): (r, c - 1)
        if (c - 1 >= 0 && maze[r][c - 1] == 1) {
            path.push_back('L');
            solve(maze, r, c - 1, n, path, result);
            path.pop_back(); // Backtrack
        }

        // 3. Right ('R'): (r, c + 1)
        if (c + 1 < n && maze[r][c + 1] == 1) {
            path.push_back('R');
            solve(maze, r, c + 1, n, path, result);
            path.pop_back(); // Backtrack
        }

        // 4. Up ('U'): (r - 1, c)
        if (r - 1 >= 0 && maze[r - 1][c] == 1) {
            path.push_back('U');
            solve(maze, r - 1, c, n, path, result);
            path.pop_back(); // Backtrack
        }

        // Un-mark current cell (restore open state for sibling search paths)
        maze[r][c] = 1;
    }

    vector<string> findPath(vector<vector<int>>& maze, int n) {
        vector<string> result;
        // Edge cases: start or destination blocked
        if (maze[0][0] == 0 || maze[n - 1][n - 1] == 0) {
            return result;
        }

        string path = "";
        solve(maze, 0, 0, n, path, result);
        return result;
    }
};

int main() {
    Solution solver;
    vector<vector<int>> maze = {
        {1, 0, 0, 0},
        {1, 1, 0, 1},
        {1, 1, 0, 0},
        {0, 1, 1, 1}
    };

    vector<string> paths = solver.findPath(maze, 4);
    cout << "Valid Paths:\n";
    for (const string& p : paths) {
        cout << p << "\n";
    }
    return 0;
}
```

---

## 🔍 Detailed Trace: Grid `4x4`

```
Start at (0, 0).
- Move Down -> (1, 0)
- Move Down -> (2, 0)
- Move Right -> (2, 1) [Down to (3,0) is blocked!]
- Move Down -> (3, 1)
- Move Right -> (3, 2)
- Move Right -> (3, 3) [Destination reached!]
Path recorded: "DDRDRR"
```

---

## 🧠 Mental Model: Breadcrumbs

Think of marking `maze[r][c] = 0` as dropping a breadcrumb that blocks you from walking in circles. When the rat finishes exploring every possibility from that room and retreats, it picks the breadcrumb back up (`maze[r][c] = 1`) so that a different path may pass through that room if needed.

---

## ⚠️ Common Mistakes

1. **Forgetting to check Start and End:** If `maze[0][0] == 0` or `maze[n-1][n-1] == 0`, the rat cannot move at all.
2. **Missing Boundary Checks:** Accessing `maze[r+1][c]` without verifying `r + 1 < n` triggers memory access violations.
3. **Wrong Direction Order:** Exploring in non-alphabetical order (e.g. `R, D, L, U`) causes test-case failures on platforms requiring strict lexicographical output (`D, L, R, U`).

---

## 🖥️ System-Specific Notes

- **Max Path Length:** In an $N \times N$ grid, a simple path cannot exceed $N^2$ cells. For $N = 4$, the maximum recursion depth is $16$ frames, consuming negligible memory.

---

## 🟡 Additional Essential Context

Using coordinate delta arrays simplifies 4-directional code:
```cpp
const int dr[] = {1, 0, 0, -1};
const int dc[] = {0, -1, 1, 0};
const char dir[] = {'D', 'L', 'R', 'U'};
```

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why must we restore `maze[r][c] = 1` when returning?  
**A:** Because a cell might be part of multiple distinct paths! If we left it as `0`, subsequent search paths would falsely believe that cell was permanently blocked.

---

### 🔥 Interview Questions

#### Q1: What is the worst-case time complexity of Rat in a Maze?
- **Short Answer:** $O(4^{N^2})$.
- **Detailed Explanation:** At each of the $N^2$ cells, the rat can branch in up to 4 directions. In an empty grid ($N \times N$ filled with 1s), the state-space tree depth is bounded by $N^2$, leading to $O(4^{N^2})$ paths in the worst case.

---

## 💻 Output / Debugging Questions

### Output Prediction
For `maze = {{1, 1}, {1, 1}}`:  
**Output:** `"DR" "RD"`  
**Explanation:** Both paths reach `(1, 1)` from `(0, 0)`.

---

## Edge Cases

1. **$1 \times 1$ Maze:** `maze = {{1}}` $\to$ Returns `[""]`.
2. **No Path:** Returns empty list `[]`.

---

## Complexity Analysis

- **Time Complexity:** $O(4^{N^2})$ worst-case branching.
- **Auxiliary Space Complexity:** $O(N^2)$ for recursion call stack.

---

## Key Takeaways

1. **In-place marking:** Avoids extra $O(N^2)$ boolean matrix allocation.
2. **Alphabetical order:** Guarantees lexicographically sorted results.
3. **Symmetric backtrack:** Always reset cell state before function return.

---

## ⚡ 2-Minute Revision

- Order: Down ('D'), Left ('L'), Right ('R'), Up ('U').
- In-place mark: `maze[r][c] = 0`; backtrack: `maze[r][c] = 1`.
- Bounds: `0 <= r < n` and `0 <= c < n`.

---

## 🧠 Core Intuition — Grid DFS as a State-Space Tree

### Why the Order D-L-R-U Produces Lexicographic Output
Characters in alphabetical order: D < L < R < U. By trying D first, then L, R, U, we explore paths in lexicographic order of their path strings. The first valid path recorded is lexicographically smallest.

### ASCII Grid DFS Visualization: 4×4 Maze

```
Maze (1=open, 0=blocked):
[1][0][0][0]
[1][1][0][1]
[1][1][0][0]
[0][1][1][1]
Start: (0,0), End: (3,3)

Exploration trace:
(0,0) → try D → (1,0) ✓ → mark (0,0) = 0
  (1,0) → try D → (2,0) ✓ → mark (1,0) = 0
    (2,0) → try D → (3,0) ✗ [blocked]
    (2,0) → try L → (2,-1) ✗ [out of bounds]
    (2,0) → try R → (2,1) ✓ → mark (2,0) = 0
      (2,1) → try D → (3,1) ✓ → mark (2,1) = 0
        (3,1) → try D → (4,1) ✗ [out of bounds]
        (3,1) → try L → (3,0) ✗ [blocked]
        (3,1) → try R → (3,2) ✓ → mark (3,1) = 0
          (3,2) → try R → (3,3) ✓ → mark (3,2) = 0
            (3,3) → DESTINATION! Record path "DDRDRR"
          (3,2) → unmark → (3,2) = 1
        (3,1) → unmark → (3,1) = 1
      ... explore other directions from (2,1)
    (2,0) → unmark → (2,0) = 1
  (1,0) → unmark → (1,0) = 1
(0,0) → unmark → (0,0) = 1
```

### The Breadcrumb Analogy (In Depth)
When the rat enters `(r,c)`:
1. Drops a breadcrumb: `maze[r][c] = 0`
2. Explores all 4 directions
3. Picks up the breadcrumb: `maze[r][c] = 1`

Why pick it up? Cell `(r,c)` might be part of ANOTHER valid path that doesn't pass through the current path. If left as `0`, that other path would incorrectly see it as a wall.

---

## 🎯 Pattern Recognition — Grid Backtracking Problems

### Keywords That Signal This Pattern
- "Find all paths from source to destination"
- "How many unique paths" (DP version!) or "find one valid path"
- "Grid/maze traversal", "island", "connected components"
- "4-directional" or "8-directional" movement

### Grid Backtracking vs. Grid DP
| Aspect | Backtracking | Dynamic Programming |
|---|---|---|
| What to find | ALL paths, or ONE path with constraints | COUNT of paths, SHORTEST path |
| State visited? | Yes, restore on backtrack | Yes, permanent memo |
| Time | $O(4^{N^2})$ worst case | $O(N^2)$ |
| Example | Rat in Maze, Word Search | Unique Paths (LC 62), Min Path Sum (LC 64) |

### The 8-Direction Variant
For problems allowing diagonal moves (e.g., Word Search, Robot Room Cleaner):
```cpp
// 8-direction delta arrays
const int dr[] = {-1, -1, -1,  0,  0,  1,  1,  1};
const int dc[] = {-1,  0,  1, -1,  1, -1,  0,  1};
// Directions: NW, N, NE, W, E, SW, S, SE
```
Used in: Chess piece movement, flood fill with diagonals, word search in any direction.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Why must we restore `maze[r][c] = 1` when backtracking?
**Answer:** Consider a maze where the path `DDRR` uses cell `(1,1)` and path `DRD R` also uses `(1,1)`. When exploring `DDRR`, we mark `(1,1) = 0`. After recording path `DDRR` and backtracking through `(1,1)`, we restore `(1,1) = 1`. Now when exploring `DRDR`, it can correctly visit `(1,1)`. Without restoration, path `DRDR` would see `(1,1) = 0` (wall) and wrongly skip a valid path.

---

### Q2: [Complexity] What is the worst-case time complexity and when does it occur?
**Answer:** $O(4^{N^2})$ when the maze is fully open (all cells = 1). At each cell, the rat can move in up to 4 directions. With $N^2$ cells and up to 4 choices per cell, the state tree can have up to $4^{N^2}$ paths. However, the `visited` marking prevents revisiting → each path visits at most $N^2$ cells. Tighter bound: the number of simple paths in an $N \times N$ grid is much less than $4^{N^2}$ in practice.

For competitive programming: $N = 5$ gives $4^{25} \approx 10^{15}$ theoretical but ~thousands in practice due to blocked cells and visited marking.

---

### Q3: [Extension] How do you find the SHORTEST path (minimum moves) instead of all paths?
**Answer:** Replace backtracking with **BFS (Breadth-First Search)**. BFS explores cells level by level (by move count), so the first time it reaches the destination, that's the shortest path.
```cpp
#include <queue>
int shortestPath(vector<vector<int>>& maze, int n) {
    queue<pair<int,int>> q;
    q.push({0, 0});
    maze[0][0] = 0;  // Mark visited
    int moves = 0;
    const int dr[] = {1, 0, 0, -1}, dc[] = {0, -1, 1, 0};
    while (!q.empty()) {
        int sz = q.size();
        while (sz--) {
            auto [r, c] = q.front(); q.pop();
            if (r == n-1 && c == n-1) return moves;
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && maze[nr][nc] == 1) {
                    maze[nr][nc] = 0;
                    q.push({nr, nc});
                }
            }
        }
        moves++;
    }
    return -1;  // No path
}
```

---

### Q4: [Output Prediction] What is the output for `maze = {{1,1},{1,1}}` (2×2, all open)?
**Answer:** Paths are `"DR"` and `"RD"`. Trace:
- Start `(0,0)`, mark visited.
- **Try D:** Go to `(1,0)`.
  - `(1,0)` → Try D: `(2,0)` out of bounds. Try L: `(1,-1)` OOB. Try R: `(1,1)` = destination! Record `"DR"`.
  - Backtrack from `(1,1)` → unmark. Try U: `(0,0)` marked. No more.
  - Unmark `(1,0)`.
- **Try R:** Go to `(0,1)`.
  - `(0,1)` → Try D: `(1,1)` = destination! Record `"RD"`.
  - Try others... no more paths.
  - Unmark `(0,1)`.
- Output: `DR`, `RD`.

---

### Q5: [Extension] How would you handle an $N \times M$ rectangular maze (not square)?
**Answer:** Replace the single `n` dimension with separate `rows` and `cols` parameters:
```cpp
void solve(vector<vector<int>>& maze, int r, int c, int rows, int cols, 
           string& path, vector<string>& result) {
    if (r == rows - 1 && c == cols - 1) { result.push_back(path); return; }
    maze[r][c] = 0;
    const int dr[] = {1, 0, 0, -1};
    const int dc[] = {0, -1, 1, 0};
    const char dir[] = {'D', 'L', 'R', 'U'};
    for (int d = 0; d < 4; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && maze[nr][nc] == 1) {
            path.push_back(dir[d]);
            solve(maze, nr, nc, rows, cols, path, result);
            path.pop_back();
        }
    }
    maze[r][c] = 1;
}
```

---

### Q6: [Conceptual] Why is the delta array approach `{dr[], dc[], dir[]}` preferred over 4 separate `if` blocks?
**Answer:**
1. **Scalability:** Adding an 8-direction variant requires changing only the array size, not writing 4 more `if` blocks.
2. **Bug reduction:** Consistent array indexing prevents order mistakes (e.g., accidentally checking `(r+1, c+1)` twice).
3. **Direction label consistency:** The `dir[]` character array ensures the path string character always matches the actual direction taken.
4. **Code review clarity:** Interviewers can verify 4 moves at a glance without reading 4 separate `if` blocks.

---

## 📊 Complexity Analysis — Extended

### Path Length Bounds
- **Shortest path:** $N + N - 2 = 2N - 2$ moves (Manhattan distance, diagonal-free).
- **Longest simple path:** $N^2 - 1$ moves (visiting every cell exactly once — Hamiltonian path).
- **Recursion depth:** = path length ≤ $N^2 - 1$ frames.
- **Space per frame:** $O(1)$ beyond the path string → total stack $O(N^2)$.

### When to Use Backtracking vs. BFS vs. DP for Grid Problems
| Goal | Algorithm | Time |
|---|---|---|
| Find ALL paths | Backtracking | $O(4^{N^2})$ |
| Find ONE path (existence) | DFS or BFS | $O(N^2)$ |
| Find SHORTEST path (unweighted) | BFS | $O(N^2)$ |
| Count paths | DP | $O(N^2)$ |
| Find min-cost path (weighted) | Dijkstra / DP | $O(N^2 \log N)$ |

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Connection |
|---|---|---|
| GFG | Rat in a Maze | Direct — this problem (all paths) |
| 79 | Word Search | 4-direction DFS with character matching + visited marking |
| 200 | Number of Islands | 4-direction flood fill (DFS/BFS without explicit backtrack) |
| 980 | Unique Paths III | Count paths visiting all non-obstacle cells (DP + backtracking) |
| 489 | Robot Room Cleaner | 4-direction backtracking with relative direction system |

---

## 🔗 Cross-Topic Connections

- **→ Graph DFS:** Rat in Maze IS graph DFS where each cell is a node and edges connect adjacent open cells.
- **→ BFS (Shortest Path):** Replace DFS stack (recursion) with BFS queue to find shortest instead of all paths.
- **→ Dynamic Programming (Unique Paths):** When counting paths (not finding them), DP table avoids exponential exploration.
- **→ Word Search (File context):** Same DFS + visited pattern; adds character matching at each cell.
- **→ N-Queens (File 05):** Both explore a 2D grid with backtracking; N-Queens uses constraints to avoid trying invalid cells.

---

## ⚡ 2-Minute Revision Flash Card (Enhanced)

- **Mark before, unmark after:** `maze[r][c] = 0` → recurse → `maze[r][c] = 1`. Symmetric.
- **Alphabetical direction order:** D, L, R, U ensures lexicographically sorted output.
- **Edge check before access:** Always validate `0 <= nr < n && 0 <= nc < n` before `maze[nr][nc]`.
- **Find all vs. shortest:** Backtracking = all paths; BFS = shortest path. Different tools for different goals.
- **Worst case:** $O(4^{N^2})$ in fully-open maze; practical complexity far lower due to blocked cells and visited marks.
