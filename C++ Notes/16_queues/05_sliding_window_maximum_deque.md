# Lecture 83: Sliding Window Maximum: Monotonic Deque (LeetCode 239)

> **One-Line Purpose:** Find the maximum element in every sliding window of size $K$ in optimal strictly $O(N)$ time using a Monotonic Decreasing Deque storing array indices.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #83  
> **Video ID:** `XwG5cozqfaM`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=XwG5cozqfaM)  
> **Duration:** 31:22  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Extend the Monotonic Stack pattern to a **Monotonic Deque** (Double-Ended Queue).
- Understand why a normal Queue or Stack fails for sliding windows.
- Master the "Age vs Utility" eviction policy for the deque.
- Handle indices effectively to enforce window boundaries.

---

## 🧠 Core Intuition — Why This Works

If you have a window of size $K$, you need to quickly find its maximum.
- A brute force loop takes $O(N \times K)$. 
- A Max-Heap (Priority Queue) takes $O(N \log K)$.
Can we do $O(N)$? Yes!

Imagine a line of candidates waiting for a job. The job only looks at the $K$ most recent people.
If person $A$ is older (arrived earlier) than person $B$, and person $A$ is also WEAKER (smaller number) than person $B$... person $A$ is completely useless! They will *never* be the maximum in any current or future window because $B$ is both stronger and will stick around longer. So we can just kick $A$ out of the line entirely.

**The Monotonic Deque Strategy:**
1. **Evict the Weak:** Before adding a new number, pop from the *back* of the deque all numbers that are smaller than it.
2. **Evict the Expired:** Check the front of the deque. If the index is too old (outside the current window $[i - K + 1, i]$), pop from the *front*.
3. **The Result:** The deque remains strictly decreasing. The strongest, valid number is always sitting right at the front!

*Why a Deque?* Because we need to pop weak elements from the back, AND pop expired elements from the front. A stack/queue only lets us modify one end.

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Sliding Window Maximum / Minimum"**: Absolute classic direct match.
- **"Max/Min element in a moving range"**: E.g., Jumping games where you can jump $1$ to $K$ steps and want to maximize score.
- **Dynamic Programming with a range constraint**: $dp[i] = \max(dp[i-K \dots i-1]) + cost[i]$.

---

## 📐 Algorithm Walk-Through

1. Initialize `deque<int> dq` (to store indices, NOT values) and `vector<int> result`.
2. Loop `i` from $0$ to $N-1$:
   - **Step 1 (Cleanup expired):** If `!dq.empty()` and `dq.front() <= i - K`, then `dq.pop_front()`.
   - **Step 2 (Cleanup weak):** While `!dq.empty()` and `nums[dq.back()] <= nums[i]`, then `dq.pop_back()`.
   - **Step 3 (Push):** `dq.push_back(i)`.
   - **Step 4 (Record):** If `i >= K - 1` (meaning we have finally processed at least $K$ elements to form our first full window), `result.push_back(nums[dq.front()])`.
3. Return `result`.

---

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <deque>
#include <iostream>

using namespace std;

class SolutionSlidingWindowMax {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        deque<int> dq; // Stores INDICES, not the actual values
        vector<int> result;

        for (int i = 0; i < (int)nums.size(); ++i) {
            // 1. Remove indices that are outside the current window bounds
            // Window is [i - k + 1, i]. If front is <= i - k, it's expired.
            if (!dq.empty() && dq.front() <= i - k) {
                dq.pop_front();
            }

            // 2. Remove smaller elements from the back
            // They are useless because the current element is larger and newer
            while (!dq.empty() && nums[dq.back()] <= nums[i]) {
                dq.pop_back();
            }

            // 3. Insert current index
            dq.push_back(i);

            // 4. Record result once the first window of size k is formed
            if (i >= k - 1) {
                result.push_back(nums[dq.front()]);
            }
        }

        return result;
    }
};

