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
# TOPIC 06: SORTING ALGORITHMS (L24 - L26)
# ==========================================
t06_dir = os.path.join(root, "06_sorting_algorithms")
t06_files = {}

t06_files["01_bubble_selection_insertion_sort.md"] = r"""# Lecture 24: Sorting Algorithms: Bubble, Selection & Insertion Sort

> **One-Line Purpose:** Master foundational $O(N^2)$ quadratic sorting algorithms, their internal loop invariants, stability, adaptive optimizations, and in-place memory characteristics.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #24  
> **Video ID:** `1jCFUv-Xlqo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=1jCFUv-Xlqo)  
> **Duration:** 34:33  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The distinction between **Comparison-based** and **Non-comparison-based** sorts.
- **Bubble Sort:** Repeatedly swap adjacent inverted elements to "bubble" the maximum to the right; optimize to $O(N)$ with a swapped flag.
- **Selection Sort:** Find the global minimum in the unsorted suffix and swap it with the front; understand why it is fundamentally unstable.
- **Insertion Sort:** Progressively insert elements into an already sorted prefix; understand why it is adaptive and ideal for nearly-sorted data.
- The precise definitions of **In-Place** ($O(1)$ space) and **Stability** (preservation of relative order of equal keys).

---

## 🔵 Lecture Content

### 1. Bubble Sort: Mechanics & Optimization

At each pass $i$ ($0 \le i < n - 1$), adjacent elements `arr[j]` and `arr[j+1]` are compared. If `arr[j] > arr[j+1]`, they are swapped.
After pass $i$, the largest remaining element is placed in its permanent position `n - 1 - i`.

```text
Pass 0: [4, 1, 5, 2, 3] -> [1, 4, 2, 3, 5]  (5 settled at index 4)
Pass 1: [1, 4, 2, 3, 5] -> [1, 2, 3, 4, 5]  (4 settled at index 3)
```

#### Optimized C++ Implementation
```cpp
#include <vector>
#include <iostream>
using namespace std;

void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        bool isSwapped = false;
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
                isSwapped = true;
            }
        }
        // Adaptive check: If no elements were swapped, array is already sorted
        if (!isSwapped) break;
    }
}
```
- **Time Complexity:** Best $O(N)$ (already sorted), Average/Worst $O(N^2)$.
- **Space Complexity:** $O(1)$ auxiliary.
- **Stability:** Stable (strictly `>` prevents swapping identical elements).

---

### 2. Selection Sort: Minimum Selection

Divide the array into sorted prefix and unsorted suffix.
In pass $i$, find the index of the minimum element in `arr[i...n-1]`, then swap it with `arr[i]`.

```cpp
void selectionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIdx]) {
                minIdx = j;
            }
        }
        if (minIdx != i) {
            swap(arr[i], arr[minIdx]);
        }
    }
}
```
- **Time Complexity:** Best, Average, Worst: Strictly $O(N^2)$ (always performs $N(N-1)/2$ comparisons).
- **Space Complexity:** $O(1)$.
- **Stability:** Unstable (e.g. `[4a, 4b, 1]` -> `1` swaps with `4a`, placing `4a` after `4b`).
- **Advantage:** Minimizes the total number of memory write operations (strictly at most $N - 1$ swaps).

---

### 3. Insertion Sort: Card Player's Algorithm

Maintain sorted subarray `arr[0...i-1]`. Pick `current = arr[i]` and shift all elements in the sorted prefix that are greater than `current` one position right. Insert `current` into the created vacancy.

```cpp
void insertionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 1; i < n; i++) {
        int current = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > current) {
            arr[j + 1] = arr[j]; // Shift right
            j--;
        }
        arr[j + 1] = current;    // Insert in correct spot
    }
}
```
- **Time Complexity:** Best $O(N)$ (already sorted), Worst $O(N^2)$ (reverse sorted).
- **Space Complexity:** $O(1)$.
- **Stability:** Stable.
- **Advantage:** Highly efficient for small arrays ($N \le 30$) and nearly-sorted arrays. (Used in hybrid algorithms like Timsort and `std::sort` introsort).

---

## 4. Comprehensive Comparison Table

| Algorithm | Best Time | Avg Time | Worst Time | Auxiliary Space | Stable? | Swaps (Worst) |
|---|---|---|---|---|---|---|
| **Bubble Sort** | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes | $O(N^2)$ |
| **Selection Sort** | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | No | $O(N)$ |
| **Insertion Sort** | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes | $O(N^2)$ (shifts) |

---

## 🔥 Interview Questions

### Q1: Why is Selection Sort preferred when memory writes are extremely expensive?
**Answer:** While Bubble and Insertion Sort may execute up to $O(N^2)$ write operations, Selection Sort makes at most $N - 1$ writes (swaps) across its entire execution. In systems with flash memory or EEPROM where writes wear down the hardware, Selection Sort's minimal write count is advantageous.
"""

