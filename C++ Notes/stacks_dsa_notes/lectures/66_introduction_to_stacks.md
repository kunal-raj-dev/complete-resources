# Lecture 66 — Introduction to Stacks

[Study index](../README.md) · [Next: Valid Parentheses](67_valid_parentheses.md)

**Source:** [Lecture 66](https://www.youtube.com/watch?v=0X-fV-1ir9c). **Verification:** full auto-caption sequence reviewed; list implementation visually checked. Captions are imperfect, so this chapter uses original wording and corrected technical terminology. [Coverage record](../SOURCE_COVERAGE.md#lecture-66).

**Prerequisites:** C++ classes, vectors, basic linked lists, and the idea of a recursive function call.

## Contents

- [1. The stack and its operations](#1-the-stack-and-its-operations)
- [2. Implementation using a vector](#2-implementation-using-a-vector)
- [3. Implementation using a linked list](#3-implementation-using-a-linked-list)
- [4. Using the C++ STL stack](#4-using-the-c-stl-stack)
- [5. Additional explanation — capacity and ownership](#5-additional-explanation--capacity-and-ownership)
- [6. Pitfalls, interview questions, and revision](#6-pitfalls-interview-questions-and-revision)

## 1. The stack and its operations

**Lecture flow: approximately 00:33–04:53.** A stack is a collection that exposes one end, called the **top**, for insertion and removal. The most recently inserted surviving item is removed first: **LIFO**, or last in, first out. A stack of books is a useful model: add a book on top, read the top book, remove the top book.

The lecture connects this to the recursion call stack. A function's unfinished work stays suspended while a deeper call runs; the deeper call completes before execution resumes in its caller. The data structure studied here is an explicit stack you manage in your program. The runtime call stack also contains call frames, local state, and return information.

| Operation   | Meaning                       | Does it change the stack? |
| ----------- | ----------------------------- | ------------------------- |
| `push(x)` | Insert`x` at the top        | Yes                       |
| `pop()`   | Remove the top item           | Yes                       |
| `top()`   | Read the top item             | No                        |
| `empty()` | Check whether no items remain | No                        |
| `size()`  | Count stored items            | No                        |

A queue's removal order is FIFO: the oldest item leaves first. This difference determines whether the latest or earliest unfinished item gets processed next.

**Original dry run.** All stack displays in these notes run **bottom → top**, so the rightmost item is the top.

| Operation   | Before      | After       | Observation         |
| ----------- | ----------- | ----------- | ------------------- |
| `push(4)` | `[]`      | `[4]`     | Top is 4            |
| `push(9)` | `[4]`     | `[4,9]`   | Top is 9            |
| `push(2)` | `[4,9]`   | `[4,9,2]` | Top is 2            |
| `top()`   | `[4,9,2]` | `[4,9,2]` | Returns 2           |
| `pop()`   | `[4,9,2]` | `[4,9]`   | Removes 2           |
| `pop()`   | `[4,9]`   | `[4]`     | Removes 9           |
| `pop()`   | `[4]`     | `[]`      | Stack becomes empty |

Notice that duplicates would be allowed. A stack stores occurrences, not a mathematical set of distinct values.

## 2. Implementation using a vector

**Lecture flow: approximately 04:53–14:35.** The lecture first chooses a vector so capacity can grow instead of being fixed in advance. Represent the stack's top by the vector's **last element**. Appending and removing at this end preserve LIFO order.

| Stack operation | Vector operation                                              |
| --------------- | ------------------------------------------------------------- |
| `push(x)`     | `push_back(x)`                                              |
| `pop()`       | `pop_back()`                                                |
| `top()`       | `back()`, equivalent to indexing `size()-1` when nonempty |
| `empty()`     | `empty()`                                                   |

**Invariant:** the vector contains precisely the stack's surviving items in insertion order. Its back is therefore the newest surviving item. Push appends a newest item; pop removes it; both preserve the invariant.

```cpp
#include <cstddef>
#include <stdexcept>
#include <vector>

class VectorStack {
    std::vector<int> data;
public:
    void push(int x) { data.push_back(x); }
    bool empty() const { return data.empty(); }
    std::size_t size() const { return data.size(); }
    int top() const {
        if (empty()) throw std::underflow_error("top on empty stack");
        return data.back();
    }
    void pop() {
        if (empty()) throw std::underflow_error("pop on empty stack");
        data.pop_back();
    }
};
```

Usage: construct `VectorStack s`, call `s.push(4)` and `s.push(9)`, then repeatedly read `s.top()` and call `s.pop()` while `!s.empty()`. The observed removal sequence is `9,4`.

**Technical correction to the lecture's constant-time description:** vector push is **amortized O(1)**. One push can cost O(k) when the vector reallocates and moves its k existing elements. Pop, top, empty, and size are O(1) for integers. Reallocation also invalidates existing references and pointers into the vector. See the [C++ vector modifier specification](https://eel.is/c++draft/vector.modifiers).

The guards above are an **additional safety choice**. The lecture demonstration operates on nonempty stacks. The standard vector does not promise to throw on an invalid `back()` or `pop_back()` call; do not rely on that behavior.

## 3. Implementation using a linked list

**Lecture flow: approximately 14:35–20:19.** Make the list's **front/head** the stack's top. A new top becomes a new head, and removing the top removes the head. The lecture uses STL `std::list`, rather than rebuilding a node class.

| Stack operation | List operation    |
| --------------- | ----------------- |
| `push(x)`     | `push_front(x)` |
| `pop()`       | `pop_front()`   |
| `top()`       | `front()`       |

```cpp
#include <cstddef>
#include <list>
#include <stdexcept>

class ListStack {
    std::list<int> data;
public:
    void push(int x) { data.push_front(x); }
    bool empty() const { return data.empty(); }
    std::size_t size() const { return data.size(); }
    int top() const {
        if (empty()) throw std::underflow_error("top on empty stack");
        return data.front();
    }
    void pop() {
        if (empty()) throw std::underflow_error("pop on empty stack");
        data.pop_front();
    }
};
```

After pushes `4,9,2`, the list's physical **head → tail** order is `2 → 9 → 4`, while our bottom-to-top stack display is `[4,9,2]`. These are two views of the same state, not contradictory orders.

**Invariant:** the list's head is the last inserted surviving element. Prepending changes the head to the newest item; removing the head reveals the next newest item. Each operation takes O(1) data-structure work. Memory is O(n), with node/link overhead. Allocation cost is treated under the usual RAM-model convention.

**Additional explanation:** `std::list` is a doubly linked list. A singly linked list is sufficient for a stack if all operations use the head. Appending at the tail of a singly linked list makes top removal expensive unless predecessor information is also maintained.

## 4. Using the C++ STL stack

**Lecture flow: approximately 20:19–22:00.** For problem solving, use the standard adaptor instead of writing a custom class every time. Include `<stack>` and specify the element type.

```cpp
#include <stack>
#include <vector>

std::vector<int> lifoOrder(const std::vector<int>& input) {
    std::stack<int> s;
    for (int x : input) s.push(x);
    std::vector<int> removed;
    while (!s.empty()) {
        removed.push_back(s.top()); // Read before removing.
        s.pop();                   // pop returns void.
    }
    return removed;
}
```

Usage: `lifoOrder({4,9,2})` returns `{2,9,4}`. Time is O(n), auxiliary stack space O(n), and returned output space O(n).

**Additional explanation:** `std::stack<T>` is an adaptor that restricts an underlying container to stack operations. Its default container is `std::deque<T>`. You can choose `std::stack<int, std::vector<int>>` or `std::stack<int, std::list<int>>`; the adaptor uses the underlying container's back operations. Thus the list-backed adaptor uses the **back**, while our lecture-style `ListStack` uses the **front**. Both implement LIFO correctly. The [C++ stack definition](https://eel.is/c++draft/stack.defn) specifies this relationship. There is no public iterator interface for `std::stack`.

## 5. Additional explanation — capacity and ownership

### Fixed-capacity array stack: lecture homework completed

The lecture assigns implementing a stack with a static array. Use `count` as the next free position. Full means `count == Capacity`; empty means `count == 0`.

```cpp
#include <array>
#include <cstddef>
#include <stdexcept>

template <std::size_t Capacity>
class FixedStack {
    std::array<int, Capacity> data{};
    std::size_t count = 0;
public:
    bool empty() const { return count == 0; }
    std::size_t size() const { return count; }
    void push(int x) {
        if (count == Capacity) throw std::overflow_error("stack full");
        data[count++] = x;
    }
    int top() const {
        if (empty()) throw std::underflow_error("stack empty");
        return data[count - 1];
    }
    void pop() {
        if (empty()) throw std::underflow_error("stack empty");
        --count;
    }
};
```

Usage: `FixedStack<2> s` accepts two pushes; a third throws. All operations take worst-case O(1); reserved storage is O(Capacity), including unused slots. Overflow here means exhausting capacity; **integer overflow** is a separate arithmetic problem.

### A node implementation with explicit ownership

This is an extension for interviews asking for a stack from scratch. Every allocated node must be deleted exactly once. Copying a raw owning head pointer would make two stacks share ownership and risk double deletion; the small teaching class below disables copy and move.

```cpp
#include <cstddef>
#include <stdexcept>

class LinkedStack {
    struct Node { int value; Node* next; };
    Node* head = nullptr;
    std::size_t count = 0;
public:
    LinkedStack() = default;
    LinkedStack(const LinkedStack&) = delete;
    LinkedStack& operator=(const LinkedStack&) = delete;
    LinkedStack(LinkedStack&&) = delete;
    LinkedStack& operator=(LinkedStack&&) = delete;
    ~LinkedStack() { while (!empty()) pop(); }
    bool empty() const { return head == nullptr; }
    std::size_t size() const { return count; }
    void push(int x) {
        head = new Node{x, head};
        ++count;
    }
    int top() const {
        if (empty()) throw std::underflow_error("stack empty");
        return head->value;
    }
    void pop() {
        if (empty()) throw std::underflow_error("stack empty");
        Node* old = head;
        head = head->next;
        delete old;
        --count;
    }
};
```

Destruction takes O(n), although each individual pop is O(1). This matters when discussing the complete object's lifetime.

## 6. Pitfalls, interview questions, and revision

- `pop()` removes; it does not return the removed value. Read `top()` first.
- Never calculate `size()-1` on an empty vector: its unsigned size can underflow.
- A dynamic container has no fixed application-level capacity, but available memory still limits growth.
- Do not use `erase(begin())` to implement the top of a vector stack: shifting elements costs O(n).
- Prefer a vector for compact storage and locality; prefer a fixed array when capacity is known; understand allocation overhead for nodes.
- Call-stack depth is also memory usage. Recursive algorithms can overflow the runtime stack even when their time complexity is acceptable.

**Interview check:** Why is the vector's back a good top? Why is the singly linked list's head a good top? Explain one expensive vector push without contradicting amortized O(1). What would a safe copy constructor for `LinkedStack` have to do?

**Lecture follow-up:** revise C++ STL basics before later problems. The static-array exercise above is the lecture's implementation homework; the raw-node class is added context.

**Revision:** identify one top end; push there, pop there, read there. A stack reverses the order of pending work. Implementation choices change storage and operation costs, not LIFO behavior.
