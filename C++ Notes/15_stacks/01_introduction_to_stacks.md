# Lecture 68: Introduction to Stacks: LIFO Abstract Data Type

> **One-Line Purpose:** Master the Last-In-First-Out (LIFO) stack invariant, evaluate array-backed vs linked-list implementations, and analyze Call Stack memory architecture in $O(1)$ time per operation.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #68  
> **Video ID:** `0X-fV-1ir9c`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=0X-fV-1ir9c)  
> **Duration:** 22:11  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation: Template Array Stack

```cpp
#include <iostream>
#include <vector>
#include <stdexcept>

using namespace std;

template <typename T>
class Stack {
private:
    vector<T> data;

public:
    void push(T val) {
        data.push_back(val);
    }

    void pop() {
        if (empty()) throw runtime_error("Stack Underflow!");
        data.pop_back();
    }

    T top() const {
        if (empty()) throw runtime_error("Stack is empty!");
        return data.back();
    }

    bool empty() const { return data.empty(); }
    int size() const { return data.size(); }
};

int main() {
    Stack<int> st;
    st.push(10);
    st.push(20);
    cout << "Top: " << st.top() << endl; // 20
    st.pop();
    cout << "Top after pop: " << st.top() << endl; // 10
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(1)$ amortized for `push`, strict $O(1)$ for `pop`, `top`, `empty`.
- **Space Complexity:** $O(N)$ contiguous memory.

---

## 🧠 Core Intuition — Why This Works

**The LIFO Principle:** Think of a stack of plates at a buffet. You always add and remove from the **top**. The last plate placed is the first one taken. This is exactly when LIFO is the right tool: **when the most recently seen thing is the most relevant thing.**

**When is LIFO the right tool?**
- You're tracking the **most recent unresolved item** (e.g., an open parenthesis waiting for its close).
- You need to **undo/backtrack** in reverse order (call stack, browser history).
- You need the **nearest** element to the left/right that satisfies a property (monotonic stacks).

```
STACK VISUALIZATION (push 10, 20, 30 then pop)

push(10)  push(20)  push(30)   pop()    pop()
 ┌────┐    ┌────┐    ┌────┐   ┌────┐   ┌────┐
 │ 10 │    │ 20 │    │ 30 │◄─ │ 20 │   │ 10 │
 └────┘    │ 10 │    │ 20 │   │ 10 │   └────┘
           └────┘    │ 10 │   └────┘
                     └────┘
