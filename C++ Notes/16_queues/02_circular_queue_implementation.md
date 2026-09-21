# Lecture 80: Circular Queue Implementation (Ring Buffer)

> **One-Line Purpose:** Prevent array queue memory drift and false overflow by wrapping indices modulo buffer capacity ($i = (i + 1) \pmod C$) in $O(1)$ time and fixed $O(C)$ space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #80  
> **Video ID:** `4mKKolshFD0`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=4mKKolshFD0)  
> **Duration:** 18:37  
> **Status:** AUDITED  

---

## 🔵 The Ring Buffer Formula
- **Enqueue:** `rear = (rear + 1) % capacity`
- **Dequeue:** `front = (front + 1) % capacity`
- **Full Condition:** `(rear + 1) % capacity == front` (or tracking explicit `size == capacity`).
- **Empty Condition:** `size == 0`.

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>

using namespace std;

class MyCircularQueue {
private:
    vector<int> buffer;
    int frontIdx;
    int rearIdx;
    int currentSize;
    int capacity;

public:
    MyCircularQueue(int k) : buffer(k), frontIdx(0), rearIdx(-1), currentSize(0), capacity(k) {}

    bool enQueue(int value) {
        if (isFull()) return false;
        rearIdx = (rearIdx + 1) % capacity;
        buffer[rearIdx] = value;
        currentSize++;
        return true;
    }

    bool deQueue() {
        if (isEmpty()) return false;
        frontIdx = (frontIdx + 1) % capacity;
        currentSize--;
        return true;
    }

    int Front() {
        if (isEmpty()) return -1;
        return buffer[frontIdx];
    }

    int Rear() {
        if (isEmpty()) return -1;
        return buffer[rearIdx];
    }

    bool isEmpty() { return currentSize == 0; }
    bool isFull() { return currentSize == capacity; }
};

int main() {
    MyCircularQueue cq(3);
    cq.enQueue(1);
    cq.enQueue(2);
    cq.enQueue(3);
    cout << "Is full: " << (cq.isFull() ? "YES" : "NO") << endl; // YES
    cq.deQueue();
    cq.enQueue(4);
    cout << "Rear: " << cq.Rear() << endl; // 4
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** Strict $O(1)$ for all operations.
- **Space Complexity:** $\Theta(K)$ statically bounded buffer.

## 🧠 Core Intuition — Why This Works
Imagine a standard array-based queue. Every time you enqueue, `rear` moves right. Every time you dequeue, `front` moves right. Eventually, both pointers hit the end of the array. Even if there are empty slots at the beginning of the array, a naive queue reports "Full" (False Overflow). 
To solve this, imagine taking the linear array and bending it into a circle, connecting the last index to the first index. When `rear` reaches the end, it wraps around to index `0` if it's empty. The mathematical magic to achieve this wrapping in code is the modulo operator `%`.

## 🎯 Pattern Recognition — When to Use This
- **"Fixed size buffer / Sliding Window of fixed size"**: E.g., maintaining the last $K$ events, a router's packet buffer.
- **"Design a custom Queue / Deque"**: If asked to design a queue using an array, you *must* implement a Circular Queue to achieve true $O(1)$ amortized memory footprint, avoiding the need to continuously resize and shift elements like a vector does.

## 🔍 Dry Run Trace
**Example:** `capacity = 3`. Initially: `front = 0, rear = -1, size = 0`. Array `buf = [_, _, _]`.

1. `enQueue(10)`: `size(0) != 3`. `rear = (-1 + 1) % 3 = 0`. `buf[0] = 10`. `size = 1`.
2. `enQueue(20)`: `size(1) != 3`. `rear = (0 + 1) % 3 = 1`. `buf[1] = 20`. `size = 2`.
3. `enQueue(30)`: `size(2) != 3`. `rear = (1 + 1) % 3 = 2`. `buf[2] = 30`. `size = 3`.
4. `enQueue(40)`: `isFull()` is `size(3) == 3`. Returns `false`.
5. `deQueue()`: `isEmpty()` is `false`. `front = (0 + 1) % 3 = 1`. `size = 2`. `buf = [_, 20, 30]`. (10 is logically deleted).
6. `enQueue(40)`: `size(2) != 3`. `rear = (2 + 1) % 3 = 0`. `buf[0] = 40`. `size = 3`. `buf = [40, 20, 30]`. *The wrap-around happened!*

## ⚠️ Common Interview Mistakes
1. **Confusing Full and Empty without a `size` variable:** If you don't keep a `currentSize` integer, the condition for empty (`front == (rear + 1) % C`) becomes dangerously similar to the full condition depending on your pointer initialization. Keeping an explicit `currentSize` completely eliminates this ambiguity.
2. **Modulo on negative numbers:** In C++, `-1 % 3 = -1`, not `2`. So if you initialize `rear = -1`, you must do `rear = (rear + 1) % capacity` (which is `0 % 3 = 0`, safe). But never do `(front - 1) % capacity` without adding capacity first.

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Can we implement this without an explicit `size` variable?
Yes. We can make the array size `capacity + 1` and leave one slot intentionally empty. 
- Empty condition: `front == rear`
- Full condition: `(rear + 1) % arraySize == front`
This trades 1 extra memory slot for the removal of the `currentSize` variable, avoiding maintaining redundant state.

### Q2: How does a Circular Queue differ from C++ `std::queue`?
`std::queue` in C++ is typically backed by a `std::deque`, which allocates chunks of memory dynamically. A circular queue is strictly bounded to a fixed size $K$, allocating memory exactly once. It is much more cache-friendly and deterministic for real-time systems.

### Q3: What happens if we want to allow the Circular Queue to grow?
If the queue is full, we can allocate a new array of $2 \times capacity$. We must copy the elements from the old array to the new one, starting from `front` up to `rear`, and place them at indices `0` to `size-1` in the new array. We then reset `front = 0` and `rear = size - 1`.

### Q4: In an OS context, where is this used?
It is extensively used in Producer-Consumer models (e.g., Ring Buffers in network interface cards), CPU task scheduling (Round Robin), and hardware I/O interrupt buffering.

## 🏆 Related Problems (Leetcode)
- **[622. Design Circular Queue](https://leetcode.com/problems/design-circular-queue/)**: The exact implementation problem.
- **[641. Design Circular Deque](https://leetcode.com/problems/design-circular-deque/)**: Extend this to allow enqueue and dequeue from BOTH sides.
- **[146. LRU Cache](https://leetcode.com/problems/lru-cache/)**: Uses concepts of bounded buffer eviction (though normally uses Doubly Linked List + Map).

## 🔗 Cross-Topic Connections
- **Modulo Arithmetic**: The foundation of wrapping indices safely.
- **Operating Systems**: Bounded Buffer / Producer-Consumer problem uses exactly this data structure wrapped in a Mutex/Semaphore.

## ⚡ 2-Minute Revision Flash Card
- **Why Circular?** Standard array queues suffer from "false overflow" when `front` moves forward but `rear` hits the end.
- **Core Formula:** `index = (index + 1) % capacity`.
- **Implementation State:** Maintain `array`, `front` (index of first item), `rear` (index of last item), `size`, and `capacity`.
- **Full/Empty:** `size == capacity` / `size == 0`.
- **Pro-Tip:** Explicit `size` variable avoids the confusing `(rear + 1) % capacity == front` check and the need for a dummy empty slot.
