# ⚡ Topic 16 Revision: Queues & Deques

> **High-Density Review:** Queue mechanics, Circular ring buffers, Monotonic deques, and greedy stream processing patterns.

---

## 1. 🎯 Queue Data Structure Summary

| Architecture | Implementation | Time (Push/Pop) | Space | Key Feature / Gotcha |
|---|---|---|---|---|
| **Linked List Queue** | Head/Tail Node pointers | $O(1) / O(1)$ | $O(N)$ | Heap allocations per push overhead |
| **Circular Array** | `(rear + 1) % Cap` | $O(1) / O(1)$ | $O(K)$ | Zero memory drift; fixed static size |
| **Two-Stack Queue** | `inSt` & `outSt` | $O(1) / O(1)$ amortized | $O(N)$ | Massive $O(N)$ pop when `outSt` is empty |
| **Monotonic Deque** | `std::deque` | $O(1)$ amortized | $O(K)$ | Evicts smaller back elements |

---

## 2. 🧠 Core Queue Code Patterns

### 1. The Sliding Window Maximum (Monotonic Deque)
Maintains a strictly decreasing deque of **indices**.
```cpp
// 1. Evict stale out-of-bound elements from the front
if (!dq.empty() && dq.front() <= i - k) dq.pop_front();

// 2. Maintain Monotonic Decreasing Order (Evict weak from back)
while (!dq.empty() && nums[dq.back()] <= nums[i]) dq.pop_back();

// 3. Push and Read
dq.push_back(i);
if (i >= k - 1) res.push_back(nums[dq.front()]);
```

### 2. First Unique Character Stream (Queue + Frequency Map)
Filters out dead/non-unique elements lazily.
```cpp
freq[char]++;
q.push(char);

// Lazily pop characters that have become redundant
while (!q.empty() && freq[q.front()] > 1) {
    q.pop();
}

char firstUnique = q.empty() ? '#' : q.front();
```

### 3. Circular Ring Buffer Push
Using modulo arithmetic to wrap around.
```cpp
if (isFull()) return false;
rear = (rear + 1) % capacity;
arr[rear] = val;
```

---

## 3. 📐 Problem Summary Matrix

| Problem | Queue/Pattern | Time | Space | Core Invariant |
|---|---|---|---|---|
| **Queue using Stacks** | 2 Stacks (`in`, `out`) | Amortized $O(1)$ | $O(N)$ | Transfer `in` to `out` ONLY when `out` is empty |
| **Stack using Queues** | 1 Queue | Push $O(N)$ | $O(N)$ | Push front, then pop & push back $N-1$ times |
| **First Unique Char** | Queue + Hash Map | $O(N)$ total | $O(1)$ | Lazy pop queue front if `freq > 1` |
| **Sliding Window Max** | Monotonic Deque | $O(N)$ | $O(K)$ | Evict expired front, evict weaker back |
| **Gas Station** | Greedy Array Pass | $O(N)$ | $O(1)$ | If tank $< 0$, skip candidate to `i+1` |

---

## 4. ⚠️ 3 Fatal Traps to Avoid

1. **Sliding Window Value Storage:** Storing actual `nums[i]` values in the deque instead of `i` indices. You MUST store indices to know when an element has fallen out of the `[i-K+1, i]` window.
2. **Transferring Stacks Every Push:** When building a Queue using Two Stacks, do NOT pour `output` back into `input` after every operation. Keep them in `output`. Only pour `input` to `output` when `output` is completely empty. This ensures Amortized $O(1)$ instead of strict $O(N)$.
3. **Array Wraparound Simulation:** In Circular Tour/Gas Station, don't literally simulate driving in a circle using `i % N` nested loops. Use the global `total_gas >= total_cost` mathematical guarantee to prove a single pass is enough.

---

## 5. 🔥 Interview Q&A — Google / Amazon Level

### Q1: Why is Monotonic Deque strictly $O(N)$ for Sliding Window Maximum, even with the nested `while` loop?
Although there is a `while` loop inside the `for` loop, look at the absolute operations per element. Every index `i` is pushed into the deque exactly once. It is also popped from the deque at most once (either from the front when it expires, or from the back when it's outclassed). Since an element cannot be popped more than once, the inner `while` loop runs at most $N$ times *globally* across all iterations. $O(N + N) = O(N)$.

### Q2: What's the main disadvantage of a Linked List Queue compared to a Circular Array Queue?
Memory allocation overhead. A Circular Array Queue is allocated once in a single contiguous block of memory. A Linked List Queue calls `new` for every single `enqueue()` operation and `delete` for every `dequeue()`, resulting in severe heap fragmentation and cache misses due to poor spatial locality.

### Q3: When is "Queue using Stacks" practically useful?
In purely functional programming languages (like Haskell or Erlang) where data structures are immutable, strict queues are inefficient to implement directly. Stacks (Lists) are the primary primitive. Emulating a queue with two stacks provides the optimal amortized time complexity in immutable environments.

### Q4: For First Unique Character in a Stream, could we use a Doubly Linked List (DLL)?
Yes. A DLL coupled with a Hash Map of pointers allows for $O(1)$ *eager* deletion (removing the character from the stream exactly when the second occurrence arrives). The Queue approach uses *lazy* deletion (waiting until the duplicated character reaches the front). DLL + Map uses more memory (node pointers) but keeps the active set size strictly bounded to non-repeated elements.

## 6. ⚡ 2-Minute Revision Flash Card

- **Queue vs Deque:** Queue = FIFO (push back, pop front). Deque = Double Ended (push/pop from both sides).
- **Circular Queue Trick:** `idx = (idx + 1) % capacity`.
- **Sliding Window Max:** Use Deque. Store indices. Front is always max. Evict smaller elements from back. Evict expired elements from front.
- **Queue with Stacks:** `InputStack` takes pushes. `OutputStack` gives pops. Transfer `In` to `Out` ONLY when `Out` is empty.
- **Gas Station (Greedy):** If `total_gas < total_cost`, return `-1`. Else, if `current_gas < 0`, start over at `i+1`.
