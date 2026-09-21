# Topic 03 Revision: Arrays & Vectors

> **High-Density Revision Guide:** Core mechanics, memory models, algorithmic patterns, and complexities for Arrays & Vectors.

---

## 1. Array & Vector Foundations
- **Address Formula:** $\text{Address}(arr[i]) = \text{Base} + i \times \text{sizeof(Type)} \implies O(1)$ access.
- **Pointer Decay:** Arrays passed to functions decay to pointers (`int arr[]` $\equiv$ `int* arr`). `sizeof(arr)` yields pointer size (8 bytes).
- **Vector Doubling:** When `size == capacity`, capacity doubles ($1 \to 2 \to 4 \to 8 \dots$). Amortized insertion cost is $O(1)$ per `push_back`.
- **Pre-allocation:** Use `vec.reserve(N)` to prevent multiple heap reallocations.

---

## 2. Core Algorithmic Patterns

### A. Kadane's Algorithm (Max Subarray Sum)
- **Rule:** If running prefix sum `< 0`, reset `currSum = 0`.
- **Trap:** Update `maxSum = max(maxSum, currSum)` *before* resetting `currSum` to handle all-negative arrays correctly.
- **Complexity:** $O(N)$ Time, $O(1)$ Space.

### B. Boyer-Moore's Voting Algorithm (Majority Element $> N/2$)
- **Rule:** Pairwise cancellation. Increment `count` if `num == candidate`; decrement `count` otherwise. Reset candidate when `count == 0`.
- **Complexity:** $O(N)$ Time, $O(1)$ Space.

### C. Buy & Sell Stock I
- **Rule:** Track lowest price seen so far (`bestBuy`). Selling today yields profit `price - bestBuy`.
- **Complexity:** $O(N)$ Time, $O(1)$ Space.

### D. Binary Exponentiation (`Pow(x, n)`)
- **Rule:** If $n$ is odd, `ans *= x`. Always square base `x *= x` and halve power `n >>= 1`.
- **Trap:** Use `long long` for exponent to handle `INT_MIN` negation overflow.
- **Complexity:** $O(\log N)$ Time, $O(1)$ Space.

### E. Container With Most Water
- **Rule:** Two pointers at extremities. Advance the pointer pointing to the shorter vertical line: `h[left] < h[right] ? left++ : right--`.
- **Complexity:** $O(N)$ Time, $O(1)$ Space.

### F. Product of Array Except Self
- **Rule:** Compute prefix products left-to-right into `ans`, then multiply by running suffix scalar right-to-left.
- **Complexity:** $O(N)$ Time, $O(1)$ Auxiliary Space (No division used).

---

## 3. Complexity Quick Reference

| Algorithm | Best Time | Average / Worst Time | Auxiliary Space |
|---|---|---|---|
| Linear Search | $O(1)$ | $O(N)$ | $O(1)$ |
| Two-Pointer Reversal | $O(N)$ | $O(N)$ | $O(1)$ |
| Pair Sum (Sorted) | $O(1)$ | $O(N)$ | $O(1)$ |
| Kadane's Algorithm | $O(N)$ | $O(N)$ | $O(1)$ |
| Boyer-Moore Voting | $O(N)$ | $O(N)$ | $O(1)$ |
| Binary Exponentiation | $O(1)$ | $O(\log N)$ | $O(1)$ |
| Container With Most Water | $O(N)$ | $O(N)$ | $O(1)$ |
| Product Except Self | $O(N)$ | $O(N)$ | $O(1)$ |
