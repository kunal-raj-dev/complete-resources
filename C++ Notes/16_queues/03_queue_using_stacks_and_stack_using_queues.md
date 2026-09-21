# Lecture 81: Implement Queue using Stacks & Stack using Queues (LeetCode 232 & 225)

> **One-Line Purpose:** Emulate FIFO behavior using two LIFO stacks with amortized $O(1)$ dequeue, and emulate LIFO behavior using a single circular queue in $O(N)$ push / $O(1)$ pop.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #81  
> **Video ID:** `sFvP5Ois0CE`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=sFvP5Ois0CE)  
> **Duration:** 15:47  
> **Status:** AUDITED  

---

## 🔵 Two-Stack Queue: The In/Out Buffer Model
- `inputStack`: Receives newly enqueued elements ($O(1)$ push).
- `outputStack`: Delivers elements in correct FIFO order.
- When `outputStack` is empty, dump all elements from `inputStack` into `outputStack`. Each element moves across stacks at most twice, yielding **Amortized $O(1)$** per operation!

---

## 💻 Complete C++ Implementation

```cpp
#include <stack>
#include <iostream>

using namespace std;

class MyQueue {
private:
    stack<int> inSt;
    stack<int> outSt;

    void transfer() {
        if (outSt.empty()) {
            while (!inSt.empty()) {
                outSt.push(inSt.top());
                inSt.pop();
            }
        }
    }

public:
    MyQueue() {}

    void push(int x) {
        inSt.push(x);
    }

    int pop() {
        transfer();
        int val = outSt.top();
        outSt.pop();
        return val;
    }

    int peek() {
        transfer();
        return outSt.top();
    }

    bool empty() {
        return inSt.empty() && outSt.empty();
    }
};

int main() {
    MyQueue q;
    q.push(1);
    q.push(2);
    cout << "Peek: " << q.peek() << endl; // 1
    cout << "Pop:  " << q.pop()  << endl; // 1
    cout << "Empty: " << (q.empty() ? "YES" : "NO") << endl; // NO
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** Push: $O(1)$, Pop/Peek: Amortized $O(1)$, Worst-case $O(N)$.
- **Space Complexity:** $O(N)$ elements stored.

## 🧠 Core Intuition — Why This Works

### 1. Queue using Stacks
A stack reverses the order of elements (LIFO). If you push `1, 2, 3` into a stack and pop them, they come out as `3, 2, 1`. If you take that reversed order and push it into a *second* stack, they are reversed again! Popping from the second stack yields `1, 2, 3` — which is exactly the original (FIFO) order. 
Thus, `Stack1` (Input) acts as a mailbox. `Stack2` (Output) acts as the delivery route. We only dump the mailbox into the delivery route when the delivery route is completely empty.

### 2. Stack using Queues
A queue preserves order. To make it behave like a stack (where the most recently added item is popped first), every time we push a new element `x` to the back of the queue, we simply `pop` all the existing elements from the front of the queue and immediately `push` them back to the rear! This effectively rotates the entire queue, pushing `x` all the way to the front, ready to be popped in $O(1)$ time.

## 🎯 Pattern Recognition — When to Use This
- **"Implement Data Structure A using B"**: Direct application.
- **"Design a queue with amortized $O(1)$ operations using limited primitives"**: E.g., in functional programming languages or systems where only strict LIFO primitives exist.

## 🔍 Dry Run Trace
**Queue using Stacks Example:**
`push(1), push(2), pop(), push(3), pop()`
- `push(1)`: `inSt = [1]`, `outSt = []`
- `push(2)`: `inSt = [1, 2]`, `outSt = []`
- `pop()`: `outSt` is empty. Transfer `inSt` to `outSt`.
  - `inSt.pop(2)` -> `outSt.push(2)`
  - `inSt.pop(1)` -> `outSt.push(1)`
  - `inSt = []`, `outSt = [2, 1] (top is 1)`
  - Pop `outSt`: returns `1`. `outSt = [2]`.
- `push(3)`: `inSt = [3]`, `outSt = [2]`. (Notice we DON'T transfer!)
- `pop()`: `outSt` is not empty. Directly pop `outSt`. Returns `2`.

## ⚠️ Common Interview Mistakes
1. **Transferring unnecessarily:** The biggest mistake in "Queue using Stacks" is transferring `inSt` to `outSt` on *every* pop/peek, or transferring back and forth. You only ever transfer when `outSt` is strictly empty. If you transfer when it's not empty, you mix up the order of elements (newer elements get buried under older ones in `outSt`).
2. **Missing `peek()` logic:** `peek()` also needs to call `transfer()` because `outSt` might be empty when someone calls `peek()`.

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: What does "Amortized $O(1)$" mean in the context of Queue using Stacks?
While a single `pop()` might trigger a transfer of $N$ elements (taking $O(N)$ time), this transfer only happens rarely. Every element is pushed to `inSt` exactly once, popped from `inSt` exactly once, pushed to `outSt` exactly once, and popped from `outSt` exactly once. Over a sequence of operations, the average cost per element is $O(1)$.

### Q2: How can we implement a Stack using Queues with $O(1)$ push?
If you want $O(1)$ push, the rotation logic must be moved to `pop()`. When `pop()` is called, you dequeue and enqueue $N-1$ elements, leaving the last pushed element at the front to be dequeued and returned. This makes `push` $O(1)$ and `pop` $O(N)$.

### Q3: Why is "Stack using Queues" generally worse than "Queue using Stacks"?
Because "Queue using Stacks" achieves *amortized* $O(1)$ for all operations. "Stack using Queues" always requires $O(N)$ time for either `push` or `pop`. It cannot achieve amortized $O(1)$ because a queue strictly preserves order, forcing us to manually cycle through all elements to invert it.

### Q4: Can you implement a Stack using just ONE queue?
Yes! Use the size of the queue. `push(x)` -> `q.push(x)`. Then loop `for (int i = 0; i < q.size() - 1; i++) { q.push(q.front()); q.pop(); }`. This eliminates the need for two queues.

## 🏆 Related Problems (Leetcode)
- **[232. Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/)**: The exact problem for the two-stack queue.
- **[225. Implement Stack using Queues](https://leetcode.com/problems/implement-stack-using-queues/)**: The queue rotation problem.
- **[155. Min Stack](https://leetcode.com/problems/min-stack/)**: Another custom data structure using stack primitives.

## 🔗 Cross-Topic Connections
- **Amortized Analysis**: This is the canonical example of aggregate method amortized analysis, similar to how dynamic arrays (like `std::vector`) double in size.

## ⚡ 2-Minute Revision Flash Card
- **Queue using 2 Stacks:** `inSt` for push, `outSt` for pop. Transfer `inSt -> outSt` ONLY when `outSt` is empty. Amortized $O(1)$.
- **Stack using 1 Queue:** On `push(x)`, push to queue, then cycle the queue `size-1` times (`push(front)`, `pop()`). $O(N)$ push, $O(1)$ pop.
- **Trap:** Do not transfer elements back to `inSt`. Elements flow one-way: `inSt -> outSt -> out`.
