# Lecture 27: C++ Standard Template Library (STL) Complete Masterclass

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
