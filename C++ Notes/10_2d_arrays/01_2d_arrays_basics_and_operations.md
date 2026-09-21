# Lecture 35: 2D Arrays in C++: Memory Layout & Diagonal Operations

> **One-Line Purpose:** Master 2D contiguous heap and stack buffer layouts in Row-Major order, boundary scanning, and optimal single-pass diagonal sum computation.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #35  
> **Video ID:** `lBL8327gq8I`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=lBL8327gq8I)  
> **Duration:** 37:31  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- How 2D arrays are flattened in physical RAM using **Row-Major Order**: $\text{Address}(arr[i][j]) = \text{Base} + (i \times C + j) \times \text{sizeof(Type)}$.
- Row-wise vs column-wise traversals and why row-wise traversal maximizes CPU cache hits.
- Linear search and maximum row/col sum patterns.
- Matrix Diagonal Sum: Computing the sum of Primary Diagonal ($i = j$) and Secondary Diagonal ($j = N - 1 - i$) in a single $O(N)$ pass without double-counting the center element when $N$ is odd.

---

## 🔵 Lecture Content

### 1. Row-Major Memory Flattening
In C++, a 2D array `int matrix[R][C]` is physically stored as a single contiguous block of $R \times C \times 4$ bytes.
Row $0$ occupies the first $C$ elements, followed immediately by Row $1$, and so on.

### 2. Matrix Diagonal Sum ($O(N)$ Single Pass)

```cpp
#include <vector>
#include <iostream>
using namespace std;

class SolutionDiagonal {
public:
    int diagonalSum(vector<vector<int>>& mat) {
        int n = mat.size();
        int sum = 0;

        for (int i = 0; i < n; i++) {
            // Primary diagonal: (i, i)
            sum += mat[i][i];

            // Secondary diagonal: (i, n - 1 - i)
            // Prevent double-counting the center element in odd-sized matrices
            if (i != n - 1 - i) {
                sum += mat[i][n - 1 - i];
            }
        }
        return sum;
    }
};
```
- **Time Complexity:** $O(N)$ — Exactly 1 loop of $N$ iterations instead of nested $O(N^2)$.
- **Space Complexity:** $O(1)$.


## 🧠 Core Intuition — Why This Works
Unlike 1D arrays, 2D arrays (matrices) are accessed using two coordinates: rows and columns. However, physical memory is strictly 1-dimensional. The compiler seamlessly maps the 2D coordinate `(r, c)` into a 1D offset using the formula `r * total_cols + c`. Traversing row-by-row is extremely fast because it matches this physical memory layout, maximizing CPU cache hits.

## 🎯 Pattern Recognition — When to Use This
- **Trigger cues:** "Grid", "Matrix", "Rows and Columns", "Board games (Tic-Tac-Toe, Sudoku)".
- **Keywords:** Row-major order, diagonal traversal, matrix sum.

## 📐 Algorithm Walk-Through
**Diagonal Sum Algorithm ($O(N)$ pass):**
1. Given an $N \times N$ matrix.
2. Initialize `sum = 0`.
3. Loop $i$ from 0 to $N-1$:
   - Add primary diagonal element: `sum += mat[i][i]`.
   - Add secondary diagonal element: `sum += mat[i][N - 1 - i]`.
   - **Crucial check:** If $i == N - 1 - i$, the element is at the exact center (occurs only for odd $N$). Do not add it twice!

## 🔍 Dry Run Trace
**Matrix:**
`[[1, 2, 3],`
` [4, 5, 6],`
` [7, 8, 9]]` (Size $N=3$)

- **i = 0:**
  - Primary: `mat[0][0] = 1`. `sum = 1`.
  - Secondary: `mat[0][2] = 3`. `0 != 2`, so add. `sum = 4`.
- **i = 1:**
  - Primary: `mat[1][1] = 5`. `sum = 9`.
  - Secondary: `mat[1][1] = 5`. `1 == 1`! Skip adding secondary to avoid double counting.
- **i = 2:**
  - Primary: `mat[2][2] = 9`. `sum = 18`.
  - Secondary: `mat[2][0] = 7`. `2 != 0`, so add. `sum = 25`.
- **Final Sum:** 25. Correct! (1+5+9 + 3+7).

## ⚠️ Common Interview Mistakes
- **Double-Counting the Center:** In odd-sized matrices, failing to add the `i != N - 1 - i` check results in the center element being added twice.
- **Column-Major Traversal:** Traversing a matrix column-by-column (inner loop for rows, outer for columns) in C++ can cause massive cache misses and slow down execution significantly for large matrices.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Why is row-wise traversal faster than column-wise in C++?
**Answer:** C++ stores 2D arrays in Row-Major order (elements of the same row are contiguous in physical RAM). Modern CPUs load memory in chunks called Cache Lines. Row-wise traversal accesses elements sequentially, maximizing cache hits. Column-wise traversal jumps across memory addresses, causing frequent Cache Misses.
### Q2: How do you dynamically allocate a 2D array in C++?
**Answer:** Using a vector of vectors: `vector<vector<int>> matrix(R, vector<int>(C, 0));` or using double pointers: `int** arr = new int*[R]; for(int i=0; i<R; i++) arr[i] = new int[C];`.

## 🏆 Related Problems (Leetcode)
- **LeetCode 1572:** Matrix Diagonal Sum (Exact implementation)
- **LeetCode 867:** Transpose Matrix (Swapping rows and columns)
- **LeetCode 73:** Set Matrix Zeroes (Modifying rows and cols based on values)

## 🔗 Cross-Topic Connections
- **Graphs:** Adjacency matrices are 2D arrays used to represent graph edges.
- **Dynamic Programming:** 2D arrays are extensively used to store states in DP problems like Longest Common Subsequence or Knapsack.

## ⚡ 2-Minute Revision Flash Card
- **Row-Major Memory:** `Address = Base + (i * Cols + j) * size`.
- **Cache Efficiency:** Always traverse row-by-row in C++.
- **Primary Diagonal:** Coordinates `(i, i)`.
- **Secondary Diagonal:** Coordinates `(i, N - 1 - i)`.
- **Diagonal Sum Trap:** Check `i != N - 1 - i` to prevent counting the center twice in odd $N \times N$ matrices.