int main() {
    SolutionSlidingWindowMax solver;
    // Classic LeetCode example
    vector<int> nums = {1, 3, -1, -3, 5, 3, 6, 7};
    vector<int> res = solver.maxSlidingWindow(nums, 3);
    
    cout << "Sliding Window Max: ";
    for (int x : res) cout << x << " "; 
    // Output: 3 3 5 5 6 7
    cout << endl;
    
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Input:** `nums = [1, 3, -1, -3, 5, 3, 6, 7]`, `K = 3`.

- **i = 0 (val = 1):** `dq` empty. Push 0. `dq = [0]`. (No result yet).
- **i = 1 (val = 3):** `nums[dq.back()] (1) <= 3`. Pop back. Push 1. `dq = [1]`.
- **i = 2 (val = -1):** `-1 <= 3` is false. Push 2. `dq = [1, 2]`. 
  - `i >= 2`, record `nums[dq.front()]` -> `nums[1] = 3`. Result: `[3]`.
- **i = 3 (val = -3):** `-3 <= -1` is false. Push 3. `dq = [1, 2, 3]`.
  - Record `nums[dq.front()]` -> `3`. Result: `[3, 3]`.
- **i = 4 (val = 5):** 
  - Expired check: `dq.front() (1) <= 4 - 3 (1)`. Yes! Expired. Pop front. `dq = [2, 3]`.
  - Weak check: `nums[3] (-3) <= 5`. Pop back. `dq = [2]`.
  - Weak check: `nums[2] (-1) <= 5`. Pop back. `dq = []`.
  - Push 4. `dq = [4]`.
  - Record `nums[4] = 5`. Result: `[3, 3, 5]`.
*(Continues for the rest of the array...)*

---

## ⚠️ Common Interview Mistakes

1. **Storing Values instead of Indices:** If you store values in the deque, you have NO WAY of knowing when they expire out of the window bounds. You must store indices, and look up the values via `nums[dq.back()]`.
2. **Off-by-One in Expired Check:** The window spans from `i - k + 1` to `i`. Therefore, an index is expired if it is strictly `< i - k + 1`, which is the same as `<= i - k`.
3. **Using a Priority Queue:** $O(N \log K)$ is acceptable in an interview as a brute-force improvement, but they will explicitly ask for $O(N)$. A Max-Heap with lazy deletion (leaving expired indices in the heap until they hit the top) works but is logarithmically slower.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$. Every index is pushed to the deque exactly once and popped at most once. Amortized $O(1)$ per element.
- **Space Complexity:** $O(K)$. The deque stores at most $K$ indices at any given time (if the array is strictly decreasing).

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: What happens if the array is strictly decreasing? (e.g., `[5, 4, 3, 2, 1]`)
**Answer:** The weak element check `nums[dq.back()] <= nums[i]` will never trigger. Every element will be pushed into the deque. However, the deque's size will never exceed $K$ because the "Expired check" at the front will perfectly pop the oldest element just as the window slides.

### Q2: What if we want the Sliding Window Minimum?
**Answer:** Simply change the weak element condition to pop strictly *larger* elements: `nums[dq.back()] >= nums[i]`. This maintains a monotonically *increasing* deque, keeping the minimum at the front.

### Q3: How does this compare to using a balanced BST (like `std::multiset`)?
**Answer:** A `std::multiset` can maintain the moving window in $O(N \log K)$ time. It trivially supports adding and removing arbitrary elements (unlike a PQ which only removes the max). However, the Deque is strictly superior because it operates in amortized $O(1)$ time per element, avoiding tree-balancing overhead.

### Q4: Can this be used for 2D matrices?
**Answer:** Yes! To find the max in a moving $K \times K$ subgrid, you first run the 1D sliding window max on every row (producing a new matrix). Then you run the 1D sliding window max on every column of that new matrix. This solves the 2D version in $O(R \times C)$ time.

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 1425: Constrained Subsequence Sum](https://leetcode.com/problems/constrained-subsequence-sum/)** — DP combined with sliding window max. `dp[i] = nums[i] + max(0, max_in_window(dp[i-k ... i-1]))`.
2. **[Leetcode 862: Shortest Subarray with Sum at Least K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/)** — A legendary Hard problem requiring a Monotonic Deque over prefix sums.
3. **[Leetcode 1438: Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit](https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/)** — Uses TWO deques simultaneously (one max, one min) to bound the window.

---

## 🔗 Cross-Topic Connections
- **Dynamic Programming Optimization:** Used heavily to drop $O(N^2)$ DP down to $O(N)$ when transitioning from a contiguous range of previous states.
- **Two Pointers / Sliding Window:** The generalized parent topic.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Max in every window of size $K$.
- **Data Structure:** `deque<int>` storing **indices**.
- **Rule 1 (Expire):** `if (dq.front() <= i - K) dq.pop_front();`
- **Rule 2 (Evict Weak):** `while (nums[dq.back()] <= nums[i]) dq.pop_back();`
- **Rule 3 (Add):** `dq.push_back(i);`
- **Rule 4 (Record):** `if (i >= K - 1) result = nums[dq.front()];`
- **Time/Space:** $O(N)$ Time | $O(K)$ Space.