t06_files["02_dnf_sort_colors.md"] = r"""# Lecture 25: Sort an Array of 0s, 1s & 2s (DNF Algorithm — LeetCode 75)

> **One-Line Purpose:** Master Edsger Dijkstra's Dutch National Flag (DNF) 3-way partitioning algorithm to sort tri-value arrays in a single $O(N)$ pass with $O(1)$ space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #25  
> **Video ID:** `J48aGjfjYTI`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=J48aGjfjYTI)  
> **Duration:** 33:39  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The limitations of counting sort ($2$ passes) vs DNF ($1$ pass).
- The 4 logical invariant regions maintained by 3 pointers: `low`, `mid`, `high`.
- Why `mid` advances when swapping with `low` (`nums[mid] == 0`), but does **NOT** advance when swapping with `high` (`nums[mid] == 2`).
- How DNF generalizes to Quicksort 3-way partitioning (dealing with duplicate keys).

---

## 🔵 Lecture Content

### 1. Invariant Regions of DNF

The array is divided into 4 contiguous zones at any point during iteration:
```text
[ 0 0 ... 0 | 1 1 ... 1 | ? ? ... ? | 2 2 ... 2 ]
  0       low-1   low   mid-1   mid   high  high+1     n-1
```
1. `arr[0 ... low - 1]` contains exclusively `0`s.
2. `arr[low ... mid - 1]` contains exclusively `1`s.
3. `arr[mid ... high]` contains **unknown / unsorted** elements (`?`).
4. `arr[high + 1 ... n - 1]` contains exclusively `2`s.

The algorithm terminates when `mid > high`, meaning the unknown region has shrunk to zero size.

---

## 2. Pointer Movement Rules

Inspect `arr[mid]`:
- **Case 0 (`arr[mid] == 0`):**
  Swap `arr[low]` and `arr[mid]`.
  Advance both: `low++`, `mid++`.
  *(Since the element swapped from `arr[low]` is guaranteed to be a `1`, `mid` can safely advance).*
- **Case 1 (`arr[mid] == 1`):**
  Element is in its correct region. Just advance `mid++`.
- **Case 2 (`arr[mid] == 2`):**
  Swap `arr[mid]` and `arr[high]`.
  Decrement `high--`.
  *(CRITICAL: Do NOT increment `mid`! The element incoming from `arr[high]` was unknown and must be re-evaluated in the next step).*

---

## 3. Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    void sortColors(vector<int>& nums) {
        int low = 0;
        int mid = 0;
        int high = nums.size() - 1;

        while (mid <= high) {
            if (nums[mid] == 0) {
                swap(nums[low], nums[mid]);
                low++;
                mid++;
            } else if (nums[mid] == 1) {
                mid++;
            } else { // nums[mid] == 2
                swap(nums[mid], nums[high]);
                high--;
                // Note: mid is NOT incremented here
            }
        }
    }
};

int main() {
    Solution sol;
    vector<int> colors = {2, 0, 2, 1, 1, 0};
    sol.sortColors(colors);
    cout << "Sorted: ";
    for (int x : colors) cout << x << " "; // Output: 0 0 1 1 2 2
    cout << endl;
    return 0;
}
```

---

## 4. Complexity Analysis

- **Time Complexity:** $O(N)$ — Exactly $1$ pass through the array. Each operation advances `mid` or decrements `high`.
- **Space Complexity:** $O(1)$ — Modified strictly in-place.

---

## 🔥 Interview Questions

### Q1: Why not just use Counting Sort (Count 0s, 1s, 2s)?
**Answer:** Counting Sort requires two passes (Pass 1: count frequencies, Pass 2: overwrite array) and is not an in-place element-swapping algorithm. If elements are rich objects (e.g., structs containing color and payload), overwriting loses object identity. DNF sorts strictly via element swaps in a single pass.
"""

t06_files["03_merge_sorted_arrays_and_next_permutation.md"] = r"""# Lecture 26: Merge Sorted Arrays (LeetCode 88) & Next Permutation (LeetCode 31)

> **One-Line Purpose:** Master reverse three-pointer in-place buffer filling and mathematical lexicographic ordering through pivot discovery and suffix inversion.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #26  
> **Video ID:** `-1cLK6PaLsQ`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=-1cLK6PaLsQ)  
> **Duration:** 43:49  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- **Merge Sorted Array:** Why filling from the front causes $O(N)$ element shifts, and how filling from the back (`m + n - 1`) achieves $O(1)$ space without extra memory.
- **Next Permutation:** The mathematical definition of lexicographical order.
- The 3-step canonical algorithm for Next Permutation:
  1. Locate the first decreasing element from the right (Pivot).
  2. Find the smallest element to the right of Pivot that is strictly greater than Pivot.
  3. Swap them and reverse the suffix to obtain the smallest lexicographical sequence.

---

## 🔵 Lecture Content

### 1. Merge Sorted Array (In-Place Backwards Fill)

Given `nums1` of size $m + n$ (with $m$ valid elements and $n$ trailing zeros) and `nums2` of size $n$, merge `nums2` into `nums1` in sorted order.

```cpp
#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;

class SolutionMerge {
public:
    void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        int p1 = m - 1;       // Pointer at end of nums1 valid elements
        int p2 = n - 1;       // Pointer at end of nums2
        int writeIdx = m + n - 1; // Write pointer at very end of buffer

        while (p1 >= 0 && p2 >= 0) {
            if (nums1[p1] > nums2[p2]) {
                nums1[writeIdx--] = nums1[p1--];
            } else {
                nums1[writeIdx--] = nums2[p2--];
            }
        }

        // If nums2 has remaining elements, flush them into nums1
        while (p2 >= 0) {
            nums1[writeIdx--] = nums2[p2--];
        }
        // (If p1 has remaining elements, they are already in their correct places)
    }
};
```
- **Time Complexity:** $O(m + n)$.
- **Space Complexity:** $O(1)$ auxiliary.

---

### 2. Next Permutation (Lexicographic Invariant)

```text
Example: [1, 2, 5, 4, 3]
Step 1: Scan from right to find pivot where nums[i] < nums[i+1].
        nums[1] (2) < nums[2] (5). Pivot = index 1 (value 2).
Step 2: Scan from right to find element strictly greater than nums[pivot].
        nums[4] is 3. Since 3 > 2, swap index 1 and index 4.
        Array becomes: [1, 3, 5, 4, 2]
Step 3: Reverse the suffix from pivot + 1 to end (index 2 to 4).
        Reverse [5, 4, 2] -> [2, 4, 5].
        Final Result: [1, 3, 2, 4, 5].
```

```cpp
class SolutionNextPermutation {
public:
    void nextPermutation(vector<int>& nums) {
        int n = nums.size();
        int pivot = -1;

        // Step 1: Find rightmost index i such that nums[i] < nums[i + 1]
        for (int i = n - 2; i >= 0; i--) {
            if (nums[i] < nums[i + 1]) {
                pivot = i;
                break;
            }
        }

        // If no pivot exists, array is in descending order (highest permutation)
        if (pivot == -1) {
            reverse(nums.begin(), nums.end());
            return;
        }

        // Step 2: Find rightmost element strictly greater than nums[pivot]
        for (int i = n - 1; i > pivot; i--) {
            if (nums[i] > nums[pivot]) {
                swap(nums[pivot], nums[i]);
                break;
            }
        }

        // Step 3: Reverse the descending suffix to make it ascending (minimal)
        reverse(nums.begin() + pivot + 1, nums.end());
    }
};
```

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$ — Scanning for pivot ($O(N)$), scanning for successor ($O(N)$), and reversing suffix ($O(N)$).
- **Space Complexity:** $O(1)$ auxiliary.
"""

