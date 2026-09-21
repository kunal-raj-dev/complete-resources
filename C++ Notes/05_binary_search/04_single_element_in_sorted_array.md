# Lecture 20: Single Element in a Sorted Array (LeetCode 540)

> **One-Line Purpose:** Master the Even-Odd Index Parity invariant in a sorted duplicate array to locate the unique single element in $O(\log N)$ time and $O(1)$ space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #20  
> **Video ID:** `qsbCBduIs40`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=qsbCBduIs40)  
> **Duration:** 27:33  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The structure of an array where every element appears exactly twice except for one single element.
- Why the total length of the array is always odd ($2k + 1$).
- The **Index Parity Property**:
  - Before the single element: Pairs start at an **even index** and end at an **odd index** (`(even, odd)`).
  - After the single element: The disruption shifts pairs to start at an **odd index** and end at an **even index** (`(odd, even)`).
- How to eliminate half of the search space using this parity transition point.
- Boundary condition handling (`mid == 0` and `mid == n - 1`).

---

## 🔵 Lecture Content

### 1. Problem Definition
Given a sorted array consisting of only integers where every element appears exactly twice, except for one element which appears exactly once. Find this single element that appears only once. Your solution must run in $O(\log N)$ time and $O(1)$ space.

```text
Example 1:
Index:   0  1  2  3  4  5  6  7  8
Array: [ 1, 1, 2, 3, 3, 4, 4, 8, 8 ]
Output: 2

Observation of Pairs:
(1, 1) -> Indices (0, 1) [even, odd]  <-- Before single element
Single: 2 at Index 2
(3, 3) -> Indices (3, 4) [odd, even]   <-- After single element
(4, 4) -> Indices (5, 6) [odd, even]
(8, 8) -> Indices (7, 8) [odd, even]
```

---

## 2. Mathematical Insight: The Parity Invariant

1. **Left of the Unique Element:**
   - For any pair `nums[i] == nums[i+1]`, `i` is **even**.
   - Equivalently, if `mid` is even, its partner is at `mid + 1`. If `mid` is odd, its partner is at `mid - 1`.
2. **Right of the Unique Element:**
   - The pattern is inverted: For any pair `nums[i] == nums[i+1]`, `i` is **odd**.
   - If `mid` is even, its partner is at `mid - 1`. If `mid` is odd, its partner is at `mid + 1`.
3. **At the Unique Element:**
   - Neither `nums[mid - 1]` nor `nums[mid + 1]` equals `nums[mid]`. This is the target!

---

## 3. Binary Search Algorithm Step-by-Step

1. Initialize `low = 0, high = n - 1`.
2. Edge cases:
   - If `n == 1`, return `nums[0]`.
   - If `nums[0] != nums[1]`, return `nums[0]`.
   - If `nums[n - 1] != nums[n - 2]`, return `nums[n - 1]`.
3. Search in the trimmed space `low = 1, high = n - 2`:
   - Compute `mid = low + (high - low) / 2`.
   - If `nums[mid] != nums[mid - 1]` and `nums[mid] != nums[mid + 1]`, return `nums[mid]`.
   - If `(mid % 2 == 1 && nums[mid] == nums[mid - 1]) || (mid % 2 == 0 && nums[mid] == nums[mid + 1])`:
     - We are in the left half! The single element lies to the right. Set `low = mid + 1`.
   - Else:
     - We are in the right half! The single element lies to the left. Set `high = mid - 1`.

---

## 4. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int singleNonDuplicate(const vector<int>& nums) {
        int n = nums.size();
        
        // Base edge cases
        if (n == 1) return nums[0];
        if (nums[0] != nums[1]) return nums[0];
        if (nums[n - 1] != nums[n - 2]) return nums[n - 1];

        // Trimmed search space to avoid out-of-bounds checks for mid - 1 and mid + 1
        int low = 1, high = n - 2;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            // Target condition: unique element differs from both left and right neighbors
            if (nums[mid] != nums[mid - 1] && nums[mid] != nums[mid + 1]) {
                return nums[mid];
            }

            // Check if mid is in the left sorted segment:
            // Case A: mid is odd and matches previous element (even index)
            // Case B: mid is even and matches next element (odd index)
            if ((mid % 2 == 1 && nums[mid] == nums[mid - 1]) ||
                (mid % 2 == 0 && nums[mid] == nums[mid + 1])) {
                // Single element is to the right
                low = mid + 1;
            } else {
                // Single element is to the left
                high = mid - 1;
            }
        }

        return -1; // Unreachable for valid inputs
    }
};

int main() {
    Solution sol;
    vector<int> nums = {1, 1, 2, 3, 3, 4, 4, 8, 8};
    cout << "Single Element: " << sol.singleNonDuplicate(nums) << endl; // Output: 2
    return 0;
}
```

---

## 5. Complexity Analysis

- **Time Complexity:** $O(\log_2 N)$ — Search space halves at every step.
- **Space Complexity:** $O(1)$ — Only constant auxiliary variables (`low`, `high`, `mid`).

---

## ⚠️ Common Pitfalls

1. **Out of bounds access on `mid - 1` or `mid + 1`:** Handled cleanly by checking `0` and `n - 1` initially and bounding search to `[1, n - 2]`.
2. **XOR Index Trick Alternative:** Notice that if `mid` is even, `mid ^ 1 == mid + 1`. If `mid` is odd, `mid ^ 1 == mid - 1`. Thus, the condition simplifies to checking if `nums[mid] == nums[mid ^ 1]`.

---

## 🔥 Interview Questions

### Q1: Can this problem be solved with XOR in $O(N)$? Why do interviewers insist on Binary Search?
- **Answer:** XORing all elements yields the unique element in $O(N)$ time and $O(1)$ space. However, XOR ignores the **sorted order** precondition. An interviewer asks this problem specifically to test your ability to exploit monotonicity and index parity to achieve logarithmic time $O(\log N)$.

---

## Key Takeaways

1. **Parity Switch:** Pairs go from `(even, odd)` to `(odd, even)` across the unique element.
2. **Index Bitwise Trick:** `mid ^ 1` automatically maps `even -> even + 1` and `odd -> odd - 1`.
