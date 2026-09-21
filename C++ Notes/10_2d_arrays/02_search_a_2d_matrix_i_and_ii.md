# Lecture 36: Search a 2D Matrix: Variations I & II (LeetCode 74 & 240)

> **One-Line Purpose:** Master virtual 1D index mapping for strictly sorted matrices ($O(\log(RC))$) and top-right staircase reduction for row/col sorted matrices ($O(R+C)$).

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #36  
> **Video ID:** `LEFFjgt5i6w`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=LEFFjgt5i6w)  
> **Duration:** 37:43  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- **Search 2D Matrix I (LeetCode 74):** Each row is sorted, and the first element of each row is strictly greater than the last element of the previous row. Treat as a single flattened 1D array of size $R \times C$.
- **Search 2D Matrix II (LeetCode 240):** Rows and columns are sorted independently. Standard binary search on answer does not apply directly. Use the **Staircase Search** starting from Top-Right `(0, C-1)`.

---

## 🔵 Lecture Content

### 1. Variation I: Virtual 1D Binary Search (LeetCode 74)

Coordinate transform formulas:
$$\text{row} = \lfloor \text{mid} / C \rfloor, \quad \text{col} = \text{mid} \pmod C$$

```cpp
#include <vector>
#include <iostream>
using namespace std;

class SolutionSearchMatrixI {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int r = matrix.size();
        int c = matrix[0].size();
        int low = 0, high = r * c - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;
            int val = matrix[mid / c][mid % c];

            if (val == target) return true;
            else if (val < target) low = mid + 1;
            else high = mid - 1;
        }
        return false;
    }
};
```
- **Time Complexity:** $O(\log(R \times C)) = O(\log R + \log C)$.
- **Space Complexity:** $O(1)$.

---

### 2. Variation II: Staircase Search (LeetCode 240)

Start at the **Top-Right corner** `(row = 0, col = c - 1)`:
- If `matrix[row][col] == target`, target found.
- If `matrix[row][col] > target`, the entire column contains elements greater than target $\implies \text{col}--$.
- If `matrix[row][col] < target`, the entire row contains elements smaller than target $\implies \text{row}++$.

```cpp
class SolutionSearchMatrixII {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int r = matrix.size();
        int c = matrix[0].size();
        int row = 0, col = c - 1;

        while (row < r && col >= 0) {
            if (matrix[row][col] == target) return true;
            else if (matrix[row][col] > target) col--; // Eliminate column
            else row++;                               // Eliminate row
        }
        return false;
    }
};
```
- **Time Complexity:** $O(R + C)$ — In every step, either `row` increments or `col` decrements.
- **Space Complexity:** $O(1)$.
