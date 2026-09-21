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

## 🧠 Core Intuition — Why This Works
The STL separates algorithms from data structures using **Iterators**. An iterator is an object that points to an element in a container and allows algorithms to traverse them uniformly without knowing the container's internal memory layout. `std::vector` uses contiguous memory, providing raw pointer arithmetic. `std::map` uses a Red-Black Tree, where moving the iterator traverses the tree in-order. By decoupling these, `std::sort` can operate on any container that provides Random Access Iterators.

## 🎯 Pattern Recognition — When to Use This
- **Need fast lookup/deduplication?** `unordered_set` / `unordered_map` ($O(1)$).
- **Need sorted keys or range queries?** `set` / `map` ($O(\log N)$).
- **Need dynamically growing arrays?** `vector` ($O(1)$ amortized push).
- **Need fast front & back insertion?** `deque` ($O(1)$).
- **Need Kth largest/smallest?** `priority_queue` (Heap, $O(\log N)$).

## 📐 Algorithm Walk-Through
**Custom Sorting with Lambdas:**
When using `std::sort`, the lambda comparator `[](const Type& a, const Type& b)` must return `true` if `a` should come strictly before `b`.
- Example: Sort descending by score, ascending by ID on tie.
- If `a.score > b.score`, return `true` (A is placed before B).
- If `a.score == b.score`, check if `a.id < b.id`. Return `true` if lower.
- **Rule of strict weak ordering:** If `a == b` conceptually, the comparator MUST return `false`. Never use `>=` or `<=`.

## 🔍 Dry Run Trace (Lower vs Upper Bound)
`vector = [1, 2, 4, 4, 4, 6]`, sorted.
- `lower_bound(vector, 4)`: Returns iterator to the *first* `4` (index 2).
- `upper_bound(vector, 4)`: Returns iterator to the *first element strictly greater than* `4`, which is `6` (index 5).
- Distance: `upper_bound - lower_bound = 5 - 2 = 3` (Exactly the count of `4`s).

## ⚠️ Common Interview Mistakes
- **Comparator returning true on equality:** This breaks strict weak ordering and can cause `std::sort` to crash or infinite loop (segmentation fault) in C++! Always use `<` or `>`.
- **Calling `map[key]` to check existence:** Using `if (myMap[key] == val)` implicitly creates a node in the map with default values if `key` didn't exist, silently increasing the map size. Always use `if (myMap.find(key) != myMap.end())` or `if (myMap.count(key))`.
- **Erase invalidating iterators:** `vector.erase(it)` invalidates all iterators pointing to elements after the erased one.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Why is `unordered_map` $O(1)$ average but $O(N)$ worst case?
**Answer:** `unordered_map` relies on hashing. If an adversary knows the hash function (or if the hash is poor), they can insert $N$ keys that all hash to the same bucket. The Hash Table degenerates into a single linked list, taking $O(N)$ to search. `std::map` guarantees $O(\log N)$ regardless of input.

### Q2: What happens when a `std::vector` runs out of capacity?
**Answer:** It allocates a new, larger memory block (usually double the current capacity), copies all existing elements to the new block, and deletes the old block. This takes $O(N)$ time, but because it doubles, the amortized cost per insertion remains $O(1)$.

### Q3: How do you initialize a Min-Heap priority queue?
**Answer:** `priority_queue<int, vector<int>, greater<int>> minHeap;`. The default is `less<int>` which produces a Max-Heap.

### Q4: When would you use a `std::list` (doubly linked list) in modern C++?
**Answer:** Almost never, due to CPU cache misses caused by non-contiguous memory allocation. `std::vector` is vastly superior for almost all use cases except when you need massive amounts of insertions/deletions exactly in the middle of a huge container AND you already have the iterator to that location.

## 🏆 Related Problems (Leetcode)
- **LeetCode 146:** LRU Cache (Requires `std::list` + `std::unordered_map`)
- **LeetCode 347:** Top K Frequent Elements (Requires `std::unordered_map` + `std::priority_queue`)
- **LeetCode 23:** Merge k Sorted Lists (Requires `std::priority_queue`)

## 🔗 Cross-Topic Connections
- **Graphs:** BFS uses `queue`, DFS can use `stack`, Dijkstra's Algorithm uses `priority_queue` (min-heap).
- **Binary Search:** `lower_bound` and `upper_bound` are native binary search implementations.

## ⚡ 2-Minute Revision Flash Card
- **Vector:** Dynamic array. Amortized $O(1)$ back insertion, $O(1)$ random access.
- **Unordered Map:** Hash table. $O(1)$ search. **Map:** Red-Black Tree. $O(\log N)$ search, sorted keys.
- **Priority Queue:** Heap. Default is Max-Heap. $O(\log N)$ push/pop, $O(1)$ top.
- **Lower Bound:** Iterator to first element $\ge X$.
- **Upper Bound:** Iterator to first element $> X$.
- **Custom Sort Trap:** Never return `true` if `a == b`.
