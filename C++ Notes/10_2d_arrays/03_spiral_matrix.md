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

## 🧠 Core Intuition — Why This Works
Think of the matrix as an onion with multiple rectangular layers. We can peel the onion layer by layer, starting from the outermost boundary. We use four pointers (`top`, `bottom`, `left`, `right`) to represent the current un-peeled boundary. As we traverse a side (e.g., top row moving right), we shrink that boundary (`top++`), forcing the next traversal to operate on the inner layer. We continue shrinking boundaries until they cross each other.

## 🎯 Pattern Recognition — When to Use This
- **Trigger cues:** "Print matrix in spiral order", "Generate spiral matrix", "Layer-by-layer 2D traversal".
- **Keywords:** 4 boundaries (`top`, `bottom`, `left`, `right`), Directional traversal (Right, Down, Left, Up).

## 📐 Algorithm Walk-Through
1. Initialize `top = 0`, `bottom = R - 1`, `left = 0`, `right = C - 1`.
2. Loop while `top <= bottom` AND `left <= right`:
   - **Right:** Traverse `col` from `left` to `right`. Shrink `top++`.
   - **Down:** Traverse `row` from `top` to `bottom`. Shrink `right--`.
   - **Left:** *If `top <= bottom`*, traverse `col` from `right` to `left`. Shrink `bottom--`.
   - **Up:** *If `left <= right`*, traverse `row` from `bottom` to `top`. Shrink `left++`.

## 🔍 Dry Run Trace
`matrix = [[1,2,3], [4,5,6], [7,8,9]]`
1. `T=0, B=2, L=0, R=2`
2. **Right:** push [1, 2, 3]. `T++` -> 1.
3. **Down:** push [6, 9]. `R--` -> 1.
4. **Left:** `T(1) <= B(2)`. push [8, 7]. `B--` -> 1.
5. **Up:** `L(0) <= R(1)`. push [4]. `L++` -> 1.
6. Next iteration: `T=1, B=1, L=1, R=1`.
7. **Right:** push [5]. `T++` -> 2.
8. Loop terminates because `T > B`. Output: `[1,2,3,6,9,8,7,4,5]`.

## ⚠️ Common Interview Mistakes
- **Missing secondary checks for Left and Up traversals:** When the matrix is rectangular (e.g., 3x1 or 1x3), `top` or `left` pointers might cross *inside* the `while` loop after the Right or Down traversals. If you don't re-check `if (top <= bottom)` before going Left, you will duplicate elements by traversing the same row backward.
- **Inclusive vs Exclusive boundaries:** Consistently using `<= right` and `>= left` is crucial. Mixing them up causes missed corners or out-of-bounds errors.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Why do we need the extra `if (top <= bottom)` check inside the loop when the `while` loop already checks it?
**Answer:** The `while` condition is only evaluated at the beginning of the cycle. However, inside the cycle, `top` is incremented after the Right traversal. If the remaining matrix was a single row, `top` now exceeds `bottom`. Without the internal `if` check, the Left traversal would execute and print the same row backwards, creating duplicates.

### Q2: Can this be implemented recursively?
**Answer:** Yes, you can pass the 4 boundaries to a recursive function that prints one outer layer and then calls itself with `top+1, bottom-1, left+1, right-1`. But this takes $O(\min(R,C))$ call stack space, making the iterative $O(1)$ space version strictly better.

### Q3: How do you handle generating a spiral matrix instead of reading one (LeetCode 59)?
**Answer:** The exact same 4-boundary logic applies! Instead of `result.push_back(matrix[r][c])`, you initialize an empty $N \times N$ matrix and write `matrix[r][c] = val++`.

## 🏆 Related Problems (Leetcode)
- **LeetCode 59:** Spiral Matrix II (Generate the matrix given $n$)
- **LeetCode 885:** Spiral Matrix III (Start from a given coordinate and spiral outwards)

## 🔗 Cross-Topic Connections
- **Simulation:** This is a pure array simulation problem. It tests the ability to manage state and loop invariants perfectly without relying on complex data structures.

## ⚡ 2-Minute Revision Flash Card
- **Problem:** Print matrix in spiral order.
- **Pointers:** `top`, `bottom`, `left`, `right`.
- **Flow:** Right -> Down -> Left -> Up.
- **Crucial Update:** Shrink the boundary immediately after traversing it (`top++`, `right--`, `bottom--`, `left++`).
- **Trap:** For rectangular matrices, always re-check `if (top <= bottom)` before going Left, and `if (left <= right)` before going Up.
