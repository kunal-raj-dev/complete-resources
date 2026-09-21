# Lecture 15: Product of Array Except Self (LeetCode 238)

> **One-Line Purpose:** Master the Prefix & Suffix Product decomposition technique to compute cumulative directional states without using the division operator, achieving strict $O(N)$ time and $O(1)$ auxiliary space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #15  
> **Video ID:** `TW2m8m_FNJE`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=TW2m8m_FNJE)  
> **Duration:** 29:30  
> **Transcript:** `.transcripts/03_arrays_and_vectors/015_Product_of_Array_Except_Self___Brute_to_Optimal_Solution___Leetcode_238.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The exact requirements and constraints of LeetCode 238.
- Why the **explicit ban on the division operator (`/`)** prevents trivial solutions and requires algorithmic innovation.
- How prefix products and suffix products decompose the product of all elements excluding index $i$.
- **Approach 1 (Prefix + Suffix Arrays):** $O(N)$ Time, $O(N)$ Auxiliary Space.
- **Approach 2 (In-Place Output Array Accumulation):** $O(N)$ Time, **$O(1)$ Auxiliary Space**.
- How this prefix-suffix decomposition pattern naturally handles single and multiple zeros without brittle edge-case branching.
- Real-world interview follow-ups, parallelization models, and integer overflow considerations.

---

## 🔵 Lecture Context

Product of Array Except Self is a Tier-1 interview problem asked frequently at Google, Amazon, Meta, and Microsoft. It evaluates an engineer's ability to precompute directional cumulative states (prefix and suffix scans). Mastering this decomposition technique is crucial because the same bidirectional accumulation pattern reappears in Trapping Rainwater (Lecture 74), 2D Range Queries, and dynamic programming state transitions.

---

## 1. Problem Statement & The Division Ban

**Problem:** Given an integer array `nums` of size $n$, return an array `ans` such that `ans[i]` is equal to the product of all the elements of `nums` except `nums[i]`.

**Constraints:**
1. You must write an algorithm that runs in $O(N)$ time.
2. You **cannot** use the division operator (`/`).

> 🧠 **Brain Trigger**
> 
> If division were allowed, how would you solve it, and what catastrophic bug would you encounter?
> 
> **Answer:** If division were allowed, you could compute the total product of the array $P = \prod_{k=0}^{n-1} \text{nums}[k]$, and then set $\text{ans}[i] = P / \text{nums}[i]$ for each index.
> 
> However, if `nums` contains:
> - **A single `0`:** $P$ becomes `0`. When evaluating $\text{ans}[i]$ for non-zero elements, `0 / nums[i] = 0`. But at the index where $\text{nums}[i] = 0$, evaluating $0 / 0$ triggers a **ZeroDivisionError / Floating Point Exception crash**!
> - **Two or more `0`s:** Every element in `ans` must be `0`.
> 
> The division ban forces an elegant bidirectional accumulation that eliminates zero-division exceptions entirely.

---

## 2. Mathematical Decomposition: Prefix $\times$ Suffix

For any element at index $i$, the product of all elements except $\text{nums}[i]$ can be factored into two disjoint contiguous ranges:
1. All elements strictly to the left of index $i$: $\text{nums}[0 \dots i-1]$
2. All elements strictly to the right of index $i$: $\text{nums}[i+1 \dots n-1]$

$$\text{ans}[i] = \underbrace{\left(\prod_{j=0}^{i-1} \text{nums}[j]\right)}_{\text{Prefix Product}} \times \underbrace{\left(\prod_{j=i+1}^{n-1} \text{nums}[j]\right)}_{\text{Suffix Product}}$$

```
Array:      [   1   |   2   |   3   |   4   ]
Index:          0       1       2       3

For index 2 (value 3):
- Left Range:   [1, 2] -> Prefix Product = 1 * 2 = 2
- Right Range:  [4]    -> Suffix Product = 4
- Result:       ans[2] = 2 * 4 = 8
```

---

## 3. Progressive Implementations

### Approach 1: Explicit Prefix & Suffix Arrays ($O(N)$ Space)

```cpp
#include <vector>
#include <iostream>
using namespace std;

