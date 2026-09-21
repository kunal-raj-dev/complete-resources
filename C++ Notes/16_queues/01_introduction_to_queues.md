# Lecture 79: Introduction to Queues: FIFO Architecture & Implementations

> **One-Line Purpose:** Master the FIFO (First-In-First-Out) abstract data type, front/back pointer invariants, dynamic array vs linked list backing stores, and boundary condition handling in $O(1)$ amortized time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #79  
> **Video ID:** `Khf9v67Ya30`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=Khf9v67Ya30)  
> **Duration:** 18:55  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- FIFO (First-In, First-Out) invariant vs LIFO (Stack).
- Core operations: `push()` (enqueue), `pop()` (dequeue), `front()`, `back()`, `empty()`.
- Linear array queue pitfalls: False overflow issue where `rear == capacity - 1` but earlier slots are vacant.
- Dynamic linked list node-based implementation with $O(1)$ operations.

---

## 🔵 Complete C++ Implementation: Linked List Queue

```cpp
#include <iostream>
#include <stdexcept>

using namespace std;

template <typename T>
class QueueLL {
private:
    struct Node {
        T data;
        Node* next;
        Node(T val) : data(val), next(nullptr) {}
    };

    Node* head; // Front of queue (pop from here)
    Node* tail; // Back of queue (push here)
    int count;

public:
    QueueLL() : head(nullptr), tail(nullptr), count(0) {}

    ~QueueLL() {
        while (!empty()) {
            pop();
        }
    }

    void push(T val) {
        Node* newNode = new Node(val);
        if (empty()) {
            head = tail = newNode;
        } else {
            tail->next = newNode;
            tail = newNode;
        }
        count++;
    }

    void pop() {
        if (empty()) throw runtime_error("Queue Underflow!");
        Node* temp = head;
        head = head->next;
        if (!head) tail = nullptr; // Queue became empty
        delete temp;
        count--;
    }

    T front() const {
        if (empty()) throw runtime_error("Queue is empty!");
        return head->data;
    }

    bool empty() const { return count == 0; }
    int size() const { return count; }
};

int main() {
    QueueLL<int> q;
    q.push(10);
    q.push(20);
    q.push(30);

    cout << "Front: " << q.front() << endl; // 10
    q.pop();
    cout << "New Front: " << q.front() << endl; // 20
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(1)$ for `push()`, `pop()`, and `front()`.
- **Space Complexity:** $O(N)$ memory for node pointers.

## 🧠 Core Intuition — Why This Works
A Queue is exactly like a line of people waiting at a ticket counter. The first person to join the line is the first person to get served and leave. This is the **First-In-First-Out (FIFO)** principle. 
To implement this efficiently using a Linked List, we need two pointers: `head` (the front of the line, where people leave) and `tail` (the back of the line, where people join). By keeping a `tail` pointer, we avoid traversing the entire list every time someone joins, achieving $O(1)$ enqueue time.

## 🎯 Pattern Recognition — When to Use This
- **"Process items in the exact order they were received"**: e.g., task scheduling, print queues, web server request handling.
- **"Level-by-Level exploration"**: This is the core engine for **Breadth-First Search (BFS)** in Trees and Graphs.
- **"Sliding Window algorithms"**: Queues (specifically Deques) are often used to maintain elements in a moving window.

## 🔍 Dry Run Trace
**Example:** `q = QueueLL()`, operations: `push(1), push(2), pop()`

1. **`push(1)`**: 
   - `newNode(1)`. `empty()` is true.
   - `head = tail = newNode`. `count = 1`.
   - `head` -> [1], `tail` -> [1].
2. **`push(2)`**: 
   - `newNode(2)`. `empty()` is false.
   - `tail->next = newNode`. (Node 1's next points to 2).
   - `tail = newNode`. `count = 2`.
   - `head` -> [1] -> [2] <- `tail`.
3. **`pop()`**:
   - `empty()` is false.
   - `temp = head` (points to Node 1).
   - `head = head->next` (head now points to Node 2).
   - Delete `temp`. `count = 1`.
   - `head` -> [2] <- `tail`.

## ⚠️ Common Interview Mistakes
1. **Forgetting to update `tail` on the last `pop()`:** If the queue has 1 element and you `pop()`, `head` becomes `nullptr`. If you don't explicitly set `tail = nullptr`, `tail` will become a dangling pointer!
2. **Memory Leaks:** In C++, if you implement a linked list queue, you must provide a destructor `~QueueLL()` that pops all elements, otherwise, memory allocated via `new` is leaked when the queue goes out of scope.
3. **Using an Array instead of a Linked List naively:** Popping from the front of a standard array/vector takes $O(N)$ time because all other elements must shift left. To use an array in $O(1)$ time, you MUST implement a **Circular Queue**.

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Why does C++ `std::queue` use `std::deque` as its default underlying container instead of `std::list` (Linked List)?
Cache locality! A Linked List allocates memory for each node randomly on the heap, causing cache misses when traversing. A `std::deque` allocates fixed-size contiguous chunks (arrays) of memory, providing much better CPU cache locality while still allowing $O(1)$ insertions at both ends without full reallocations.

### Q2: What happens if you call `pop()` on an empty `std::queue` in C++?
It leads to **Undefined Behavior (UB)**. The standard library does not throw an exception for performance reasons. It is the programmer's responsibility to always check `if (!q.empty())` before calling `pop()` or `front()`.

### Q3: How do you make a queue Thread-Safe in a concurrent environment?
You must wrap the core operations (`push`, `pop`, `front`) with a Mutex (mutual exclusion lock). Additionally, for a Producer-Consumer scenario, you would use a Condition Variable so the consumer can `wait()` efficiently until the queue is no longer empty, rather than spinning in an infinite loop.

### Q4: Can a Queue be implemented using Recursion?
Yes, the Call Stack (which is a LIFO structure) can be used to emulate a Queue by utilizing the unraveling phase of recursion. However, this is just "Queue using Stacks" in disguise, and limits the queue size to the maximum stack depth (risk of Stack Overflow).

## 🏆 Related Problems (Leetcode)
- **[232. Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/)**: Emulate queue behavior.
- **[622. Design Circular Queue](https://leetcode.com/problems/design-circular-queue/)**: Array-based $O(1)$ queue.
- **[1700. Number of Students Unable to Eat Lunch](https://leetcode.com/problems/number-of-students-unable-to-eat-lunch/)**: Great simulation problem using a queue.

## 🔗 Cross-Topic Connections
- **Breadth-First Search (BFS)**: Uses a Queue to traverse a graph/tree layer by layer.
- **Operating Systems**: OS task schedulers (Round Robin) use Queues heavily.

## ⚡ 2-Minute Revision Flash Card
- **Queue Principle:** FIFO (First-In, First-Out).
- **Linked List Implementation:** Need both `head` (for $O(1)$ pop) and `tail` (for $O(1)$ push).
- **Trap 1:** If popping the last element, ensure `tail = nullptr`.
- **Trap 2:** Array-based queues without a circular design take $O(N)$ to pop or waste unbounded space.
- **C++ STL:** `std::queue<T> q`. Uses `push()`, `pop()`, `front()`, `back()`, `empty()`.
