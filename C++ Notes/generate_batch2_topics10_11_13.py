import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def write_files(base_dir, files_dict):
    os.makedirs(base_dir, exist_ok=True)
    for fname, content in files_dict.items():
        fpath = os.path.join(base_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Wrote {fpath}")

# ==========================================
# TOPIC 10: 2D ARRAYS (L35 - L37)
# ==========================================
t10_dir = os.path.join(root, "10_2d_arrays")
t10_files = {}

t10_files["01_2d_arrays_basics_and_operations.md"] = r"""# Lecture 35: 2D Arrays in C++: Memory Layout & Diagonal Operations

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
"""

t10_files["02_search_a_2d_matrix_i_and_ii.md"] = r"""# Lecture 36: Search a 2D Matrix: Variations I & II (LeetCode 74 & 240)

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
"""

t10_files["03_spiral_matrix.md"] = r"""# Lecture 37: Spiral Matrix (LeetCode 54)

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
"""

t10_files["00_master_index.md"] = r"""# Topic 10: 2D Arrays — Master Index

> **Domain:** Multi-Dimensional Memory Layouts, Virtual Index Binary Search, Staircase Pruning, and Spiral Boundary Invariants

---

## 📋 Topic Overview

This module covers 2D grid processing in C++. Starting from physical Row-Major RAM layout and single-loop diagonal summation, it addresses logarithmic search in strictly sorted matrices, $O(R+C)$ staircase reduction, and boundary-managed spiral traversals.

---

## 📑 Lecture Index

| # | Lecture Title | Focus Areas | Notes Link | Status |
|---|---|---|---|---|
| **35** | 2D Arrays in C++ | Row-major layout, memory address formula, cache performance, diagonal sum | [01_2d_arrays_basics_and_operations.md](./01_2d_arrays_basics_and_operations.md) | **AUDITED** |
| **36** | Search a 2D Matrix (I & II) | Virtual 1D binary search ($O(\log(RC))$), Staircase search ($O(R+C)$) | [02_search_a_2d_matrix_i_and_ii.md](./02_search_a_2d_matrix_i_and_ii.md) | **AUDITED** |
| **37** | Spiral Matrix | 4-boundary shrinking (`top`, `bottom`, `left`, `right`), single-line matrix edge cases | [03_spiral_matrix.md](./03_spiral_matrix.md) | **AUDITED** |

---

## 🎯 Topic Revision & Interview Preparation
- **Topic Quick Revision:** [topic_revision.md](./topic_revision.md)
- **Topic Interview Question Bank:** [topic_interview_questions.md](./topic_interview_questions.md)
"""

t10_files["topic_revision.md"] = r"""# ⚡ Rapid Revision — Topic 10: 2D Arrays

> **Target:** 5-minute pre-interview refresher on 2D array coordinates and matrix algorithms.

---

## 🔑 Key Matrix Formulas
- **Virtual 1D to 2D:** `row = idx / cols`, `col = idx % cols`.
- **Search Matrix I:** Flattened binary search in $O(\log(R \times C))$.
- **Search Matrix II:** Start at `(0, C - 1)`. If `val > target` $\implies \text{col}--$; if `val < target` $\implies \text{row}++$.
- **Spiral Invariant:** Must guard bottom and left passes with `if (top <= bottom)` and `if (left <= right)`.
"""

t10_files["topic_interview_questions.md"] = r"""# 💼 Topic Interview Question Bank — Topic 10: 2D Arrays

---

### Q1: Why can't we start Staircase Search at (0, 0) or (R - 1, C - 1)?
**Answer:**
At `(0, 0)`, moving right increases value, and moving down *also* increases value. If target is greater than `matrix[0][0]`, we cannot know whether to proceed right or down (non-deterministic branching).
At `(0, C - 1)` (or `(R - 1, 0)`), one direction strictly decreases value (left) while the other strictly increases value (down). This eliminates an entire row or column deterministically in $O(1)$.
"""

write_files(t10_dir, t10_files)

# ==========================================
# TOPIC 11: HASHING & PREFIX SUMS (L38 - L41)
# ==========================================
t11_dir = os.path.join(root, "11_hashing")
t11_files = {}

t11_files["01_two_sum_duplicate_repeating_missing.md"] = r"""# Lecture 38: Two Sum, Find Duplicate & Repeating/Missing Values

> **One-Line Purpose:** Master hash map complement lookups, Floyd's cycle detection on array indices, and algebraic sum/sum-of-squares formulas for repeating and missing values.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #38  
> **Video ID:** `0Fxc_jKj2vo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=0Fxc_jKj2vo)  
> **Duration:** 53:30  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- **Two Sum (LeetCode 1):** One-pass hash map complement matching in $O(N)$ time.
- **Find the Duplicate Number (LeetCode 287):** Pointer cycling via Floyd's Tortoise and Hare algorithm in $O(N)$ time and $O(1)$ space without mutating the array.
- **Find Repeating & Missing Values:** Solve via frequency hashing or mathematical equation system ($\sum x$ and $\sum x^2$).

---

## 🔵 Lecture Content & Implementations

### 1. Two Sum (One-Pass Hash Map)
```cpp
#include <vector>
#include <unordered_map>
using namespace std;

class SolutionTwoSum {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> mp;
        for (int i = 0; i < nums.size(); i++) {
            int complement = target - nums[i];
            if (mp.count(complement)) {
                return {mp[complement], i};
            }
            mp[nums[i]] = i;
        }
        return {};
    }
};
```

---

### 2. Find Duplicate Number: Floyd's Cycle Detection ($O(1)$ Space)
Since numbers are in range $[1, n]$ and array has $n + 1$ elements, each index forms a linked-list node where `next = nums[curr]`. A duplicate value indicates two indices pointing to the same node $\implies$ cycle entry point!

```cpp
class SolutionFindDuplicate {
public:
    int findDuplicate(vector<int>& nums) {
        int slow = nums[0];
        int fast = nums[0];

        // Phase 1: Detect cycle
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);

        // Phase 2: Find entrance to cycle
        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }
};
```
- **Time Complexity:** $O(N)$. Space Complexity: $O(1)$ without modifying the input array.
"""

t11_files["02_three_sum_two_pointer_optimal.md"] = r"""# Lecture 39: 3 Sum: Sorting & Two Pointers (LeetCode 15)

> **One-Line Purpose:** Master two-pointer inward scanning with comprehensive duplicate skipping to identify all unique zero-sum triplets in $O(N^2)$ time and $O(1)$ auxiliary space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #39  
> **Video ID:** `K-RsltkN63w`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=K-RsltkN63w)  
> **Duration:** 43:43  
> **Status:** AUDITED  

---

## 🔵 Lecture Content & Implementation

```cpp
#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;

class SolutionThreeSum {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int>> res;
        int n = nums.size();
        sort(nums.begin(), nums.end()); // Crucial: Sort first

        for (int i = 0; i < n - 2; i++) {
            // Optimization: If smallest element is > 0, three positive numbers cannot sum to 0
            if (nums[i] > 0) break;

            // Skip duplicates for the first element
            if (i > 0 && nums[i] == nums[i - 1]) continue;

            int left = i + 1;
            int right = n - 1;

            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];

                if (sum == 0) {
                    res.push_back({nums[i], nums[left], nums[right]});

                    // Skip duplicates for left and right
                    while (left < right && nums[left] == nums[left + 1]) left++;
                    while (left < right && nums[right] == nums[right - 1]) right--;

                    left++;
                    right--;
                } else if (sum < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }
        return res;
    }
};
```
- **Time Complexity:** $O(N \log N + N^2) = O(N^2)$.
- **Space Complexity:** $O(1)$ auxiliary (excluding output).
"""

t11_files["03_four_sum_two_pointer_optimal.md"] = r"""# Lecture 40: 4 Sum: Optimal Multi-Pointer Reduction (LeetCode 18)

> **One-Line Purpose:** Extend two-pointer quadratic reduction to 4-quadruplet discovery with 64-bit integer overflow protection.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #40  
> **Video ID:** `X6sL8JTROLY`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=X6sL8JTROLY)  
> **Duration:** 23:02  
> **Status:** AUDITED  

---

## 🔵 Lecture Content & Implementation

```cpp
#include <vector>
#include <algorithm>
using namespace std;

class SolutionFourSum {
public:
    vector<vector<int>> fourSum(vector<int>& nums, int target) {
        vector<vector<int>> res;
        int n = nums.size();
        sort(nums.begin(), nums.end());

        for (int i = 0; i < n - 3; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;

            for (int j = i + 1; j < n - 2; j++) {
                if (j > i + 1 && nums[j] == nums[j - 1]) continue;

                int left = j + 1;
                int right = n - 1;

                while (left < right) {
                    // Use 64-bit integer to prevent overflow during sum
                    long long sum = (long long)nums[i] + nums[j] + nums[left] + nums[right];

                    if (sum == target) {
                        res.push_back({nums[i], nums[j], nums[left], nums[right]});
                        while (left < right && nums[left] == nums[left + 1]) left++;
                        while (left < right && nums[right] == nums[right - 1]) right--;
                        left++;
                        right--;
                    } else if (sum < target) {
                        left++;
                    } else {
                        right--;
                    }
                }
            }
        }
        return res;
    }
};
```
- **Time Complexity:** $O(N^3)$.
- **Space Complexity:** $O(1)$ auxiliary.
"""

t11_files["04_subarray_sum_equals_k_prefix_sum.md"] = r"""# Lecture 41: Subarray Sum Equals K: Prefix Sum & Hash Map (LeetCode 560)

> **One-Line Purpose:** Master the prefix sum hash table technique to count arbitrary-sum subarrays in $O(N)$ linear time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #41  
> **Video ID:** `KDH4mhFVvHw`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=KDH4mhFVvHw)  
> **Duration:** 34:45  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- Understand why Two Pointers / Sliding Window fails when arrays contain negative integers.
- The Prefix Sum algebraic relation:
  $$\text{sum}(i, j) = \text{prefixSum}[j] - \text{prefixSum}[i - 1] = K \implies \text{prefixSum}[i - 1] = \text{prefixSum}[j] - K$$
- Why the hash map must be pre-populated with `mp[0] = 1` (accounting for subarrays starting at index $0$).

---

## 🔵 Complete C++ Implementation

```cpp
#include <vector>
#include <unordered_map>
#include <iostream>
using namespace std;

class SolutionSubarraySum {
public:
    int subarraySum(vector<int>& nums, int k) {
        unordered_map<int, int> prefixFreq;
        prefixFreq[0] = 1; // Base case: prefix sum of 0 appears once before any elements

        int currentSum = 0;
        int count = 0;

        for (int x : nums) {
            currentSum += x;
            int targetPrefix = currentSum - k;

            if (prefixFreq.count(targetPrefix)) {
                count += prefixFreq[targetPrefix];
            }

            prefixFreq[currentSum]++;
        }

        return count;
    }
};
```
- **Time Complexity:** $O(N)$ — Single linear scan with $O(1)$ average hash map lookups.
- **Space Complexity:** $O(N)$ — Hash table storing distinct prefix sums.
"""

t11_files["00_master_index.md"] = r"""# Topic 11: Hashing & Prefix Sums — Master Index

> **Domain:** Constant-Time Lookups, Complement Matching, Multi-Pointer Pruning, and Prefix Sum Frequencies

---

## 📋 Topic Overview

This module covers hashing and prefix sum algorithms: Two Sum complement lookups, cycle detection on array indices, 3-Sum and 4-Sum $O(1)$-space multi-pointer techniques, and prefix sum frequency hashing for continuous subarray queries.

---

## 📑 Lecture Index

| # | Lecture Title | Focus Areas | Notes Link | Status |
|---|---|---|---|---|
| **38** | Two Sum, Duplicate & Repeating/Missing | Hash map complement matching, Floyd's tortoise & hare cycle detection on arrays | [01_two_sum_duplicate_repeating_missing.md](./01_two_sum_duplicate_repeating_missing.md) | **AUDITED** |
| **39** | 3 Sum | Array sorting, two-pointer inward scan, complete duplicate avoidance | [02_three_sum_two_pointer_optimal.md](./02_three_sum_two_pointer_optimal.md) | **AUDITED** |
| **40** | 4 Sum | Two outer loops + two pointers ($O(N^3)$), 64-bit integer overflow protection | [03_four_sum_two_pointer_optimal.md](./03_four_sum_two_pointer_optimal.md) | **AUDITED** |
| **41** | Subarray Sum Equals K | Prefix sum frequencies, negative numbers support, base case `mp[0]=1` | [04_subarray_sum_equals_k_prefix_sum.md](./04_subarray_sum_equals_k_prefix_sum.md) | **AUDITED** |

---

## 🎯 Topic Revision & Interview Preparation
- **Topic Quick Revision:** [topic_revision.md](./topic_revision.md)
- **Topic Interview Question Bank:** [topic_interview_questions.md](./topic_interview_questions.md)
"""

t11_files["topic_revision.md"] = r"""# ⚡ Rapid Revision — Topic 11: Hashing & Prefix Sums

> **Target:** 5-minute pre-interview refresher on hashing patterns and prefix sum equations.

---

## 🔑 Key Problem Patterns
- **Subarray Sum = K:** `target = curr_sum - K`. Store prefix sum frequencies. Always initialize `mp[0] = 1`.
- **3-Sum:** Sort array. Loop $i$, two pointers $j$ and $k$. Skip `nums[i] == nums[i-1]`.
- **4-Sum:** Nested loops $i, j$ + two pointers. Cast to `long long` before adding 4 values.
- **Find Duplicate ($O(1)$ space):** Array is a linked list (`next = nums[curr]`). Use Floyd's cycle detection.
"""

t11_files["topic_interview_questions.md"] = r"""# 💼 Topic Interview Question Bank — Topic 11: Hashing

---

### Q1: Why does Sliding Window fail for "Subarray Sum Equals K" when negative numbers are present?
**Answer:**
The two-pointer sliding window technique relies on monotonicity: expanding the window increases the window sum, and contracting the window decreases the window sum. When negative integers exist, adding an element can decrease the sum, and removing an element can increase it. Monotonicity is violated; thus, Prefix Sum + Hash Map is strictly required.
"""

write_files(t11_dir, t11_files)

# ==========================================
# LECTURE 52: MILESTONE UPDATE IN TOPIC 12
# ==========================================
t12_dir = os.path.join(root, "12_recursion_and_backtracking")
l52_content = r"""# Lecture 52: Series Milestone Update & Course Progression Roadmap

> **One-Line Purpose:** Transitioning from foundational Divide-and-Conquer and Backtracking into Advanced Linear and Non-Linear Data Structures (OOPs, Linked Lists, Stacks, Trees, Graphs, DP).

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #52  
> **Video ID:** `SBQfXK7q5K4`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=SBQfXK7q5K4)  
> **Duration:** 03:50  
> **Status:** AUDITED  

---

## 🎯 Educational Roadmap & Milestones

This lecture marks the halfway milestone in the Apna College C++ DSA series:
1. **Completed Milestones:** C++ Foundations, Binary Operations, Contiguous Memory (Arrays/Vectors), Pointers, Binary Search, Sorting, Strings, 2D Arrays, Hashing, and Core Recursion/Backtracking.
2. **Upcoming Advanced Modules:**
   - Object-Oriented Programming (OOPs) in C++ (Lecture 56)
   - Non-Contiguous Linear Structures: Linked Lists (Lectures 57–67, 78)
   - Abstract Data Types: Stacks & Queues (Lectures 68–84)
   - Hierarchical Structures: Binary Trees & BSTs (Lectures 85–110)
   - Graph Theory & Network Topologies (Lectures 111–136)
   - Dynamic Programming & Knapsack Optimization (Lectures 137–144)
"""
l52_path = os.path.join(t12_dir, "14_course_milestone_and_series_update.md")
with open(l52_path, "w", encoding="utf-8") as f:
    f.write(l52_content)
print(f"Wrote {l52_path}")

# ==========================================
# TOPIC 13: OOPS IN C++ (L56)
# ==========================================
t13_dir = os.path.join(root, "13_oops")
t13_files = {}

t13_files["01_oops_in_cpp_complete_masterclass.md"] = r"""# Lecture 56: Object-Oriented Programming (OOPs) in C++ Complete Masterclass

> **One-Line Purpose:** Master the 4 pillars of Object-Oriented Programming (Encapsulation, Abstraction, Inheritance, Polymorphism), virtual functions, vtables, and deep vs shallow copying for placement interviews.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #56  
> **Video ID:** `mlIUKyZIUUU`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=mlIUKyZIUUU)  
> **Duration:** 02:04:23  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- **Classes vs Objects:** Blueprint vs instantiated memory.
- **Access Modifiers:** `public`, `private`, `protected`.
- **Constructors & Destructors:** Parameterized, Copy Constructor (Deep vs Shallow Copy), Destructor cleanup.
- **Encapsulation & Abstraction:** Data hiding and abstract interface design via pure virtual functions (`= 0`).
- **Inheritance:** Single, Multilevel, Multiple, Hierarchical, Hybrid, and the **Diamond Problem** solved via `virtual` base classes.
- **Polymorphism:**
  - Compile-Time: Function Overloading and Operator Overloading.
  - Run-Time: `virtual` member functions, Dynamic Dispatch, `vptr` pointer and `vtable`.
- **Advanced C++ OOP Keywords:** `static`, `friend`, `override`, `final`.

---

## 🔵 Lecture Content

### 1. The 4 Core Pillars of OOP

```text
┌──────────────────────────────────────────────────────────────┐
│                    THE 4 PILLARS OF OOPS                     │
├─────────────────┬─────────────────┬──────────────────────────┤
│ Encapsulation   │ Abstraction     │ Inheritance & Poly       │
├─────────────────┼─────────────────┼──────────────────────────┤
│ Bundling data   │ Hiding internal │ Code reuse via hierarchy │
│ and functions;  │ implementation; │ and dynamic runtime      │
│ private fields. │ public APIs.    │ method dispatch.         │
└─────────────────┴─────────────────┴──────────────────────────┘
```

---

### 2. Deep Copy vs Shallow Copy

A default copy constructor performs a **shallow copy** (bitwise member-by-member copy). If a class manages dynamic heap memory via a raw pointer, shallow copying duplicates the pointer address, not the allocated memory:
1. Double Free Error: When both objects destruct, they call `delete` on the same address.
2. Unintended Side Effects: Modifying heap memory via one object mutates the other.

#### Implementing a Custom Deep Copy Constructor:
```cpp
#include <iostream>
#include <cstring>
using namespace std;

class Student {
public:
    string name;
    double* cgpa;

    Student(string name, double cgpaVal) {
        this->name = name;
        this->cgpa = new double(cgpaVal);
    }

    // Deep Copy Constructor
    Student(const Student& other) {
        this->name = other.name;
        this->cgpa = new double(*other.cgpa); // Allocate independent heap memory!
    }

    // Destructor to prevent memory leak
    ~Student() {
        delete cgpa;
    }
};
```

---

### 3. Run-Time Polymorphism: Virtual Functions & `vtable`

When a base class pointer points to a derived class object, calling a non-virtual function invokes the **base class method** (Static Binding).
Adding the `virtual` keyword enables **Dynamic Binding**:
- The compiler inserts a hidden pointer (`vptr`) into every object of a class with virtual functions.
- `vptr` points to a class-wide `vtable` (array of function pointers).
- At runtime, the function call is resolved by looking up the derived class's override in the `vtable`.

```cpp
class Shape {
public:
    virtual void draw() {
        cout << "Drawing generic shape" << endl;
    }
    virtual ~Shape() {} // Essential: Virtual destructor ensures derived cleanup
};

class Circle : public Shape {
public:
    void draw() override {
        cout << "Drawing Circle" << endl;
    }
};

void render(Shape* s) {
    s->draw(); // Calls Circle::draw() at runtime if s is a Circle!
}
```

---

### 4. Pure Virtual Functions & Abstract Classes
A class with at least one pure virtual function (`virtual void f() = 0;`) cannot be directly instantiated and acts as an interface.

---

## 🔥 Interview Questions

### Q1: Why must a base class destructor always be declared `virtual`?
**Answer:**
If a derived class object is deleted through a base class pointer (`Base* b = new Derived(); delete b;`), and the base destructor is **not** virtual, the program exhibits undefined behavior. The compiler statically binds the destructor call and executes only `~Base()`, skipping `~Derived()`. Any heap memory or system resources acquired by the derived class will leak.
"""

t13_files["00_master_index.md"] = r"""# Topic 13: Object-Oriented Programming (OOPs) — Master Index

> **Domain:** Encapsulation, Abstraction, Inheritance, Run-Time Polymorphism, `vptr`/`vtable`, Deep Copying

---

## 📋 Topic Overview

This module covers Object-Oriented Programming in C++. Key topics include class memory representation, shallow vs deep copying, inheritance hierarchies, compile-time vs run-time polymorphism, virtual destructors, and pure virtual abstract interfaces.

---

## 📑 Lecture Index

| # | Lecture Title | Focus Areas | Notes Link | Status |
|---|---|---|---|---|
| **56** | OOPs Tutorial in One Shot | 4 Pillars of OOP, Constructors/Destructors, Deep Copy, `virtual` functions, `vtable` | [01_oops_in_cpp_complete_masterclass.md](./01_oops_in_cpp_complete_masterclass.md) | **AUDITED** |

---

## 🎯 Topic Revision & Interview Preparation
- **Topic Quick Revision:** [topic_revision.md](./topic_revision.md)
- **Topic Interview Question Bank:** [topic_interview_questions.md](./topic_interview_questions.md)
"""

t13_files["topic_revision.md"] = r"""# ⚡ Rapid Revision — Topic 13: OOPs in C++

> **Target:** 5-minute pre-interview refresher on C++ OOP concepts and system design questions.

---

## 🔑 Quick Rule Refresher
- **Shallow Copy:** Bitwise copy; triggers double-free when pointers exist.
- **Deep Copy:** Allocate separate heap buffer and copy dereferenced values.
- **`vptr` & `vtable`:** Enables dynamic dispatch for `virtual` functions (costs 8 bytes per object for pointer).
- **Abstract Class:** Class containing at least one pure virtual function (`= 0`).
- **Diamond Problem:** Solved by `class B : virtual public A`.
"""

t13_files["topic_interview_questions.md"] = r"""# 💼 Topic Interview Question Bank — Topic 13: OOPs

---

### Q1: What is the Diamond Problem in C++ and how is it resolved?
**Answer:**
The Diamond Problem occurs in multiple inheritance when a class `D` inherits from both `B` and `C`, and both `B` and `C` inherit from class `A`. As a result, `D` contains two duplicate copies of `A`'s member variables, leading to compiler ambiguity when accessing `A`'s fields.
It is resolved using **Virtual Inheritance**: `class B : virtual public A` and `class C : virtual public A`. The compiler ensures only a single shared instance of `A` is constructed.
"""

write_files(t13_dir, t13_files)
print("Finished writing Batch 2: Topics 10, 11, L52, 13.")