vector<int> productExceptSelfWithArrays(const vector<int>& nums) {
    int n = nums.size();
    vector<int> prefix(n, 1);
    vector<int> suffix(n, 1);
    vector<int> ans(n);

    // 1. Build Prefix Array: prefix[i] stores product of nums[0 ... i-1]
    for (int i = 1; i < n; i++) {
        prefix[i] = prefix[i - 1] * nums[i - 1];
    }

    // 2. Build Suffix Array: suffix[i] stores product of nums[i+1 ... n-1]
    for (int i = n - 2; i >= 0; i--) {
        suffix[i] = suffix[i + 1] * nums[i + 1];
    }

    // 3. Combine: ans[i] = prefix[i] * suffix[i]
    for (int i = 0; i < n; i++) {
        ans[i] = prefix[i] * suffix[i];
    }

    return ans;
}
```

- **Time Complexity:** $O(N)$ (Three sequential linear passes).
- **Space Complexity:** $O(N)$ auxiliary space (allocates two temporary vectors `prefix` and `suffix`).

---

### Approach 2: In-Place Output Accumulation ($O(1)$ Auxiliary Space)

> 💡 **The Optimization:**
> 1. We don't need a separate `prefix` array—we can compute the prefix products directly into the return vector `ans`.
> 2. We don't need an entire `suffix` array—we can maintain a single running scalar variable `suffix = 1` while traversing backwards from index $n-1$ to $0$.

```cpp
#include <vector>
#include <iostream>
using namespace std;

vector<int> productExceptSelf(const vector<int>& nums) {
    int n = nums.size();
    vector<int> ans(n, 1);

    // Pass 1: Accumulate Prefix Products directly into ans
    // ans[i] will contain product of all elements strictly to the left of i
    for (int i = 1; i < n; i++) {
        ans[i] = ans[i - 1] * nums[i - 1];
    }

    // Pass 2: Accumulate Suffix Products on-the-fly using a single scalar
    int suffix = 1;
    for (int i = n - 1; i >= 0; i--) {
        ans[i] = ans[i] * suffix;
        suffix *= nums[i]; // Update suffix accumulator for next element to the left
    }

    return ans;
}

int main() {
    vector<int> nums = {1, 2, 3, 4};
    vector<int> res = productExceptSelf(nums);

    for (int val : res) {
        cout << val << " "; // Output: 24 12 8 6
    }
    cout << "\n";
    return 0;
}
```

- **Time Complexity:** $O(N)$ (Two sequential linear passes).
- **Space Complexity:** $O(1)$ auxiliary space (The problem specification explicitly notes that the returned output array does not count toward auxiliary space complexity).

---

## 🔍 Detailed Trace

Input: `nums = [1, 2, 3, 4]`

### Forward Pass (Prefix Accumulation):
- `ans[0] = 1` (Identity value: no elements to the left of index 0)
- `i = 1`: `ans[1] = ans[0] * nums[0] = 1 * 1 = 1`
- `i = 2`: `ans[2] = ans[1] * nums[1] = 1 * 2 = 2`
- `i = 3`: `ans[3] = ans[2] * nums[2] = 2 * 3 = 6`
- State of `ans` after Pass 1: `[1, 1, 2, 6]`

### Backward Pass (Suffix Multiplication):
Initial `suffix = 1`:
- `i = 3`: `ans[3] = ans[3] * suffix = 6 * 1 = 6`. Update: `suffix = 1 * nums[3] = 4`.
- `i = 2`: `ans[2] = ans[2] * suffix = 2 * 4 = 8`. Update: `suffix = 4 * nums[2] = 12`.
- `i = 1`: `ans[1] = ans[1] * suffix = 1 * 12 = 12`. Update: `suffix = 12 * nums[1] = 24`.
- `i = 0`: `ans[0] = ans[0] * suffix = 1 * 24 = 24`. Update: `suffix = 24 * nums[0] = 24`.

**Final `ans`:** `[24, 12, 8, 6]` (Matches $24, 12, 8, 6$).

---

## 🧠 Mental Model

Think of this problem as two light beams shining across the array from opposite directions:
```
Left-to-Right Beam (Prefix):
   [1] --------> [1*2] --------> [1*2*3] --------> [1*2*3*4]
   Accumulates products of all elements seen so far from the left.

