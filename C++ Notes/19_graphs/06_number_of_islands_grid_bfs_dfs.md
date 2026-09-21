# Lecture 116: Number of Islands: Matrix Connected Components (LeetCode 200)

> **One-Line Purpose:** Count disconnected component clusters in a 2D binary grid using BFS/DFS flood fill traversals.

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

## 🔵 Complete Implementation

```cpp
#include <vector>
using namespace std;

class SolutionNumIslands {
private:
    void dfs(vector<vector<char>>& grid, int r, int c, int rows, int cols) {
        if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] != '1') return;

        grid[r][c] = '0'; // Sink island to mark as visited

        dfs(grid, r + 1, c, rows, cols);
        dfs(grid, r - 1, c, rows, cols);
        dfs(grid, r, c + 1, rows, cols);
        dfs(grid, r, c - 1, rows, cols);
    }

public:
    int numIslands(vector<vector<char>>& grid) {
        int rows = grid.size();
        int cols = grid[0].size();
        int islands = 0;

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == '1') {
                    islands++;
                    dfs(grid, i, j, rows, cols);
                }
            }
        }
        return islands;
    }
};
```
- **Time Complexity:** $O(R \times C)$. Space Complexity: $O(R \times C)$.