t06_files["00_master_index.md"] = r"""# Topic 06: Sorting Algorithms — Master Index

> **Domain:** Quadratic Sorts, Loop Invariants, Multi-Pointer Partitioning, and Lexicographic Permutations

---

## 📋 Topic Overview

This module establishes core sorting foundations. It analyzes elementary sorting mechanics (Bubble, Selection, Insertion) focusing on algorithmic invariants, in-place behavior, and stability. It advances to Dutch National Flag 3-way partitioning and two-pointer buffer filling and lexicographical permutations.

---

## 📑 Lecture Index

| # | Lecture Title | Focus Areas | Notes Link | Status |
|---|---|---|---|---|
| **24** | Sorting Algorithms (Bubble, Selection, Insertion) | Loop invariants, best/worst complexity, stability, adaptive optimizations | [01_bubble_selection_insertion_sort.md](./01_bubble_selection_insertion_sort.md) | **AUDITED** |
| **25** | Sort Colors (DNF 3-Way Partitioning) | Dutch National Flag, 4-region invariants, single-pass element swaps | [02_dnf_sort_colors.md](./02_dnf_sort_colors.md) | **AUDITED** |
| **26** | Merge Sorted Arrays & Next Permutation | In-place backward buffer filling, pivot finding, lexicographic order | [03_merge_sorted_arrays_and_next_permutation.md](./03_merge_sorted_arrays_and_next_permutation.md) | **AUDITED** |

---

## 🎯 Topic Revision & Interview Preparation
- **Topic Quick Revision:** [topic_revision.md](./topic_revision.md)
- **Topic Interview Question Bank:** [topic_interview_questions.md](./topic_interview_questions.md)
"""

t06_files["topic_revision.md"] = r"""# ⚡ Rapid Revision — Topic 06: Sorting Algorithms

> **Target:** 5-minute pre-interview refresher on sorting algorithms, complexities, stability, and invariant rules.

---

## 🔑 Quick Comparison Chart

| Algorithm | Best Time | Worst Time | Space | Stable | Key Trick |
|---|---|---|---|---|---|
| **Bubble Sort** | $O(N)$ | $O(N^2)$ | $O(1)$ | Yes | Break if `!isSwapped` |
| **Selection Sort** | $O(N^2)$ | $O(N^2)$ | $O(1)$ | No | Min writes ($N-1$ swaps) |
| **Insertion Sort** | $O(N)$ | $O(N^2)$ | $O(1)$ | Yes | Shift sorted prefix right |
| **DNF Algorithm** | $O(N)$ | $O(N)$ | $O(1)$ | No | `low`, `mid`, `high`; don't advance `mid` on `swap(mid, high)` |
| **Next Permutation**| $O(N)$ | $O(N)$ | $O(1)$ | N/A | Find pivot from right, swap with successor, reverse suffix |
| **Merge Sorted Array**| $O(m+n)$ | $O(m+n)$ | $O(1)$ | Yes | Fill backwards from `m + n - 1` |
"""

t06_files["topic_interview_questions.md"] = r"""# 💼 Topic Interview Question Bank — Topic 06: Sorting Algorithms

---

### Q1: When is Insertion Sort faster than QuickSort or MergeSort?
**Answer:**
For small arrays ($N \le 16 - 32$) or arrays that are already "nearly sorted", Insertion Sort runs in linear $O(N)$ time with minimal constant factors, zero recursion overhead, and excellent CPU cache locality. This is why standard library implementations (`std::sort`) switch to Insertion Sort for small partitions.

---

### Q2: Why does DNF not increment `mid` when `nums[mid] == 2`?
**Answer:**
When `nums[mid] == 2`, it is swapped with `nums[high]`. The element previously at `high` was in the "unknown" partition `[mid...high]`. Because its value has not yet been inspected, we cannot increment `mid`; it must be evaluated on the subsequent iteration.
"""

write_files(t06_dir, t06_files)

