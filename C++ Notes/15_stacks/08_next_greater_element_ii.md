# Lecture 75: Next Greater Element II: Circular Array (LeetCode 503)

> **One-Line Purpose:** Find the next greater element in a circular array by virtually concatenating the array to length $2N$ and using index modulo arithmetic $(i \pmod N)$ in $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #75  
> **Video ID:** `If--3pm9K3U`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=If--3pm9K3U)  
> **Duration:** 20:04  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Extend the Monotonic Stack pattern to handle circular arrays.
- Master the "Virtual Concatenation" trick using the modulo `%` operator.
- Understand why exactly $2N - 1$ passes are sufficient for any circular search.
- Differentiate between the backwards-iteration approach and forward-iteration approach for NGE.

---

## 🧠 Core Intuition — Why This Works

If you have a straight array `[1, 2, 1]`, the Next Greater Element (NGE) for the last `1` is `-1` because there's nothing to its right.
But if the array is **circular**, you can wrap around to the beginning! The NGE for the last `1` becomes the `2` in the middle.

How do we simulate wrapping around without messing up our logic? 
**Just append the array to itself!** 
`[1, 2, 1]` becomes `[1, 2, 1, 1, 2, 1]`.
If we run our standard Monotonic Stack NGE algorithm on this double-length array, it perfectly handles the wrap-around. 

Instead of actually copying the array (which takes $O(N)$ extra space), we just let our loop run up to $2N$, and use `index % N` to fetch the elements virtually.

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Circular array" + "Next greater/smaller"**: Immediate trigger for `2N` Monotonic Stack.
- **"Wrap around to the beginning"**: Any array problem allowing wrap-around usually benefits from the `i % N` virtual doubling trick.

---

## 📐 Algorithm Walk-Through

We will use the **Backwards Iteration** approach for NGE. (Iterating right-to-left, answering questions as we go).

1. Initialize `vector<int> nge(n, -1)` and a `stack<int> st` (stores values, not indices).
2. Loop `i` from $2N - 1$ down to $0$:
   - Calculate the virtual index: `int val = nums[i % n]`.
   - **Maintain Monotonicity**: While stack is not empty and `st.top() <= val`, we `st.pop()`. (We want the *strictly greater* element, so we crush anything smaller or equal).
   - **Record Answer**: We only need answers for the *first* $N$ elements. So if `i < n`, we record the NGE:
     - `nge[i] = st.empty() ? -1 : st.top()`.
   - **Push**: `st.push(val)` so it can be the NGE for elements further to the left.
3. Return `nge`.

---

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <stack>
#include <iostream>

using namespace std;

class SolutionNGE2 {
public:
    vector<int> nextGreaterElements(vector<int>& nums) {
        int n = nums.size();
        vector<int> nge(n, -1);
        stack<int> st;

        // Iterate through virtual 2N indices backwards
        for (int i = 2 * n - 1; i >= 0; --i) {
            int val = nums[i % n];

            // Crush anything smaller or equal to current value
            while (!st.empty() && st.top() <= val) {
                st.pop();
            }

            // We only need to record answers for the original array (i < n)
            if (i < n) {
                if (!st.empty()) {
                    nge[i] = st.top();
                }
            }

            // Push current value for elements to the left to use
            st.push(val);
        }

        return nge;
    }
};

