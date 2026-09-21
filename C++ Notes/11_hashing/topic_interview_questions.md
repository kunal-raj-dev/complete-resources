# 💼 Topic 11 Interview Question Bank: Hashing & Prefix Sums

> **Curated FAANG Question Bank:** Hash collisions, prefix equations with negative numbers, and 64-bit integer overflows.

---

## 📌 Conceptual & Architectural Questions

### Q1: Why does Subarray Sum Equals K require Hash Maps instead of Two Pointers / Sliding Window?
- **Answer:** The sliding window technique relies on the monotonicity invariant: expanding the right pointer increases the sum, and shrinking the left pointer decreases the sum. If the array contains negative integers, adding an element can decrease the sum, destroying monotonicity. The prefix sum frequency map equation $\text{prefix}[j] - \text{prefix}[i] = K$ works universally regardless of negative numbers.

---

### Q2: What is Hash Collision and how does `std::unordered_map` handle it?
- **Answer:** A collision occurs when two distinct keys produce the same hash bucket index. `std::unordered_map` resolves collisions using **Separate Chaining** (linked lists / buckets at each index). When load factor exceeds the maximum threshold, it automatically rehashes into a larger bucket array to maintain average $O(1)$ complexity.

---

### Q3: Why does 4-Sum require `long long` casts in C++?
- **Answer:** If 4 array elements are close to $10^9$, their sum $4 \times 10^9$ exceeds `INT_MAX` ($2.14 \times 10^9$). Computing `nums[i] + nums[j] + nums[k] + nums[l]` without casting causes signed integer overflow (Undefined Behavior). Cast to `(long long)nums[i] + ...` to prevent overflow.