# ==========================================
# TOPIC 07: C++ STL (L27 - L28)
# ==========================================
t07_dir = os.path.join(root, "07_cpp_stl")
t07_files = {}

t07_files["01_cpp_stl_complete_containers_and_algorithms.md"] = r"""# Lecture 27: C++ Standard Template Library (STL) Complete Masterclass

> **One-Line Purpose:** Master all standard C++ STL containers, iterators, comparator lambdas, and standard algorithms with exact time complexities and internal data structure mechanics.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #27  
> **Video ID:** `okhdtEk1iKk`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=okhdtEk1iKk)  
> **Duration:** 01:27:20  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The 4 pillars of the STL: **Containers, Iterators, Algorithms, and Functors**.
- **Sequence Containers:** `vector`, `list` (doubly linked list), `deque` (double-ended queue).
- **Container Adaptors:** `stack`, `queue`, `priority_queue` (max-heap / min-heap).
- **Associative Containers:** `set`, `map`, `multiset`, `multimap` (Self-balancing Red-Black Trees, $O(\log N)$).
- **Unordered Associative Containers:** `unordered_set`, `unordered_map` (Hash Tables, $O(1)$ amortized).
- **Standard Algorithms:** `sort`, `reverse`, `binary_search`, `lower_bound`, `upper_bound`, `accumulate`, custom lambda comparators.

---

## 🔵 Lecture Content

### 1. Sequential Containers Deep-Dive

#### `std::vector` (Dynamic Contiguous Array)
- Contiguous memory, amortized $O(1)$ push_back, $O(1)$ random access.
- `capacity()` vs `size()`, `reserve()` vs `resize()`.

#### `std::list` (Doubly Linked List)
- Non-contiguous memory, $O(1)$ insertion and deletion at any point given an iterator.
- No random access ($O(N)$ traversal).

#### `std::deque` (Double-Ended Queue)
- Chunked memory blocks connected via a central map.
- $O(1)$ `push_front`, `push_back`, `pop_front`, `pop_back`.

---

### 2. Container Adaptors

```cpp
#include <stack>
#include <queue>
#include <iostream>
using namespace std;

void containerAdaptorsDemo() {
    // 1. Stack: LIFO
    stack<int> s;
    s.push(10); s.push(20);
    s.pop(); // removes 20

    // 2. Queue: FIFO
    queue<int> q;
    q.push(10); q.push(20);
    q.pop(); // removes 10

    // 3. Priority Queue: Max-Heap by default (O(log N) push/pop, O(1) top)
    priority_queue<int> maxHeap;
    maxHeap.push(5); maxHeap.push(20); maxHeap.push(10);
    // maxHeap.top() == 20

    // Min-Heap instantiation:
    priority_queue<int, vector<int>, greater<int>> minHeap;
    minHeap.push(5); minHeap.push(20); minHeap.push(10);
    // minHeap.top() == 5
}
```

---

### 3. Associative vs Unordered Containers

| Container | Internal Structure | Search / Insert / Delete | Ordering | Key Requirement |
|---|---|---|---|---|
| `std::set` / `std::map` | Red-Black Tree (BST) | $O(\log N)$ strictly | Strictly sorted | `operator<` defined |
| `std::unordered_set` / `std::unordered_map` | Hash Table (Buckets) | $O(1)$ average, $O(N)$ worst | Arbitrary (hash based) | `std::hash` & `operator==` |

---

### 4. STL Algorithms & Custom Comparators

```cpp
#include <vector>
#include <algorithm>
#include <numeric>
#include <iostream>
using namespace std;

struct Item {
    int id;
    int score;
};

void algorithmsDemo() {
    vector<int> nums = {4, 1, 8, 3, 8, 2};

    // Sorting
    sort(nums.begin(), nums.end()); // Ascending: [1, 2, 3, 4, 8, 8]
    sort(nums.begin(), nums.end(), greater<int>()); // Descending

    // Binary Search & Bounds (array must be sorted)
    sort(nums.begin(), nums.end());
    bool exists = binary_search(nums.begin(), nums.end(), 3); // true
    auto lb = lower_bound(nums.begin(), nums.end(), 8); // iterator to first 8
    auto ub = upper_bound(nums.begin(), nums.end(), 8); // iterator to element strictly > 8

    // Custom Comparator Lambda
    vector<Item> items = {{1, 95}, {2, 80}, {3, 95}};
    sort(items.begin(), items.end(), [](const Item& a, const Item& b) {
        if (a.score != b.score) return a.score > b.score; // Higher score first
        return a.id < b.id; // Lower ID first on tie
    });
}
```

---

## 5. Summary Matrix of Operations

| Operation | `vector` | `list` | `deque` | `set` | `unordered_set` | `priority_queue` |
|---|---|---|---|---|---|---|
| Random Access (`[]`) | $O(1)$ | N/A | $O(1)$ | N/A | N/A | N/A |
| Insert Front | $O(N)$ | $O(1)$ | $O(1)$ | N/A | N/A | N/A |
| Insert Back | $O(1)$ amortized | $O(1)$ | $O(1)$ | N/A | N/A | $O(\log N)$ |
| Find / Search | $O(N)$ | $O(N)$ | $O(N)$ | $O(\log N)$ | $O(1)$ avg | $O(1)$ (top only) |
"""

