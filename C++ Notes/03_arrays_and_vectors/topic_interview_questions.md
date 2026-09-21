# Topic 03 Interview Questions: Arrays & Vectors

> **Curated Question Bank:** FAANG interview questions, edge-case traps, and algorithmic puzzles across Arrays & Vectors.

---

## 📌 Problem-Solving & Implementation Questions

### Q1: [LeetCode 53] Can Kadane's algorithm handle a circular array where subarrays can wrap around the end?
- **Short Answer:** Yes! LeetCode 918 (Maximum Sum Circular Subarray).
- **Detailed Explanation:** In a circular array, the maximum sum subarray is either:
  1. A standard non-wrapping subarray (found directly via standard Kadane).
  2. A wrapping subarray (wrapping around the ends), which is mathematically equal to:
     $$\text{Total Array Sum} - \text{Minimum Subarray Sum}$$
  We run Kadane's algorithm once for maximum subarray sum, once for minimum subarray sum, and take $\max(\text{maxSum}, \text{totalSum} - \text{minSum})$.
- **Critical Edge Case:** If all elements are negative, `totalSum == minSum`, which makes `totalSum - minSum == 0` (an empty subarray). In that case, return `maxSum`.

---

### Q2: [LeetCode 11] Why is it incorrect to move BOTH pointers simultaneously in Container With Most Water when `height[left] == height[right]`?
- **Short Answer:** It is safe to move either pointer (e.g. `right--`), but moving both simultaneously could skip a state if the next inner elements are tall enough to form a wider sub-container. In practice, moving either one is sufficient because any container using either of the tied lines with an inner line will have equal or less height and strictly less width.

---

### Q3: [Memory & Internals] Why does `vector<bool>` behave differently from all other standard vector specializations?
- **Short Answer:** `vector<bool>` is a space-optimized proxy specialization that packs 8 boolean values into a single byte (1 bit per bool).
- **Detailed Explanation:** Because CPU architectures cannot take the memory address of an individual bit, `vector<bool>::operator[]` does not return a `bool&`. Instead, it returns a temporary proxy object (`std::vector<bool>::reference`).
- **Interview Trap:** You cannot bind `auto &x = vec_bool[0];` because non-const lvalue references cannot bind to temporary proxy objects!

---

### Q4: [LeetCode 238] If the input array contains two or more zeros, what is the output of Product of Array Except Self?
- **Short Answer:** An array consisting exclusively of zeroes (`[0, 0, \dots, 0]`).
- **Explanation:** If there are $\ge 2$ zeroes, for any index $i$, the remaining elements will always contain at least one of the other zeroes, making every product $0$. The prefix-suffix product algorithm naturally handles this without any special branching.

---

### Q5: [Complexity Deduction] Given an array constraint of $N = 2 \times 10^5$, can a solution with $O(N^2)$ pass within a 1.0s time limit?
- **Short Answer:** Absolutely not. It will fail with Time Limit Exceeded (TLE).
- **Mathematical Justification:**
  $$(2 \times 10^5)^2 = 4 \times 10^{10} \text{ operations}$$
  Standard CPUs execute $\approx 10^8$ operations per second. A run requiring $4 \times 10^{10}$ operations will take $\approx 400$ seconds. To pass within 1.0s, the algorithm must run in $O(N)$ or $O(N \log N)$ time ($2 \times 10^5 \log_2(2 \times 10^5) \approx 3.6 \times 10^6$ operations $\ll 10^8$).