TOP = 10   TOP = 20  TOP = 30  TOP = 20  TOP = 10
```

**The Call Stack analogy:** Every function call in C++ pushes a **stack frame** onto the OS call stack. When the function returns, the frame is popped. That's why recursive functions "unwind" in reverse order — it's a literal stack!

---

## 🎯 Pattern Recognition — When to Use a Stack

| Problem Cue | Stack Pattern |
|---|---|
| "Balanced brackets / parentheses" | Push opens, match closes |
| "Next/Previous Greater/Smaller Element" | Monotonic Stack |
| "Undo / backtrack / reverse" | Plain Stack |
| "Min/Max with O(1) retrieval" | Auxiliary Stack |
| "Evaluate expression (postfix/prefix)" | Operand Stack |
| "DFS on graph/tree iteratively" | Stack replaces recursion |

**Distinguishing Stack vs Queue:** If you need to process things in the **order they arrived** → Queue. If the **latest thing determines the next action** → Stack.

---

## 🔍 Dry Run Trace

```
Stack<int> st;
st.push(10);  → data = [10],     top = 10
st.push(20);  → data = [10, 20], top = 20
st.top();     → returns 20 (no mutation)
st.pop();     → data = [10],     top = 10
st.empty();   → false (size = 1)
st.pop();     → data = [],       empty
st.empty();   → true
```

---

## ⚠️ Common Interview Mistakes

1. **Forgetting the empty check before `top()` or `pop()`:** Accessing `top()` on an empty stack is undefined behavior with `std::stack`. Always guard with `!st.empty()`.

2. **Confusing stack and queue direction:** Push goes to the top; pop comes from the top. With queues, push goes to the back, pop from the front.

3. **Using `std::stack` when `std::deque` is needed:** If you need to inspect both ends, use a `std::deque`. `std::stack` only gives you `top()`.

4. **Integer overflow in the Min Stack encoding trick:** The formula `2x - minVal` can overflow `int`. Always use `long long` as shown in `06_design_min_stack.md`.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] What is the difference between a Stack and a Queue at the memory layout level?
**Answer:** Both can be backed by contiguous arrays or linked lists. The difference is purely in **which end** supports each operation. A stack uses the same end for both push and pop (LIFO). A queue uses one end for enqueue and the other for dequeue (FIFO). `std::stack` in C++ is a **container adaptor** that wraps a `std::deque` by default but can wrap `std::vector` or `std::list`. `std::queue` also wraps `std::deque`.

### Q2: [Conceptual] Why does `std::stack` use `std::deque` as its default backing container instead of `std::vector`?
**Answer:** `std::deque` provides $O(1)$ push/pop at **both ends** without reallocation. While `std::vector` would also work (push_back/pop_back are $O(1)$ amortized), `deque` avoids the costly $O(N)$ reallocation when the vector doubles. The trade-off is slightly worse cache performance with `deque` due to its segmented memory layout.

### Q3: [Debugging] What is wrong with the following code?
```cpp
stack<int> st;
st.push(5);
st.pop();
cout << st.top(); // What happens?
```
**Answer:** This is **undefined behavior**. After `pop()`, the stack is empty. Calling `top()` on an empty `std::stack` has undefined behavior (no exception is thrown by default). The fix: always check `!st.empty()` before calling `top()` or `pop()`.

### Q4: [Extension] How would you implement a stack that supports `push`, `pop`, `top`, AND `getMin` all in O(1) time?
**Answer:** Use an auxiliary min-stack in parallel. When pushing value `v`, also push `min(v, minStack.top())` to the min-stack. `getMin()` is simply `minStack.top()`. When popping, pop from both stacks simultaneously. This uses $O(N)$ auxiliary space. The $O(1)$ space version uses the encoding trick `2x - minVal`. (See `06_design_min_stack.md` for full implementation.)

### Q5: [System Design] How does the CPU call stack work, and what causes a Stack Overflow?
**Answer:** Each function call allocates a **stack frame** on the process's call stack segment containing: the return address, local variables, saved registers, and function arguments. Stack frames are pushed on function entry and popped on return. The call stack has a fixed maximum size (typically 1–8 MB on most OS). A **Stack Overflow** occurs when recursive calls are too deep (no base case, or depth exceeds the limit), causing the stack pointer to exceed the segment boundary. The OS signals `SIGSEGV`.

### Q6: [Derivation] Prove that all operations on a vector-backed stack are O(1) amortized.
**Answer:** Using the **potential method**: define $\Phi = $ number of elements in the vector. `push()` costs $O(1)$ amortized because doubling happens once every $N$ pushes (doubling costs $O(N)$ but spreads over $N$ operations → $O(1)$ each). `pop()` and `top()` are always $O(1)$ without reallocation. Total work for $N$ operations is $O(N)$, so amortized $O(1)$ per operation.

### Q7: [OOP Extension] How would you make a thread-safe stack in C++?
**Answer:**
```cpp
#include <stack>
#include <mutex>
#include <stdexcept>
template<typename T>
class ThreadSafeStack {
    std::stack<T> st;
    mutable std::mutex mtx;
public:
    void push(T val) {
        std::lock_guard<std::mutex> lock(mtx);
        st.push(val);
    }
    T pop() {
        std::lock_guard<std::mutex> lock(mtx);
        if (st.empty()) throw std::runtime_error("empty");
        T val = st.top();
        st.pop();
        return val;
    }
};
```
The key insight: `top()` and `pop()` must be **combined** into a single locked operation to avoid a TOCTOU (Time-Of-Check-Time-Of-Use) race condition.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Hint |
|---|---------|----------|
| 155 | Min Stack | Auxiliary stack or encoding trick |
| 20 | Valid Parentheses | Push opens, match closes |
| 232 | Implement Queue using Stacks | Two-stack amortized model |
| 84 | Largest Rectangle in Histogram | Monotonic increasing stack |
| 739 | Daily Temperatures | Next greater element variant |

---

## 🔗 Cross-Topic Connections

- **Recursion:** Every recursive algorithm has an equivalent iterative version using an explicit stack. DFS on graphs/trees is the canonical example.
- **Monotonic Stack:** Specialized stack invariant used in NGE, histogram, trapping rainwater problems.
- **Queues:** Implement Queue using Stacks (LeetCode 232) — the duality of these two structures.
- **Dynamic Programming:** Parsing expression problems (arithmetic evaluators) combine DP with stack-based operator precedence.
- **Graphs:** Iterative DFS uses an explicit stack. Topological sort (Kahn's algorithm) uses a queue; DFS-based uses an implicit stack.

---

## ⚡ 2-Minute Revision Flash Card

- **LIFO**: Last-In, First-Out. Top is the only accessible element.
- **Operations**: `push()` → $O(1)$ amortized, `pop()` / `top()` / `empty()` → strict $O(1)$.
- **ALWAYS** check `!st.empty()` before `top()` or `pop()` — undefined behavior otherwise.
- **Use Stack when**: the most recently seen unresolved item determines the next action.
- **Monotonic Stack**: maintain a stack sorted in increasing or decreasing order — kills "nearest greater/smaller" problems in $O(N)$.