t07_files["02_cpp_compiler_setup_and_toolchain.md"] = r"""# Lecture 28: C++ Compiler Setup & Development Toolchain

> **One-Line Purpose:** Establish a modern, production-grade C++ compilation environment using GCC/Clang, VS Code tasks, and compiler optimization flags.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #28  
> **Video ID:** `varXreLWPRo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=varXreLWPRo)  
> **Duration:** 01:40  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- Setup C++ compilers on macOS / Linux (`clang++` / `g++`) and Windows (MinGW-w64 / MSVC).
- Understand modern C++ compiler flags: `-std=c++17`, `-Wall`, `-Wextra`, `-O2`.
- Fast terminal compilation commands for competitive programming.

---

## 🔵 Content

### Essential Terminal Flags
```bash
g++ -std=c++17 -Wall -Wextra -O2 main.cpp -o main
./main
```
- `-std=c++17` enables structured binding, inline variables, and `std::string_view`.
- `-Wall -Wextra` surfaces all latent compiler warnings (uninitialized variables, signed/unsigned comparisons).
- `-O2` turns on production compiler optimizations.
"""

t07_files["00_master_index.md"] = r"""# Topic 07: C++ Standard Template Library (STL) — Master Index

> **Domain:** Data Structures in STL, Iterators, Computational Complexity Guarantees, and Toolchains

---

## 📋 Topic Overview

This module covers the C++ Standard Template Library (STL), demystifying internal data structure mechanics (contiguous memory, doubly-linked lists, binary heaps, red-black trees, hash tables) and standard algorithmic routines.

---

## 📑 Lecture Index

| # | Lecture Title | Focus Areas | Notes Link | Status |
|---|---|---|---|---|
| **27** | C++ STL Complete Masterclass | Containers (`vector`, `deque`, `list`, `set`, `map`), Iterators, Algorithms, Comparators | [01_cpp_stl_complete_containers_and_algorithms.md](./01_cpp_stl_complete_containers_and_algorithms.md) | **AUDITED** |
| **28** | C++ Compiler Setup & Toolchain | `clang++`/`g++` installation, compilation flags, `-O2`, `-std=c++17` | [02_cpp_compiler_setup_and_toolchain.md](./02_cpp_compiler_setup_and_toolchain.md) | **AUDITED** |

---

## 🎯 Topic Revision & Interview Preparation
- **Topic Quick Revision:** [topic_revision.md](./topic_revision.md)
- **Topic Interview Question Bank:** [topic_interview_questions.md](./topic_interview_questions.md)
"""

t07_files["topic_revision.md"] = r"""# ⚡ Rapid Revision — Topic 07: C++ STL

> **Target:** 5-minute pre-interview refresher on STL complexity guarantees and container selection.

---

## 🔑 Container Selection Cheatsheet
- Need random access + fast push_back: `std::vector`.
- Need fast push/pop at both ends: `std::deque`.
- Need fast sorted lookup / uniqueness: `std::set` ($O(\log N)$).
- Need fastest key-value lookup: `std::unordered_map` ($O(1)$ avg).
- Need maximum or minimum priority access: `std::priority_queue` ($O(\log N)$ push/pop).
"""

t07_files["topic_interview_questions.md"] = r"""# 💼 Topic Interview Question Bank — Topic 07: C++ STL

---

### Q1: What is the difference between `map` and `unordered_map`?
**Answer:**
- `std::map` is implemented via a Self-Balancing Binary Search Tree (Red-Black Tree). Keys are stored in sorted order. Search, insertion, and deletion are guaranteed $O(\log N)$ worst-case.
- `std::unordered_map` is implemented via a Hash Table with buckets. Keys are unordered. Search, insertion, and deletion are $O(1)$ amortized average, but can degrade to $O(N)$ in the event of hash collisions.
"""

write_files(t07_dir, t07_files)

# ==========================================
# TOPIC 08: STRINGS (L29 - L33)
# ==========================================
t08_dir = os.path.join(root, "08_strings")
t08_files = {}

t08_files["01_strings_and_character_arrays.md"] = r"""# Lecture 29: Strings & Character Arrays in C++ — Part 1

> **One-Line Purpose:** Master the fundamental distinction between C-style null-terminated character arrays and dynamic `std::string` objects, memory layouts, and input streams.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #29  
> **Video ID:** `MOSjYaVymcU`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=MOSjYaVymcU)  
> **Duration:** 30:03  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The structure of C-style character arrays and the mandatory null-terminating character `'\0'`.
- Why `cin >>` stops reading at whitespace and how `cin.getline()` or `getline(cin, str)` captures full lines.
- The dynamic heap-allocated nature of C++ `std::string` and Small String Optimization (SSO).
- Crucial member functions: `length()`, `substr()`, `push_back()`, `pop_back()`.

---

## 🔵 Lecture Content

### 1. Character Arrays vs `std::string`

```cpp
#include <iostream>
#include <cstring>
#include <string>
using namespace std;

void stringBasics() {
    // 1. C-style char array
    char charArr[] = "hello"; // size is 6 bytes: 'h','e','l','l','o','\0'
    cout << "Length: " << strlen(charArr) << endl; // 5

    // 2. C++ std::string
    string s = "hello";
    s += " world"; // Dynamic reallocation handled automatically
    cout << "Size: " << s.size() << ", Capacity: " << s.capacity() << endl;

    // Reading with spaces
    string fullLine;
    // getline(cin, fullLine); // Reads until '\n'
}
```

---

## 2. Common Interview Traps with `getline`
When switching from `cin >> x` to `getline(cin, s)`, the trailing newline `'\n'` remains in the input stream buffer. Always consume it using `cin.ignore()` before `getline()`.
"""

