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