int main() {
    SolutionNGE2 solver;
    vector<int> nums = {1, 2, 1};
    auto res = solver.nextGreaterElements(nums);
    
    cout << "Circular NGE: ";
    for (int x : res) cout << x << " "; 
    // Output: 2 -1 2
    cout << endl;
    
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Input:** `nums = [1, 2, 1]`, `N = 3`.
Virtual array: `[1, 2, 1,  1, 2, 1]`
Indices `i`: `0, 1, 2, 3, 4, 5`. Loop backwards from 5 down to 0.

- `i=5 (val=1)`: Stack empty. `i >= 3` (ignore answer). Push `1`. Stack `[1]`.
- `i=4 (val=2)`: `st.top() (1) <= 2`. Pop `1`. Stack empty. `i >= 3` (ignore). Push `2`. Stack `[2]`.
- `i=3 (val=1)`: `st.top() (2) > 1`. `i >= 3` (ignore). Push `1`. Stack `[2, 1]`.
*(Stack is now primed with the first copy of the array for wrap-around!)*

- `i=2 (val=1)`: `st.top() (1) <= 1`. Pop `1`. `st.top()` is now `2`. `i < 3`, so `nge[2] = 2`. Push `1`. Stack `[2, 1]`.
- `i=1 (val=2)`: `st.top() (1) <= 2`. Pop `1`. `st.top() (2) <= 2`. Pop `2`. Stack empty. `nge[1] = -1`. Push `2`. Stack `[2]`.
- `i=0 (val=1)`: `st.top() (2) > 1`. `nge[0] = 2`. Push `1`. Stack `[2, 1]`.

**Final Result:** `nge = [2, -1, 2]`. Correct!

---

## ⚠️ Common Interview Mistakes

1. **Allocating a `2N` Array**: Literally creating `vector<int> doubleNums(nums.begin(), nums.end()); doubleNums.insert(...)` is highly frowned upon by interviewers because it wastes $O(N)$ space and copies memory needlessly. Always use the modulo operator `%`.
2. **Forgetting `i < n` check**: If you assign answers unconditionally `nge[i % n] = st.top()`, you will overwrite the correct answers from the first pass with potentially incorrect/redundant answers from the second pass. Only record answers when processing the original indices (`i < n`).
3. **Strictly Greater vs Greater/Equal**: Standard NGE requires the *strictly greater* element. Your while loop condition must be `st.top() <= val` (with the `=`). If you use `<` only, you'll return a duplicate identical value as the "greater" element, which is wrong.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$. The loop runs $2N$ times. Every element is pushed to the stack exactly once and popped at most once. Amortized time per element is $O(1)$.
- **Space Complexity:** $O(N)$ to store the stack, which can grow to size $N$ in the worst-case (a strictly decreasing array).

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Why loop to exactly $2N - 1$? Why not $3N$?
**Answer:** In a circular array of size $N$, the furthest you can possibly look ahead to find a greater element is $N-1$ steps. If you haven't found it after checking every other element once, it doesn't exist (it must be the absolute maximum element of the array). Therefore, concatenating exactly 1 extra copy ($2N$ total elements) provides a full $N-1$ look-ahead runway for the very last element of the original array.

### Q2: What if we iterated forwards instead of backwards?
**Answer:** Forward iteration is perfectly valid! However, you must store *indices* in the stack rather than *values*. When you find an element larger than the element at the index `st.top()`, you pop it and record the answer for that index. The logic is:
```cpp
for (int i = 0; i < 2 * n; ++i) {
    while (!st.empty() && nums[i % n] > nums[st.top()]) {
        nge[st.top()] = nums[i % n];
        st.pop();
    }
    if (i < n) st.push(i);
}
```

### Q3: What is the maximum element's NGE?
**Answer:** The absolute maximum element in the array will always have an NGE of `-1`. If there are multiple copies of the maximum element, *all* of them will have an NGE of `-1`.

### Q4: Can we optimize the space complexity to $O(1)$?
**Answer:** No, the Monotonic Stack intrinsically requires $O(N)$ auxiliary space to buffer elements whose next greater element has not yet been discovered.

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 496: Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/)** — The foundational, non-circular version using a Hash Map to answer queries for a subset.
2. **[Leetcode 739: Daily Temperatures](https://leetcode.com/problems/daily-temperatures/)** — Standard NGE but asks for the *distance* (difference in indices) rather than the value.
3. **[Leetcode 901: Online Stock Span](https://leetcode.com/problems/online-stock-span/)** — NGE applied to a continuous input stream (Next Greater on the left).

---

## 🔗 Cross-Topic Connections
- **Modulo Arithmetic:** Core to handling any circular buffer/queue or circular array problems.
- **Monotonic Stacks:** The fundamental pattern for all O(N) boundary/greater/smaller queries.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** NGE in a circular array.
- **Trick:** Virtual array of size $2N$ using `i % N`.
- **Direction:** Loop backwards `i = 2N-1` down to `0`.
- **Condition:** `while (!st.empty() && st.top() <= nums[i % n]) st.pop();`
- **Recording Answer:** Only if `i < n`, `nge[i] = st.empty() ? -1 : st.top()`.
- **Push:** `st.push(nums[i % n])`.
- **Time/Space:** $O(N)$ Time | $O(N)$ Space.