t08_files["02_valid_palindrome_and_remove_occurrences.md"] = r"""# Lecture 30: Valid Palindrome (LeetCode 125) & Remove All Occurrences (LeetCode 1910)

> **One-Line Purpose:** Master two-pointer inward scans with alphanumeric filtering and iterative substring eradication.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #30  
> **Video ID:** `dSRFgEs3a6A`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=dSRFgEs3a6A)  
> **Duration:** 24:02  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- Solve **Valid Palindrome** in $O(N)$ time and $O(1)$ space using two pointers.
- Use standard C++ utility functions `isalnum()` and `tolower()`.
- Solve **Remove All Occurrences of a Substring** using `std::string::find` and `erase`.

---

## 🔵 Lecture Content

### 1. Valid Palindrome (LeetCode 125)

```cpp
#include <string>
#include <cctype>
#include <iostream>
using namespace std;

class SolutionPalindrome {
public:
    bool isPalindrome(string s) {
        int left = 0, right = s.size() - 1;

        while (left < right) {
            while (left < right && !isalnum(s[left])) left++;
            while (left < right && !isalnum(s[right])) right--;

            if (tolower(s[left]) != tolower(s[right])) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
};
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$ in-place without copying into a secondary string.

---

### 2. Remove All Occurrences of Substring (LeetCode 1910)

```cpp
class SolutionRemoveOccurrences {
public:
    string removeOccurrences(string s, string part) {
        while (s.length() > 0 && s.find(part) != string::npos) {
            s.erase(s.find(part), part.length());
        }
        return s;
    }
};
```
- **Time Complexity:** $O(N^2 / M)$ where $N = \text{length}(s)$ and $M = \text{length}(part)$.
- Can also be solved in $O(N)$ time using a stack or string builder.
"""

t08_files["03_permutation_in_string_sliding_window.md"] = r"""# Lecture 31: Permutation in String: Fixed-Length Sliding Window (LeetCode 567)

> **One-Line Purpose:** Master frequency-matching over a fixed-size sliding window to detect anagrams in linear $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #31  
> **Video ID:** `VXewy91P0S4`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=VXewy91P0S4)  
> **Duration:** 21:41  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- Understand why a permutation of $s_1$ inside $s_2$ implies a contiguous substring of length $|s_1|$ with identical character frequency distribution.
- Implement the **Fixed Sliding Window** technique with 26-element integer arrays.
- Achieve $O(|s_2|)$ time complexity with $O(1)$ constant space (26 characters).

---

## 🔵 Lecture Content & Implementation

```cpp
#include <string>
#include <vector>
#include <iostream>
using namespace std;

class SolutionPermutation {
public:
    bool checkInclusion(string s1, string s2) {
        int n1 = s1.length();
        int n2 = s2.length();
        if (n1 > n2) return false;

        vector<int> freq1(26, 0);
        vector<int> freq2(26, 0);

        // Populate initial window of size n1
        for (int i = 0; i < n1; i++) {
            freq1[s1[i] - 'a']++;
            freq2[s2[i] - 'a']++;
        }

        if (freq1 == freq2) return true;

        // Slide the window across s2
        for (int i = n1; i < n2; i++) {
            freq2[s2[i] - 'a']++;          // Add newly included character
            freq2[s2[i - n1] - 'a']--;     // Remove character falling out of window

            if (freq1 == freq2) return true;
        }

        return false;
    }
};
```
- **Time Complexity:** $O(26 \times |s_2|) = O(|s_2|)$ time.
- **Space Complexity:** $O(1)$ space (fixed 26-size frequency arrays).
"""

t08_files["04_reverse_words_in_a_string.md"] = r"""# Lecture 32: Reverse Words in a String (LeetCode 151)

> **One-Line Purpose:** Master two-pointer word reversal and in-place whitespace compaction to reverse sentence semantics in $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #32  
> **Video ID:** `RitppzIdMCo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=RitppzIdMCo)  
> **Duration:** 14:42  
> **Status:** AUDITED  

---

## 🔵 Lecture Content & Implementation

```cpp
#include <string>
#include <algorithm>
#include <iostream>
using namespace std;

class SolutionReverseWords {
public:
    string reverseWords(string s) {
        // Step 1: Reverse entire string
        reverse(s.begin(), s.end());

        int n = s.size();
        int writeIdx = 0;

        // Step 2: Traverse words and reverse each word individually
        for (int start = 0; start < n; start++) {
            if (s[start] == ' ') continue;

            if (writeIdx != 0) s[writeIdx++] = ' '; // add single separating space

            int end = start;
            while (end < n && s[end] != ' ') end++;

            int wordStart = writeIdx;
            while (start < end) {
                s[writeIdx++] = s[start++];
            }

            reverse(s.begin() + wordStart, s.begin() + writeIdx);
        }

        s.resize(writeIdx); // Trim trailing whitespace
        return s;
    }
};
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$ auxiliary (in-place modification).
"""

