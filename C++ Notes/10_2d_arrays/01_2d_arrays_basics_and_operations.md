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
