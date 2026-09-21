# Lecture 122: Flood Fill Algorithm (LeetCode 733)

> **One-Line Purpose:** Recolor a 4-directionally connected matrix component from a start coordinate `(sr, sc)` to a new color using DFS/BFS in $O(M \times N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #122  
> **Video ID:** `JI_e2RzARbM`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=JI_e2RzARbM)  
> **Duration:** 15:10  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Map 2D matrix traversal problems to standard Graph Traversals (DFS/BFS).
- Safely handle edge conditions and matrix boundaries.
- Understand how to prevent infinite recursion traps in connected-component algorithms.
- Simulate real-world applications (like the MS Paint bucket tool).

---

## 🧠 Core Intuition — Why This Works

This algorithm is exactly how the "Paint Bucket" tool works in MS Paint or Photoshop. 
When you click on a pixel, the computer looks at the color of that pixel. It then changes that pixel to the new color, and checks the 4 immediate neighbors (Up, Down, Left, Right). If a neighbor has the *same original color*, it paints that one too, and spreads outwards continuously. 

**Graph Mapping:**
- **Nodes**: Each cell `(r, c)` in the 2D matrix.
- **Edges**: Implicit connections between a cell and its 4 adjacent neighbors (Top, Bottom, Left, Right) IF they share the same color.
- **Traversal**: DFS (recursive depth-first exploration) or BFS (queue-based outward ripples). DFS is typically shorter to code.

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Matrix/Grid of characters/colors"**: Searching for blocks of connected identical items.
- **"Island problems"**: Connected 1s (land) surrounded by 0s (water). Flood Fill is the underlying engine for counting or measuring islands.
- **"Spreading" or "Contagion"**: Fire burning a forest, disease spreading through neighbors, water flowing.

---

## 📐 Algorithm Walk-Through

1. **Safety Check**: If the target pixel `(sr, sc)` already has the `newColor`, immediately return. Doing this prevents an infinite loop!
2. **Record Original State**: Store `oldColor = image[sr][sc]`. This is the color we need to match as we spread.
3. **DFS Function**:
   - **Base Cases (Stop spreading)**:
     - Out of bounds: `r < 0`, `c < 0`, `r >= rows`, `c >= cols`.
     - Color mismatch: `image[r][c] != oldColor`.
   - **Action**: Change `image[r][c] = newColor`.
   - **Recursive Spreading**: Call DFS on `(r+1, c)` [Down], `(r-1, c)` [Up], `(r, c+1)` [Right], `(r, c-1)` [Left].
4. **Return**: The matrix is modified in-place. Return it.

---

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <iostream>

using namespace std;

class SolutionFloodFill {
private:
    void dfs(vector<vector<int>>& image, int r, int c, int oldColor, int newColor, int rows, int cols) {
        if (r < 0 || r >= rows || c < 0 || c >= cols || image[r][c] != oldColor) {
            return;
        }

        image[r][c] = newColor;

        dfs(image, r + 1, c, oldColor, newColor, rows, cols); // Down
        dfs(image, r - 1, c, oldColor, newColor, rows, cols); // Up
        dfs(image, r, c + 1, oldColor, newColor, rows, cols); // Right
        dfs(image, r, c - 1, oldColor, newColor, rows, cols); // Left
    }

public:
    vector<vector<int>> floodFill(vector<vector<int>>& image, int sr, int sc, int color) {
        int oldColor = image[sr][sc];
        
        // Critical: Guard against infinite recursion if new color == old color!
        if (oldColor == color) return image; 

        dfs(image, sr, sc, oldColor, color, image.size(), image[0].size());
        return image;
    }
};