t08_files["05_string_compression.md"] = r"""# Lecture 33: String Compression (LeetCode 443)

> **One-Line Purpose:** Implement in-place Run-Length Encoding (RLE) using two pointers to compress repeating character sequences into character-count pairs.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #33  
> **Video ID:** `cAB15h6-sWA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=cAB15h6-sWA)  
> **Duration:** 19:29  
> **Status:** AUDITED  

---

## 🔵 Lecture Content & Implementation

```cpp
#include <vector>
#include <string>
#include <iostream>
using namespace std;

class SolutionStringCompression {
public:
    int compress(vector<char>& chars) {
        int n = chars.size();
        int writeIdx = 0;
        int i = 0;

        while (i < n) {
            char currChar = chars[i];
            int count = 0;

            // Count contiguous occurrences of currChar
            while (i < n && chars[i] == currChar) {
                count++;
                i++;
            }

            // Write character
            chars[writeIdx++] = currChar;

            // If count > 1, write count digits
            if (count > 1) {
                string countStr = to_string(count);
                for (char c : countStr) {
                    chars[writeIdx++] = c;
                }
            }
        }

        return writeIdx; // New length of compressed array
    }
};
```
- **Time Complexity:** $O(N)$ — Every character is read at most twice and written at most twice.
- **Space Complexity:** $O(1)$ auxiliary memory.
"""

t08_files["00_master_index.md"] = r"""# Topic 08: Strings & Character Arrays — Master Index

> **Domain:** Memory Representation, Two Pointers, Fixed Sliding Windows, and In-Place Compaction

---

## 📋 Topic Overview

This module covers string manipulation in C++. Beginning with null-terminated character buffers vs `std::string`, it advances through two-pointer palindromes, fixed sliding-window permutation matching, word reversal, and in-place run-length string compression.

---

## 📑 Lecture Index

| # | Lecture Title | Focus Areas | Notes Link | Status |
|---|---|---|---|---|
| **29** | Strings & Character Arrays in C++ | Null terminator `'\0'`, `cin.getline()`, `std::string` dynamic storage | [01_strings_and_character_arrays.md](./01_strings_and_character_arrays.md) | **AUDITED** |
| **30** | Valid Palindrome & Remove Occurrences | Inward two-pointer checks, `isalnum()`, `find()` and `erase()` | [02_valid_palindrome_and_remove_occurrences.md](./02_valid_palindrome_and_remove_occurrences.md) | **AUDITED** |
| **31** | Permutation in String | Fixed-size sliding window, 26-char frequency mapping, $O(N)$ matching | [03_permutation_in_string_sliding_window.md](./03_permutation_in_string_sliding_window.md) | **AUDITED** |
| **32** | Reverse Words in String | In-place double reversal, whitespace compaction, $O(1)$ auxiliary space | [04_reverse_words_in_a_string.md](./04_reverse_words_in_a_string.md) | **AUDITED** |
| **33** | String Compression | Run-length encoding (RLE), read/write pointers, digit stringification | [05_string_compression.md](./05_string_compression.md) | **AUDITED** |

---

## 🎯 Topic Revision & Interview Preparation
- **Topic Quick Revision:** [topic_revision.md](./topic_revision.md)
- **Topic Interview Question Bank:** [topic_interview_questions.md](./topic_interview_questions.md)
"""

t08_files["topic_revision.md"] = r"""# ⚡ Rapid Revision — Topic 08: Strings

> **Target:** 5-minute pre-interview refresher on string manipulation algorithms.

---

## 🔑 Key Patterns
- **Palindrome:** Two pointers (`left`, `right`) skipping non-alphanumeric characters.
- **Anagram / Permutation in String:** Fixed-size sliding window with frequency array comparison.
- **Reverse Words:** Reverse full string, then reverse each word in-place, then resize.
- **Run-Length Compression:** Two pointers (`read`, `write`), write count digits only if `count > 1`.
"""

t08_files["topic_interview_questions.md"] = r"""# 💼 Topic Interview Question Bank — Topic 08: Strings

---

### Q1: What is Small String Optimization (SSO) in C++?
**Answer:**
Modern C++ `std::string` implementations avoid heap allocation for small strings (typically $\le 15$ or $22$ bytes) by storing the character array directly inside the string object's internal buffer on the stack. Only when the string exceeds this threshold is memory dynamically allocated on the heap.
"""

write_files(t08_dir, t08_files)

# ==========================================
# TOPIC 09: MATHS FOR DSA (L34)
# ==========================================
t09_dir = os.path.join(root, "09_maths_for_dsa")
t09_files = {}

