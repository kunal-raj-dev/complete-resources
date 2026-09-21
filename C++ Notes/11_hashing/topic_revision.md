# ⚡ Rapid Revision — Topic 11: Hashing & Prefix Sums

> **Target:** 5-minute pre-interview refresher on hashing patterns and prefix sum equations.

---

## 🔑 Key Problem Patterns
- **Subarray Sum = K:** `target = curr_sum - K`. Store prefix sum frequencies. Always initialize `mp[0] = 1`.
- **3-Sum:** Sort array. Loop $i$, two pointers $j$ and $k$. Skip `nums[i] == nums[i-1]`.
- **4-Sum:** Nested loops $i, j$ + two pointers. Cast to `long long` before adding 4 values.
- **Find Duplicate ($O(1)$ space):** Array is a linked list (`next = nums[curr]`). Use Floyd's cycle detection.