int main() {
    vector<vector<int>> img = {
        {1, 1, 1},
        {1, 1, 0},
        {1, 0, 1}
    };
    SolutionFloodFill solver;
    solver.floodFill(img, 1, 1, 2);
    
    cout << "Recolored Matrix:\n";
    for(const auto& row : img) {
        for(int val : row) cout << val << " ";
        cout << "\n";
    }
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Input:**
```text
image = [[1, 1, 1],
         [1, 1, 0],
         [1, 0, 1]]
sr = 1, sc = 1, newColor = 2
```
`oldColor` = `image[1][1]` = 1. `newColor` = 2.

1. **DFS(1, 1)**: `image[1][1] == 1`. Change to 2. Matrix:
   `[1, 1, 1]`, `[1, 2, 0]`, `[1, 0, 1]`
   - Call Down: `DFS(2, 1)` -> `image[2][1] == 0`. Returns (not 1).
   - Call Up: `DFS(0, 1)` -> `image[0][1] == 1`.
2. **DFS(0, 1)**: Change to 2.
   - Call Down: `DFS(1, 1)` -> `image[1][1] == 2`. Returns (not 1).
   - Call Up: `DFS(-1, 1)` -> Out of bounds. Returns.
   - Call Right: `DFS(0, 2)` -> `image[0][2] == 1`. 
3. **DFS(0, 2)**: Change to 2. 
   - (Explores neighbors, changes nothing more, returns).
   - Call Left from `DFS(0,1)`: `DFS(0, 0)` -> `image[0][0] == 1`.
4. **DFS(0, 0)**: Change to 2.
   - Call Down: `DFS(1, 0)` -> `image[1][0] == 1`.
5. **DFS(1, 0)**: Change to 2.
   - Call Down: `DFS(2, 0)` -> `image[2][0] == 1`.
6. **DFS(2, 0)**: Change to 2.
   - Explores neighbors, all fail or are 2 already. Returns.
7. Stack unwinds. Final Matrix:
   ```text
   [[2, 2, 2],
    [2, 2, 0],
    [2, 0, 1]]
   ```

---

## ⚠️ Common Interview Mistakes

1. **Missing the `oldColor == newColor` check**: If you don't check this, and the target pixel is ALREADY the `newColor`, `image[r][c] = newColor` doesn't change it. So when DFS recurses on its neighbors and comes back, it thinks the cell still needs processing. **Result: Infinite Recursion / Stack Overflow!**
2. **Bounds Checking Order**: Writing `image[r][c] != oldColor` BEFORE `r < 0 || r >= rows` will cause an array out-of-bounds segfault. Always put boundary checks FIRST so C++ short-circuits the `||` operator.
3. **8-Directional vs 4-Directional**: Ensure you clarify with the interviewer if diagonals count as "connected." Usually, flood fill is 4-directional, but Minesweeper or Word Search variants might be 8.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(M \times N)$ where $M$ is rows, $N$ is cols. In the worst case (the entire matrix is the `oldColor`), we visit every cell exactly once.
- **Space Complexity:** $O(M \times N)$ in the worst case for the recursive call stack (if the matrix forms a long snake-like path of 1s).

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Is it better to use BFS or DFS for Flood Fill?
**Answer:** In competitive programming, DFS is faster to type and has slightly less overhead. In production (or if the matrix is enormous, say 100,000 x 100,000), DFS can cause a Stack Overflow. BFS (using a queue) is strictly safer for massive grids because it allocates memory on the Heap, bypassing the OS call stack limits.

### Q2: How can we implement this without modifying the input array?
**Answer:** If the input array is read-only, you must allocate a `visited` matrix `vector<vector<bool>> visited(m, vector<bool>(n, false))` and return a deep copy of the original array with the changes applied.

### Q3: What happens if we don't pass `image` by reference?
**Answer:** If `vector<vector<int>> image` is passed by value (`void dfs(vector<vector<int>> image...)`), C++ copies the entire 2D array on *every single recursive call*. This destroys Performance and blows up Memory to $O((MN)^2)$. ALWAYS pass large structures by reference `&`.

### Q4: If I want to find the boundary (perimeter) of the flooded region, how would I adapt this?
**Answer:** Inside your DFS, keep a global or reference counter `perimeter = 0`. Whenever you hit an out-of-bounds coordinate OR a cell with a different color (a `0` if you're on `1`s), increment `perimeter++`. This is a classic Google question (Island Perimeter).

### Q5: How would you solve this iteratively if you can't use recursion (DFS) or a queue (BFS)?
**Answer:** You can implement DFS iteratively using an explicit `std::stack<pair<int, int>>`. This behaves exactly like recursive DFS but stores the state on the heap rather than the call stack, preventing stack overflow.

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 200: Number of Islands](https://leetcode.com/problems/number-of-islands/)** — Exactly the same DFS logic, but you run it from every unvisited `1` to count components.
2. **[Leetcode 130: Surrounded Regions](https://leetcode.com/problems/surrounded-regions/)** — Run flood fill only from the edges of the matrix to mark "safe" regions.
3. **[Leetcode 695: Max Area of Island](https://leetcode.com/problems/max-area-of-island/)** — Keep a running `size` counter inside your DFS and return the max.
4. **[Leetcode 463: Island Perimeter](https://leetcode.com/problems/island-perimeter/)** — Calculate the perimeter while traversing.

---

## 🔗 Cross-Topic Connections
- **Graphs (Implicit):** A 2D grid is an implicit graph where max degree is 4. Matrix traversals are one of the most common graph categories.
- **Stacks vs Queues:** Demonstrates how choice of data structure (Call Stack vs Queue) changes traversal behavior (DFS depth vs BFS ripple) even if the final result is the same.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Color a connected component in a 2D grid.
- **Trap 1:** Infinite Loop. ALWAYS check `if (newColor == oldColor) return;`.
- **Trap 2:** Segfaults. Check matrix boundaries `r < 0 || c < 0 || r >= R || c >= C` BEFORE accessing `image[r][c]`.
- **Algorithm:** 
  1. Record start color.
  2. Change current cell color.
  3. Recurse 4 directions (Up, Down, Left, Right).
- **Time/Space:** $O(M \times N)$ Time | $O(M \times N)$ Space (Call stack).
