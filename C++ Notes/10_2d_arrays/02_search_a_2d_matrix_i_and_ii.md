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

## 🧠 Core Intuition — Why This Works
**Matrix I:** Because every row's first element is strictly greater than the last element of the previous row, the entire matrix can be imagined as one continuously sorted 1D array. By using integer division (`/ C`) and modulo (`% C`), we can map any 1D index `mid` to a 2D coordinate `(row, col)`.
**Matrix II (Staircase Search):** Since rows and columns are independently sorted, treating it as 1D fails. However, the Top-Right element `(0, C-1)` acts as a "binary search tree node". Everything to its left is smaller, and everything below it is larger. By comparing our target with this node, we can instantly eliminate an entire row (if target is larger) or an entire column (if target is smaller), stepping down a "staircase" towards the answer.

## 🎯 Pattern Recognition — When to Use This
- **Trigger cues:** "Search in a 2D matrix", "Rows and columns are sorted".
- **Keywords:** Index mapping (`mid / C`, `mid % C`), Staircase Search, BST elimination.

## 📐 Algorithm Walk-Through
**Matrix I (1D mapping):**
1. Treat matrix as 1D array of size `N = R * C`.
2. Binary search `low = 0`, `high = N - 1`.
3. `mid = (low + high) / 2`.
4. Fetch value at `matrix[mid / C][mid % C]`. Adjust `low`/`high` as usual.

**Matrix II (Staircase Search):**
1. Start at `row = 0, col = C - 1`.
2. While inside matrix bounds:
   - If `val == target`: Return true.
   - If `val > target`: `col--` (Eliminate current column because everything below is even bigger).
   - If `val < target`: `row++` (Eliminate current row because everything left is even smaller).

## 🔍 Dry Run Trace (Matrix II)
`matrix = [[1, 4], [2, 5]]`, `target = 2`
1. Start `row=0, col=1`, val = 4.
2. `4 > 2`. Eliminate column 1. `col--` -> `col=0`.
3. `row=0, col=0`, val = 1.
4. `1 < 2`. Eliminate row 0. `row++` -> `row=1`.
5. `row=1, col=0`, val = 2.
6. `2 == 2`. Return `true`.

## ⚠️ Common Interview Mistakes
- **Index mapping inversion:** Doing `matrix[mid % C][mid / C]` instead of `matrix[mid / C][mid % C]`. Remember: Division (`/`) yields the row, Modulo (`%`) yields the column.
- **Staircase starting point:** Starting at Top-Left `(0,0)` or Bottom-Right `(R-1, C-1)` doesn't work for Matrix II because both directions increase/decrease the values, making elimination impossible.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Could we start the Staircase Search from the Bottom-Left instead of Top-Right?
**Answer:** Yes! At the Bottom-Left `(R-1, 0)`, everything above is smaller, and everything to the right is larger. It works exactly the same. We just cannot start at Top-Left or Bottom-Right.

### Q2: Can we use binary search on each row for Matrix II?
**Answer:** Yes. You can iterate through all $R$ rows, and binary search each row. Time complexity would be $O(R \log C)$. However, Staircase Search is $O(R + C)$, which is strictly better for square matrices and most rectangular ones.

### Q3: How to prevent integer overflow in Matrix I `high = R * C - 1`?
**Answer:** If $R \times C$ exceeds $2^{31}-1$, you should use `long long` for `low`, `high`, and `mid` to prevent multiplication overflow before division/modulo.

## 🏆 Related Problems (Leetcode)
- **LeetCode 378:** Kth Smallest Element in a Sorted Matrix (Uses binary search on answer over the 2D value range).
- **LeetCode 1095:** Find in Mountain Array (Binary search variations).

## 🔗 Cross-Topic Connections
- **Binary Search Tree (BST):** The Staircase algorithm in Matrix II is perfectly isomorphic to searching in a BST.

## ⚡ 2-Minute Revision Flash Card
- **Matrix I:** Sorted continuously. 1D Mapping: `row = mid / C`, `col = mid % C`. Time: $O(\log(RC))$.
- **Matrix II:** Sorted rows/cols. Staircase Search.
- **Staircase Setup:** Start Top-Right `(0, C-1)` or Bottom-Left `(R-1, 0)`.
- **Staircase Logic:** If `> target`, move left (`col--`). If `< target`, move down (`row++`). Time: $O(R + C)$.
