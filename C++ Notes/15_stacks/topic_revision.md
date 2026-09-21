# ⚡ Topic 15 Revision: Stacks & Monotonic Invariants

> **High-Density Review:** Stack LIFO principles, Monotonic stack templates, boundary calculation patterns, and algorithm matrix.

---

## 1. 🎯 Monotonic Stack Cheat Sheet

The direction of your `while` loop dictates the behavior:
- `st.top() <= target`: Finds the **Strictly Greater** element.
- `st.top() >= target`: Finds the **Strictly Smaller** element.

### Next Greater Element (Scan R $\to$ L)
Builds a **decreasing** stack.
```cpp
for (int i = n - 1; i >= 0; --i) {
    while (!st.empty() && st.top() <= nums[i]) st.pop();
    nge[i] = st.empty() ? -1 : st.top();
    st.push(nums[i]);
}
```

### Previous Smaller Element (Scan L $\to$ R)
Builds an **increasing** stack.
```cpp
for (int i = 0; i < n; ++i) {
    while (!st.empty() && st.top() >= nums[i]) st.pop();
    pse[i] = st.empty() ? -1 : st.top();
    st.push(nums[i]);
}
```

---

## 2. 🧠 Universal Patterns & Invariants

### The "Push Expected Match" Trick (Valid Parentheses)
Instead of pushing opening brackets and checking closing ones with massive `if-else` chains:
```cpp
if (c == '(') st.push(')');
else if (c == '{') st.push('}');
else if (st.empty() || st.top() != c) return false;
else st.pop();
```

### The $O(1)$ Space Min-Stack Encoder
```cpp
// Push:
long long encoded = 2LL * val - minVal; 
// Pop recovery:
minVal = 2LL * minVal - popped_encoded_val;
```

### The Circular Array (NGE II) Trick
Double the bounds virtually, no extra memory needed:
```cpp
for (int i = 2 * n - 1; i >= 0; --i) {
    int val = nums[i % n];
    // ...
```

---

## 3. 📐 Problem Summary Matrix

| Problem | Stack Type / Alg | Time | Space | Core Invariant |
|---|---|---|---|---|
| **Valid Parentheses** | Char Stack | $O(N)$ | $O(N)$ | LIFO matching of bracket pairs |
| **Min Stack** | Encoded Stack | $O(1)$ | $O(1)$ aux | $2x - \text{minVal}$ flag encoding |
| **Next Greater (NGE)**| Monotonic Decr | $O(N)$ | $O(N)$ | Right-to-Left backward scan |
| **Circular NGE II** | Monotonic Decr | $O(N)$ | $O(N)$ | $2N$ iterations + `modulo N` trick |
| **Stock Span** | Monotonic Decr | $O(N)$ | $O(N)$ | Store *indices*. Span = `i - st.top()` |
| **Largest Rectangle** | Monotonic Incr | $O(N)$ | $O(N)$ | Width = `i - st.top() - 1`. Dummy 0 at end |
| **Trapping Water** | Two Pointers | $O(N)$ | $O(1)$ | Shorter pointer dictates bottleneck |
| **Celebrity Problem**| Two Pointers | $O(N)$ | $O(1)$ | `knows(A, B)` eliminates exactly one person |

---

## 4. ⚠️ 3 Fatal Traps to Avoid

1. **Calling `.top()` on an Empty Stack:** This is the #1 cause of Segmentation Faults in stack problems. ALWAYS put `!st.empty()` first in your `while` conditions.
2. **Not Flushing the Monotonic Stack:** In Area/Rectangle problems, if you don't push a final dummy value (like a `0` height) at the end, any elements left in the stack will never calculate their final area.
3. **Using $<=$ vs $<$ in Monotonic Pops:** If the question asks for the "Next Greater Element", you MUST pop elements that are equal (`<=`). If you only pop `<`, you will falsely claim that `5` is the next greater element for another `5`.
