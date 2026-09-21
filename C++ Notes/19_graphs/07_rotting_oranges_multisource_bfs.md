# Lecture 117: Rotting Oranges: Multi-Source BFS (LeetCode 994)

> **One-Line Purpose:** Simulate concurrent wavefront decay across a grid using multi-source BFS queue initialization.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #117  
> **Video ID:** `RmXo5SWkhCs`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=RmXo5SWkhCs)  
> **Duration:** 26:22  
> **Status:** AUDITED  

---

## 🔵 Complete Implementation

```cpp
#include <vector>
#include <queue>
using namespace std;

class SolutionRottingOranges {
public:
    int orangesRotting(vector<vector<int>>& grid) {
        int rows = grid.size(), cols = grid[0].size();
        queue<pair<int, int>> q;
        int freshCount = 0;

        // Push all initially rotten oranges to queue simultaneously
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == 2) q.push({i, j});
                else if (grid[i][j] == 1) freshCount++;
            }
        }

        if (freshCount == 0) return 0;

        int minutes = -1;
        int dirs[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

        while (!q.empty()) {
            int size = q.size();
            minutes++;

            for (int k = 0; k < size; k++) {
                auto [r, c] = q.front();
                q.pop();

                for (auto& d : dirs) {
                    int nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] == 1) {
                        grid[nr][nc] = 2;
                        freshCount--;
                        q.push({nr, nc});
                    }
                }
            }
        }

        return (freshCount == 0) ? minutes : -1;
    }
};
```