Right-to-Left Beam (Suffix):
   [1*2*3*4] <-------- [2*3*4] <-------- [3*4] <-------- [4]
   Accumulates products of all elements seen so far from the right.

At each cell i:
   Result = (Left Beam Value before cell i) * (Right Beam Value after cell i)
```

---

## ⚠️ Common Mistakes

1. **Incorrect Prefix Indexing:** Writing `ans[i] = ans[i-1] * nums[i]` includes the current element in its own prefix product! The prefix for index $i$ must only include elements strictly before $i$, i.e., `nums[i-1]`.
2. **Suffix Update Ordering:** Updating `suffix *= nums[i]` *before* multiplying into `ans[i]`. This mistakenly includes `nums[i]` into the suffix product of index $i$. You must multiply `ans[i] *= suffix` *first*, and *then* update `suffix *= nums[i]`.
3. **Integer Overflow Assumption:** On LeetCode, intermediate products are guaranteed to fit in a signed 32-bit `int`. However, in real-world systems, multiplying $10^5$ elements easily overflows $2^{31}-1$. If numbers can be large, use `long long` or modulo arithmetic.

---

## 🖥️ System-Specific Notes

- **32-bit vs 64-bit Integer Limits:** In C++, signed 32-bit `int` overflows at $2^{31}-1 \approx 2.14 \times 10^9$. If the problem statement states that elements can be up to $30$ and array length is up to $10^5$, products will exceed $2^{64}-1$. In production environments, arbitrary-precision libraries (or logarithmic summation: $\prod x_i = \exp(\sum \ln x_i)$) are used.
- **Cache Locality:** Pass 1 runs forward through memory (sequential cache line prefetching). Pass 2 runs backward. Modern CPU hardware prefetchers easily handle both forward and reverse linear strides.

---

## 🟡 Additional Essential Context

The prefix-suffix decomposition technique is a general algorithmic paradigm:
- **Prefix Sum + Suffix Sum:** Used in Equilibrium Index and Subarray Sum queries.
- **Prefix Max + Suffix Max:** The foundational building block for LeetCode 42 (Trapping Rainwater).
- **Prefix GCD + Suffix GCD:** Used to find the maximum GCD after removing one element.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why do we initialize `ans[0] = 1` and `suffix = 1`?  
**A:** `1` is the identity element of multiplication ($x \times 1 = x$). There are zero elements to the left of index 0, so the empty prefix product is mathematically defined as $1$.

**Q2:** Does returning `vector<int> ans` violate the $O(1)$ auxiliary space constraint?  
**A:** No. By convention across technical interviews (including LeetCode and FAANG rubrics), memory allocated solely to return the required output does not count toward *auxiliary* space complexity.

---

### 🔥 Interview Questions

#### Q1: How does this algorithm handle an array containing multiple zeros, e.g., `[0, 1, 2, 0]`?
- **Short Answer:** It handles multiple zeros naturally without any special conditional branches, producing `[0, 0, 0, 0]`.
- **Detailed Explanation:** For any element at index $i$, both zeros cannot be excluded simultaneously unless there is only one zero. With two or more zeros, every single index will have at least one zero in its left prefix or its right suffix. Thus, every product evaluates to $0 \times \text{anything} = 0$.
- **Why Interviewers Ask:** Tests whether your code relies on fragile special-case branching (`if (zero_count > 1)`) or relies on robust mathematical invariants.

#### Q2: Can this algorithm be parallelized on a multi-core CPU or GPU?
- **Short Answer:** Yes, using the Parallel Prefix Scan (Blelloch Algorithm).
- **Detailed Explanation:** Prefix and suffix computations are associative operations: $(a \times b) \times c = a \times (b \times c)$. Using an up-sweep (tree reduction) followed by a down-sweep on an array of size $N$, parallel prefix products can be computed in $O(\log N)$ parallel time on $O(N)$ processor cores.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> nums = {-1, 1, 0, -3, 3};
    int n = nums.size();
    vector<int> ans(n, 1);

    for (int i = 1; i < n; i++) ans[i] = ans[i - 1] * nums[i - 1];
    int suffix = 1;
    for (int i = n - 1; i >= 0; i--) {
        ans[i] *= suffix;
        suffix *= nums[i];
    }

    for (int x : ans) cout << x << " ";
    cout << "\n";
    return 0;
}
```
**Output:** `0 0 9 0 0`  
**Explanation:** Index 2 contains `0`.
- For index 2: Prefix product = $(-1) \times 1 = -1$. Suffix product = $(-3) \times 3 = -9$. Result = $(-1) \times (-9) = 9$.
- For all other indices: Their prefix or suffix spans include the `0` at index 2, making their product `0`.

