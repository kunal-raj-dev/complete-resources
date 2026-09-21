# Lecture 136: Floyd-Warshall Algorithm: All-Pairs Shortest Path

> **One-Line Purpose:** Compute shortest paths between every pair of vertices in $O(V^3)$ time via 2D dynamic programming relaxation.

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

## 🔵 Implementation & Negative Cycle Detection

$$\text{matrix}[i][j] = \min(\text{matrix}[i][j], \text{matrix}[i][k] + \text{matrix}[k][j])$$

```cpp
#include <vector>
#include <algorithm>
using namespace std;

void floydWarshall(vector<vector<int>>& matrix) {
    int n = matrix.size();

    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (matrix[i][k] != 1e9 && matrix[k][j] != 1e9) {
                    matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j]);
                }
            }
        }
    }

    // Negative Cycle check: if any diagonal element becomes negative
    // matrix[i][i] < 0 indicates negative cycle reachable from i
}
```
- **Time Complexity:** $O(V^3)$. Space Complexity: $O(1)$ auxiliary (in-place matrix).