t09_files["01_maths_for_dsa_sieve_gcd_modular_arithmetic.md"] = r"""# Lecture 34: Maths for DSA: Euclid's GCD, Sieve of Eratosthenes & Modular Arithmetic

> **One-Line Purpose:** Master foundational discrete mathematics for competitive programming and technical interviews: prime sieving, Euclidean logarithmic GCD, and modular arithmetic rules.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #34  
> **Video ID:** `Y4KdgqV1IqA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=Y4KdgqV1IqA)  
> **Duration:** 55:48  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- Why trial division takes $O(\sqrt{N})$ time and how prime factors appear in symmetrical pairs.
- The **Sieve of Eratosthenes** and its harmonic series complexity derivation: $O(N \log \log N)$.
- **Euclid's Algorithm** for Greatest Common Divisor (GCD) and why $\gcd(a, b) = \gcd(b, a \pmod b)$ runs in $O(\log(\min(a, b)))$.
- Mathematical laws of **Modular Arithmetic** under addition, subtraction, and multiplication.
- **Modular Exponentiation (Binary Exponentiation)** running in $O(\log B)$ time.

---

## 🔵 Lecture Content

### 1. Prime Numbers & The Sieve of Eratosthenes

A number $N > 1$ is prime if its only positive divisors are $1$ and $N$.
- **Sieve Algorithm:**
  1. Create boolean array `isPrime[0...N]` initialized to `true`.
  2. Mark `0` and `1` as `false`.
  3. For each $i$ from $2$ up to $\sqrt{N}$:
     - If `isPrime[i]` is `true`, mark all multiples $i \times i, i \times i + i, \dots$ as `false`.

```cpp
#include <vector>
#include <iostream>
using namespace std;

vector<bool> sieveOfEratosthenes(int n) {
    vector<bool> isPrime(n + 1, true);
    isPrime[0] = isPrime[1] = false;

    for (int i = 2; i * i <= n; i++) {
        if (isPrime[i]) {
            // Optimization: start crossing out from i * i
            for (int j = i * i; j <= n; j += i) {
                isPrime[j] = false;
            }
        }
    }
    return isPrime;
}
```
- **Time Complexity:** $O(N \log(\log N))$ — Harmonic series over primes: $\sum_{p \le N} \frac{N}{p} \approx N \ln(\ln N)$.
- **Space Complexity:** $O(N)$ boolean array.

---

### 2. Greatest Common Divisor (GCD): Euclidean Algorithm

$$\gcd(a, b) = \begin{cases} a & \text{if } b = 0 \\ \gcd(b, a \pmod b) & \text{otherwise} \end{cases}$$

```cpp
int gcd(int a, int b) {
    while (b != 0) {
        int rem = a % b;
        a = b;
        b = rem;
    }
    return a;
}

int lcm(int a, int b) {
    return (a / gcd(a, b)) * b; // Division first prevents intermediate overflow
}
```
- **Time Complexity:** $O(\log(\min(a, b)))$ steps (Lamé's theorem proves consecutive Fibonacci numbers represent the worst case).

---

### 3. Modular Arithmetic & Modular Exponentiation

Properties:
1. $(a + b) \pmod M = ((a \pmod M) + (b \pmod M)) \pmod M$
2. $(a - b) \pmod M = ((a \pmod M) - (b \pmod M) + M) \pmod M$ (Prevents negative results)
3. $(a \times b) \pmod M = ((a \pmod M) \times (b \pmod M)) \pmod M$

#### Fast Modular Exponentiation ($A^B \pmod M$ in $O(\log B)$)
```cpp
long long powerMod(long long base, long long exp, long long mod) {
    long long res = 1;
    base %= mod;

    while (exp > 0) {
        if (exp & 1) { // If exp is odd
            res = (res * base) % mod;
        }
        base = (base * base) % mod;
        exp >>= 1;
    }
    return res;
}
```

---

## 🔥 Interview Questions

### Q1: Why does the Sieve inner loop start at $i \times i$ instead of $2 \times i$?
**Answer:** Any multiple $k \times i$ with $k < i$ has already been marked as composite by a prime factor smaller than $i$. For example, when $i = 5$, $2 \times 5 = 10$ was marked by $2$, $3 \times 5 = 15$ was marked by $3$, and $4 \times 5 = 20$ was marked by $2$. Thus, the earliest unmarked multiple of $i$ is strictly $i \times i$.
"""

t09_files["00_master_index.md"] = r"""# Topic 09: Maths for DSA — Master Index

> **Domain:** Number Theory, Primality Sieving, Euclid's Algorithm, and Modular Exponentiation

---

## 📋 Topic Overview

This module consolidates core mathematical concepts required in computer science: Sieve of Eratosthenes, Euclidean GCD, LCM overflow prevention, modular arithmetic invariants, and binary exponentiation.

---

## 📑 Lecture Index

| # | Lecture Title | Focus Areas | Notes Link | Status |
|---|---|---|---|---|
| **34** | Maths for DSA (Sieve, GCD, Modular Arithmetic) | Sieve of Eratosthenes ($O(N \log \log N)$), Euclidean GCD, fast exponentiation | [01_maths_for_dsa_sieve_gcd_modular_arithmetic.md](./01_maths_for_dsa_sieve_gcd_modular_arithmetic.md) | **AUDITED** |

---

## 🎯 Topic Revision & Interview Preparation
- **Topic Quick Revision:** [topic_revision.md](./topic_revision.md)
- **Topic Interview Question Bank:** [topic_interview_questions.md](./topic_interview_questions.md)
"""

t09_files["topic_revision.md"] = r"""# ⚡ Rapid Revision — Topic 09: Maths for DSA

> **Target:** 5-minute pre-interview refresher on number theory and modular equations.

---

## 🔑 Formulas to Memorize
- **Euclidean GCD:** `gcd(a, b) = b == 0 ? a : gcd(b, a % b)`.
- **LCM Formula:** `(a / gcd(a, b)) * b`.
- **Modular Subtraction:** `(a - b + M) % M`.
- **Sieve Complexity:** $O(N \log \log N)$.
- **Binary Exponentiation:** Divide exponent by 2, square the base, multiply when odd.
"""

t09_files["topic_interview_questions.md"] = r"""# 💼 Topic Interview Question Bank — Topic 09: Maths for DSA

---

### Q1: How do you compute modular division $(a / b) \pmod M$?
**Answer:**
Division is not defined directly under modulo arithmetic. When $M$ is a prime number, by Fermat's Little Theorem:
$$b^{M-1} \equiv 1 \pmod M \implies b \cdot b^{M-2} \equiv 1 \pmod M$$
Thus, the modular multiplicative inverse of $b$ is $b^{-1} \equiv b^{M-2} \pmod M$.
Therefore:
$$(a / b) \pmod M = (a \cdot b^{M-2}) \pmod M$$
computed via modular binary exponentiation in $O(\log M)$ time.
"""

write_files(t09_dir, t09_files)
print("Finished writing Batch 1: Topics 06, 07, 08, 09.")
