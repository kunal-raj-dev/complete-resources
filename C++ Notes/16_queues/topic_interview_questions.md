# 💼 Topic 16 Interview Question Bank: Queues & Deques

> **Curated FAANG Interview Bank:** Real-world queue designs, concurrency, streaming duplicates, and buffer management.

---

## 📌 Conceptual & Architectural Questions

### Q1: Why is `std::deque` preferred over `std::vector` when implementing a double-ended queue in C++?
**Answer:** `std::vector` stores elements in a single contiguous memory block; popping or pushing at the front takes $O(N)$ because every single subsequent element must be shifted down. `std::deque` allocates a sequence of fixed-size chunks (arrays) indexed by a central map of chunk pointers. Pushing or popping at *both* the front and back occurs in true $O(1)$ by simply allocating/deallocating chunks when the boundary chunks get full/empty, without shifting existing data.

### Q2: How does a Monotonic Deque achieve $O(N)$ total time for Sliding Window Maximum?
**Answer:** The algorithm uses a nested `while` loop to pop inferior elements. However, time complexity is bounded by the total number of operations, not loop depth. Every element in the array is pushed into the deque exactly once. Therefore, it can only be popped exactly once. The aggregate number of deque operations across all $N$ elements is bounded by $2N$, yielding strict $O(N)$ amortized linear time.

### Q3: When should you use a Queue instead of a Stack?
**Answer:** Use a Queue (FIFO) when processing items in the exact order they arrive:
- **Breadth-First Search (BFS):** Exploring neighbors layer by layer.
- **Fair Scheduling:** Task execution, printer queues, handling web requests.
- **Data Buffering:** Streaming data where older data must be processed first.
Use a Stack (LIFO) for nested, recursive, or dependency-chain logic (DFS, balancing parentheses).

### Q4: How do you design a thread-safe Bounded Blocking Queue in C++?
**Answer:** Use a circular buffer array with a `std::mutex` for thread safety, and two `std::condition_variable` instances: `not_full` and `not_empty`. 
- `push()` acquires the lock, then waits on `not_full` while `size == capacity`. Once it inserts, it signals `not_empty`.
- `pop()` acquires the lock, waits on `not_empty` while `size == 0`. Once it removes, it signals `not_full`.

### Q5: How do you implement a Queue using two Stacks?
**Answer:** Use an `input` stack and an `output` stack.
- **Push:** Always push to `input` ($O(1)$).
- **Pop/Peek:** If `output` is empty, pop all elements from `input` and push them to `output`. This reverses the LIFO order to FIFO. Then pop from `output`. (Amortized $O(1)$).

### Q6: What is a Circular Queue and why is it useful?
**Answer:** A Circular Queue connects the end of a fixed-size array back to the beginning. We maintain `front` and `rear` pointers. When `rear` reaches the end of the array, it wraps around to index 0 using `rear = (rear + 1) % capacity`. It is extremely useful in embedded systems and network buffers because it reuses empty spaces left by dequeued elements without needing to dynamically allocate memory or shift elements.

### Q7: Explain the logic of the "First Unique Character in a Stream" problem.
**Answer:** Maintain a frequency array and a Queue. When a character arrives:
1. Increment its frequency.
2. Push it to the queue.
3. While the queue is not empty AND the character at the front of the queue has a frequency $> 1$, pop the queue! (It's no longer unique).
4. The front of the queue is now guaranteed to be the first unique character.

### Q8: In the Gas Station (Circular Tour) problem, how do you know a solution exists without simulating the full loop?
**Answer:** The Global Feasibility Theorem: If the sum of all gas is $\ge$ the sum of all costs, it is mathematically guaranteed that a valid starting point exists. If this holds, the algorithm just needs to find the *first* station that can successfully reach the end of the array without the tank dropping below zero.

### Q9: Why does the greedy "skip" logic work in the Gas Station problem?
**Answer:** If you start at station $A$ and run out of gas at station $B$, it means the accumulated surplus from $A$ wasn't enough to cross $B$. Any station between $A$ and $B$ (say, $A+1$) would have started with 0 surplus instead of the positive surplus passed down from $A$. Therefore, starting anywhere between $A$ and $B$ will inevitably fail at or before $B$. The next viable candidate to test must be $B+1$.

### Q10: Can you implement a Stack using just ONE Queue?
**Answer:** Yes.
- **Push:** Add the new element to the back of the queue. Then, pop the queue $N-1$ times (where $N$ is the new size) and immediately push those popped elements back into the queue. This rotates the new element to the front of the queue!
- **Pop:** Standard queue pop.
Push is $O(N)$, Pop is $O(1)$.

### Q11: What is a Priority Queue and how is it implemented?
**Answer:** A Priority Queue is a queue where elements are dequeued based on priority (e.g., maximum or minimum value) rather than insertion order. It is typically implemented using a **Heap** (a complete binary tree stored in an array), providing $O(\log N)$ for both insertions and deletions.

### Q12: How do you find the maximum of all subarrays of size K (Sliding Window Maximum) in $O(N \log K)$ without a Deque?
**Answer:** You can use a Max-Heap (Priority Queue). The heap stores pairs of `(value, index)`. As the window slides, push the new `(value, index)`. Then, `while (heap.top().index <= i - k)`, pop the top element (lazy deletion of expired elements). The top is then the max of the current window.

---

## 💻 Debugging & Trace Challenges

### Q13: [Debugging] Why does this Circular Queue `isFull` check fail?
```cpp
bool isFull() {
    return front == (rear + 1) % capacity;
}
```
**Answer:** It depends on how `front` and `rear` are initialized. If both start at `-1` (empty state), `(-1 + 1) % capacity` is `0`, which doesn't equal `-1`, so it doesn't falsely return full. However, when the queue is actually full, `front` could be `0` and `rear` could be `capacity - 1`. `(capacity - 1 + 1) % capacity == 0`. It matches `front`!
*Wait*, the logic `front == (rear + 1) % capacity` is actually CORRECT for a full queue in standard array implementations. The bug usually arises when people don't leave one slot empty to differentiate between Full and Empty, or when they mismanage the `-1` initial state.

### Q14: [Output Prediction] First Non-Repeating Character Stream
Input Stream: `a, a, b, c`
Queue trace:
1. 'a': freq['a']=1. Q=[a]. Front='a'.
2. 'a': freq['a']=2. Q=[a,a]. Front='a' has freq 2 $\to$ Pop. Front='a' has freq 2 $\to$ Pop. Q=[]. Output: `#`.
3. 'b': freq['b']=1. Q=[b]. Front='b'. Output: `b`.
4. 'c': freq['c']=1. Q=[b,c]. Front='b' freq 1. Output: `b`.

### Q15: [Conceptual Bug] In Sliding Window Maximum, what happens if we store values instead of indices in the Deque?
**Answer:** If the deque stores values (e.g., `[5, 3]`), when the window slides, we have NO IDEA if the `5` at the front has fallen out of the window or not! By storing indices, we can strictly evaluate `if (dq.front() <= i - K)` to expire old elements. Values alone lack positional context.
