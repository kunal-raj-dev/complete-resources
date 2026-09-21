# 💼 Topic Interview Question Bank — Topic 05: Binary Search

---

### Q1: How do you identify whether a problem can be solved with "Binary Search on Answer"?
**Answer:**
Look for these key indicators:
1. The question asks to **"Minimize the Maximum"** or **"Maximize the Minimum"**.
2. There is a monotonic property in the feasibility of the answer: if answer $X$ is feasible, all answers $> X$ (or $< X$) are guaranteed to be feasible.
3. A greedy verification function (`isValid(X)`) can check whether a candidate value $X$ is valid in $O(N)$ time.

---

### Q2: What is the significance of the `mid ^ 1` trick in Single Element in Sorted Array?
**Answer:**
In a paired array:
- If `mid` is even, `mid ^ 1 = mid + 1`.
- If `mid` is odd, `mid ^ 1 = mid - 1`.
Thus, `nums[mid] == nums[mid ^ 1]` checks if `mid` belongs to a valid pair matching the expected `(even, odd)` order in a single line without branching on parity.

---

### Q3: Why does Aggressive Cows require sorting while Book Allocation does not?
**Answer:**
- In Book Allocation, books must be distributed in **contiguous subarray order** to students as given in the problem statement. Reordering would change subarray partitions.
- In Aggressive Cows, stalls are spatial points in a 1D barn. The cows can occupy any stalls; sorting stall coordinates allows a straightforward single-pass greedy distance check from left to right.
