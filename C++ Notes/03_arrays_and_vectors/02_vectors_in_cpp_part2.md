# Lecture 09: Vectors in C++ — Dynamic Arrays & Amortized Analysis

> **One-Line Purpose:** Master `std::vector` internal architecture, Heap dynamic memory reallocation, the geometric doubling capacity mechanism, Amortized $O(1)$ complexity, and range-based iterators.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #09  
> **Video ID:** `NWg38xWYzEg`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=NWg38xWYzEg)  
> **Duration:** 40:06  
> **Transcript:** `.transcripts/03_arrays_and_vectors/009_Vectors_in_C_____Arrays_Part_2___DSA_Series_by_Shradha_Ma_am___Lecture_9.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The fundamental limitations of static arrays and why dynamic arrays (`std::vector`) are required.
- Memory distribution: Vector header on the Stack, underlying data buffer on the Heap.
- The critical distinction between `size()` (elements currently held) and `capacity()` (total allocated buffer slots).
- How the geometric doubling growth strategy guarantees **Amortized $O(1)$** `push_back` operations.
- Vector member functions: `push_back`, `pop_back`, `front`, `back`, `at()`, `operator[]`, and `empty()`.
- Range-based `for` loops by value vs by reference.

---

## 🔵 Lecture Context

In modern C++ and competitive programming, raw static arrays are rarely used in isolation due to fixed-size constraints and memory leaks. `std::vector` is the default standard sequence container. Understanding how it manages Heap memory prevents performance pitfalls like iterator invalidation and repeated memory reallocation.

---

## 1. Static Array vs Dynamic Vector

> 🔵 **Lecture Content**

| Feature | Static Array (`int arr[N]`) | Dynamic Vector (`std::vector<int>`) |
|---|---|---|
| **Size Determination** | Fixed at compile time | Completely dynamic, expands at runtime |
| **Memory Region** | Typically Stack memory | Elements stored on the **Heap** |
| **Pass-by-Value** | Decays into raw pointer | Can be copied or passed by reference (`&`) |
| **Size Tracking** | Must manually pass `size` | Self-tracking via `.size()` method |

---

## 2. Vector Internal Architecture: Size vs Capacity

A `std::vector` object consists of three internal pointers on the Stack (typically 24 bytes total on 64-bit systems):
1. Pointer to the beginning of the buffer.
2. Pointer to the current end of elements (`size`).
3. Pointer to the end of allocated memory (`capacity`).

```
Stack:
[ vector object: 24 bytes ]
         │
         ▼ (points to Heap)
Heap:
[  10  |  20  |  30  |  --  |  --  ]
 ▲                     ▲           ▲
 begin()              size()      capacity()
 (size = 3, capacity = 5)
```

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> vec;

    for (int i = 1; i <= 5; i++) {
        vec.push_back(i);
        cout << "Element: " << i 
             << " | Size: " << vec.size() 
             << " | Capacity: " << vec.capacity() << endl;
    }
    return 0;
}
```

### Output:
```text
Element: 1 | Size: 1 | Capacity: 1
Element: 2 | Size: 2 | Capacity: 2
Element: 3 | Size: 3 | Capacity: 4
Element: 4 | Size: 4 | Capacity: 4
Element: 5 | Size: 5 | Capacity: 8
```

> 🧠 **Brain Trigger**
> 
> Notice how `capacity` jumps from $1 \to 2 \to 4 \to 8$. Why does the vector **double** its capacity instead of increasing by $+1$ each time?
> 
> **Answer:** If the vector increased capacity by $+1$ on each insertion, every `push_back` would require allocating a new array, copying all $N$ elements, and deleting the old array, resulting in $\sum_{i=1}^N i = O(N^2)$ time for $N$ insertions ($O(N)$ per insertion!). Geometric doubling amortizes the copying cost down to $O(1)$ average per insertion.

---

## 3. Mathematical Proof: Amortized $O(1)$ `push_back`

Consider inserting $N = 2^k$ elements into an initially empty vector:
- Insertions that require reallocation and copying occur at powers of 2: $1, 2, 4, 8, \dots, 2^{k-1}$.
- Total element copies across all reallocations:
  $$\text{Total Copies} = 1 + 2 + 4 + 8 + \dots + 2^{k-1} = 2^k - 1 = N - 1$$
- Total operations for $N$ insertions = $N \text{ (direct writes)} + (N - 1) \text{ (copies)} = 2N - 1$.
- Average time per insertion:
  $$\text{Amortized Cost} = \frac{2N - 1}{N} \approx 2 = O(1)$$

---

## 4. Vector Member Functions & Traversal

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> vec = {10, 20, 30, 40};

    vec.push_back(50); // Append at end
    vec.pop_back();    // Removes 50

    cout << "Front: " << vec.front() << endl; // 10
    cout << "Back:  " << vec.back() << endl;  // 40
    cout << "at(2): " << vec.at(2) << endl;   // 30 (bounds-checked)

    // Traversal 1: Range-based for loop (by value - copy)
    for (int val : vec) {
        cout << val << " ";
    }
    cout << endl;

    // Traversal 2: Range-based for loop (by reference - modifies original)
    for (int &val : vec) {
        val *= 2; // Doubled in-place
    }

    return 0;
}
```

---

## ⚠️ Common Mistakes

1. **Passing Vectors by Value to Functions:**
   ```cpp
   void printVec(vector<int> v) // EXPENSIVE COPY! Deep-copies all elements onto heap.
   void printVec(const vector<int> &v) // OPTIMAL: Constant reference (0 copy overhead).
   ```
2. **Accessing Unallocated Indices with `[]`:**
   ```cpp
   vector<int> v;
   v[0] = 10; // SEGMENTATION FAULT! v.size() is 0; index 0 does not exist yet!
   v.push_back(10); // Correct
   ```

---

## 🔥 Interview Questions

### Q1: What is Iterator Invalidation in `std::vector`?
- **Short Answer:** When a vector reallocates its internal buffer during a `push_back` or `insert`, existing pointers, references, and iterators pointing to elements in the old buffer become **dangling pointers**.
- **Detailed Explanation:** When `capacity` is exceeded, the vector allocates memory at a completely new heap address and frees the previous buffer. Any iterator referencing the old address now points to deallocated memory. Accessing it invokes Undefined Behavior.

### Q2: How can you prevent frequent reallocations if the final vector size is known in advance?
- **Short Answer:** Use `vec.reserve(expectedSize);`.
- **Detailed Explanation:** `reserve()` pre-allocates a capacity of `expectedSize` on the heap without changing `size()`. All subsequent `push_back` calls up to that size run in strict $O(1)$ worst-case time with **zero** reallocations.

---

## Key Takeaways

1. **Heap Allocation:** Vector data lives dynamically on the heap; metadata lives on the stack.
2. **Doubling Strategy:** Doubles capacity when full to guarantee $O(1)$ amortized insertion.
3. **Reference Passing:** Always pass vectors as `const vector<T>&` unless a copy is explicitly required.
4. **Performance Tuning:** Use `.reserve()` to eliminate reallocation overhead.

---

## ⚡ 2-Minute Revision

- `size()`: Number of active elements.
- `capacity()`: Total allocated buffer slots ($capacity \ge size$).
- `push_back()`: Amortized $O(1)$, worst-case $O(N)$ during reallocation.
- `pop_back()`: Strictly $O(1)$.
- `at(i)` vs `[i]`: `at(i)` throws exception if out of range; `[i]` does unchecked memory dereference.
