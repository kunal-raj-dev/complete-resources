# Lecture 37: Spiral Matrix (LeetCode 54)

> **One-Line Purpose:** Master 4-boundary inward shrinking loops to traverse 2D grids in clockwise spiral order.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #37  
> **Video ID:** `XMpdvwUObho`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=XMpdvwUObho)  
> **Duration:** 24:33  
> **Status:** AUDITED  

---

## 🔵 Lecture Content & Implementation

Maintain 4 pointers: `top = 0`, `bottom = r - 1`, `left = 0`, `right = c - 1`.

```cpp
#include <vector>
#include <iostream>
using namespace std;

class SolutionSpiralMatrix {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        vector<int> result;
        int top = 0, bottom = matrix.size() - 1;
        int left = 0, right = matrix[0].size() - 1;

        while (top <= bottom && left <= right) {
            // 1. Traverse Right along Top boundary
            for (int col = left; col <= right; col++) {
                result.push_back(matrix[top][col]);
            }
            top++;

            // 2. Traverse Down along Right boundary
            for (int row = top; row <= bottom; row++) {
                result.push_back(matrix[row][right]);
            }
            right--;

            // 3. Traverse Left along Bottom boundary (Check boundary validity)
            if (top <= bottom) {
                for (int col = right; col >= left; col--) {
                    result.push_back(matrix[bottom][col]);
                }
                bottom--;
            }

            // 4. Traverse Up along Left boundary (Check boundary validity)
            if (left <= right) {
                for (int row = bottom; row >= top; row--) {
                    result.push_back(matrix[row][left]);
                }
                left++;
            }
        }
        return result;
    }
};
```
- **Time Complexity:** $O(R \times C)$ — Every matrix element is visited exactly once.
- **Space Complexity:** $O(1)$ auxiliary memory (excluding returned output vector).