---

### 🐛 Debugging Challenge
Find the fatal bug in this implementation:
```cpp
vector<int> buggyProductExceptSelf(const vector<int>& nums) {
    int n = nums.size();
    vector<int> ans(n, 1);
    
    for (int i = 1; i < n; i++) {
        ans[i] = ans[i - 1] * nums[i - 1];
    }
    
    int suffix = 1;
    for (int i = n - 1; i >= 0; i--) {
        suffix *= nums[i]; // <-- BUG!
        ans[i] *= suffix;
    }
    return ans;
}
```
**Why it fails:** Line `suffix *= nums[i]` is executed *before* multiplying into `ans[i]`. This causes `ans[i]` to be multiplied by `nums[i]`, calculating the product of *all* elements *including* `nums[i]` instead of *except* `nums[i]`.  
**Correction:** Multiply `ans[i] *= suffix;` first, and *then* update `suffix *= nums[i];`.

---

## Edge Cases

1. **Minimum Array Size ($N = 2$):** `nums = [2, 3]` $\to$ `ans = [3, 2]`. Handled correctly.
2. **Single Zero:** `nums = [1, 0]` $\to$ `ans = [0, 1]`. Handled correctly without division-by-zero crashes.
3. **Multiple Zeros:** `nums = [0, 0, 2]` $\to$ `ans = [0, 0, 0]`. Correct.
4. **All Ones:** `nums = [1, 1, 1]` $\to$ `ans = [1, 1, 1]`. Correct.
5. **Negative Numbers:** Handles sign cancellations correctly (e.g. two negative numbers yield a positive product).

---

## Complexity Analysis

| Approach | Time Complexity | Auxiliary Space Complexity | Description |
|---|---|---|---|
| Brute Force | $O(N^2)$ | $O(1)$ | Nested loops multiplying all $j \neq i$. |
| Division Approach | $O(N)$ | $O(1)$ | Crashes on 0, violates interview constraints. |
| Prefix + Suffix Arrays | $O(N)$ | $O(N)$ | Three passes, allocates two extra $O(N)$ arrays. |
| **Optimal In-Place Accumulation** | **$O(N)$** | **$O(1)$** | **Two passes, reuses output vector + single scalar.** |

---

## Key Takeaways

1. **Decomposition:** `result[i] = prefix[i-1] * suffix[i+1]`.
2. **Division Avoidance:** Zeroes are handled naturally without special-case branching or risk of divide-by-zero crashes.
3. **Space Optimization:** Accumulate the prefix scan directly into the output vector, then sweep backward with a running scalar `suffix` variable to achieve $O(1)$ auxiliary memory.

---

## ⚡ 2-Minute Revision

```cpp
vector<int> productExceptSelf(const vector<int>& nums) {
    int n = nums.size();
    vector<int> ans(n, 1);
    for (int i = 1; i < n; i++) ans[i] = ans[i - 1] * nums[i - 1];
    int suffix = 1;
    for (int i = n - 1; i >= 0; i--) {
        ans[i] *= suffix;
        suffix *= nums[i];
    }
    return ans;
}
```
- **Forward pass:** Computes prefix product strictly before $i$.
- **Backward pass:** Multiplies running suffix product strictly after $i$.
- **Time:** $O(N)$ | **Auxiliary Space:** $O(1)$.
