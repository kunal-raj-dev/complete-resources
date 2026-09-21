# Lecture 39: 3 Sum: Sorting & Two Pointers (LeetCode 15)

> **One-Line Purpose:** Master two-pointer inward scanning with comprehensive duplicate skipping to identify all unique zero-sum triplets in $O(N^2)$ time and $O(1)$ auxiliary space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #39  
> **Video ID:** `K-RsltkN63w`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=K-RsltkN63w)  
> **Duration:** 43:43  
> **Status:** AUDITED  

---

## 🔵 Lecture Content & Implementation

```cpp
#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;

class SolutionThreeSum {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int>> res;
        int n = nums.size();
        sort(nums.begin(), nums.end()); // Crucial: Sort first

        for (int i = 0; i < n - 2; i++) {
            // Optimization: If smallest element is > 0, three positive numbers cannot sum to 0
            if (nums[i] > 0) break;

            // Skip duplicates for the first element
            if (i > 0 && nums[i] == nums[i - 1]) continue;

            int left = i + 1;
            int right = n - 1;

            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];

                if (sum == 0) {
                    res.push_back({nums[i], nums[left], nums[right]});

                    // Skip duplicates for left and right
                    while (left < right && nums[left] == nums[left + 1]) left++;
                    while (left < right && nums[right] == nums[right - 1]) right--;

                    left++;
                    right--;
                } else if (sum < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }
        return res;
    }
};
```
- **Time Complexity:** $O(N \log N + N^2) = O(N^2)$.
- **Space Complexity:** $O(1)$ auxiliary (excluding output).

## 🧠 Core Intuition — Why This Works
If you fix one number $X$, the problem reduces exactly to the **Two Sum** problem: find two numbers that sum to $-X$. 
While Two Sum can be solved in $O(N)$ with a Hash Map, doing that $N$ times (for each $X$) gives $O(N^2)$ time and $O(N)$ space.
However, because we are looking for *combinations* and order doesn't matter (a triplet `[a, b, c]` is the same as `[b, c, a]`), we can **sort the array first**. Once sorted, we can solve the inner Two Sum problem in $O(N)$ time using the **Two-Pointer technique**, requiring $O(1)$ space. Sorting also groups identical numbers together, making it trivial to skip duplicates by just checking if `nums[i] == nums[i-1]`.

## 🎯 Pattern Recognition — When to Use This
- **"Find 3 (or 4, or K) elements that sum to a target"**: Sorting + fixing one element + Two Pointers on the remainder is the universal blueprint.
- **"Return all UNIQUE triplets/quadruplets"**: Using a HashSet to filter duplicates is often $O(N^3)$ or causes TLE due to hashing overhead. Sorting + skipping adjacent identical elements is the optimal $O(1)$ space way to ensure uniqueness.

## 🔍 Dry Run Trace
**Example:** `nums = [-1, 0, 1, 2, -1, -4]`
1. **Sort:** `[-4, -1, -1, 0, 1, 2]`
2. **`i = 0` (`-4`):**
   - `left = 1` (`-1`), `right = 5` (`2`)
   - Sum: `-4 + (-1) + 2 = -3 < 0`. Move `left++`.
   - `left = 2` (`-1`), `right = 5` (`2`). Sum = `-3`. `left++`.
   - Eventually `left >= right`.
3. **`i = 1` (`-1`):**
   - `left = 2` (`-1`), `right = 5` (`2`)
   - Sum: `-1 + (-1) + 2 = 0`. **MATCH!** Add `[-1, -1, 2]`.
   - Skip duplicates: `left` moves to `3` (`0`), `right` moves to `4` (`1`).
   - Sum: `-1 + 0 + 1 = 0`. **MATCH!** Add `[-1, 0, 1]`.
   - `left` moves to `4`, `right` moves to `3`. Break loop.
4. **`i = 2` (`-1`):** `nums[i] == nums[i-1]`. **SKIP!** (Prevents duplicate triplet `[-1, 0, 1]`).
5. **`i = 3` (`0`):** `left = 4`, `right = 5`. Sum > 0.
Result: `[[-1, -1, 2], [-1, 0, 1]]`.

## ⚠️ Common Interview Mistakes
1. **Forgetting to skip duplicates for `left` and `right`:** Only skipping for `i` will still result in duplicate triplets if the array has multiple identical pairs (e.g., `[-2, 1, 1, 1, 1]`).
2. **Skipping duplicates *before* recording the triplet:** You must record the triplet first when `sum == 0`, and *then* advance `left` and `right` past duplicates. 
3. **Using a Hash Set for uniqueness:** Interviewers will dock points if you use `set<vector<int>>` to remove duplicates. It works, but wastes $O(K)$ space and adds $O(\log K)$ time overhead per insertion. Learn the adjacent-skip logic!

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Why sort the array? Doesn't that take $O(N \log N)$ time?
Yes, sorting takes $O(N \log N)$. But the nested Two-Pointer loop takes $O(N^2)$. The overall time is $O(N \log N + N^2) = O(N^2)$. The sort doesn't worsen our asymptotic complexity, but it drops the auxiliary space from $O(N)$ (if we used a Hash Map) down to $O(1)$, and makes duplicate skipping trivial.

### Q2: What is the `if (nums[i] > 0) break;` optimization?
Since the array is sorted, if our currently fixed element `nums[i]` is strictly greater than 0 (our target), all numbers to its right are also $> 0$. Three positive numbers can never sum to 0. We can safely terminate the entire algorithm early.

### Q3: How do we adapt this to "3Sum Closest"?
Instead of `if (sum == 0)`, you maintain a `minDiff` variable. `if (abs(sum - target) < minDiff)`, you update `minDiff` and the `closestSum`. If `sum < target`, `left++`; if `sum > target`, `right--`.

### Q4: Can we solve 3Sum in less than $O(N^2)$ time?
No. To date, there is no known algorithm that solves 3Sum faster than $O(N^2)$ in the worst case. 

## 🏆 Related Problems (Leetcode)
- **[16. 3Sum Closest](https://leetcode.com/problems/3sum-closest/)**: Find the triplet whose sum is closest to target.
- **[18. 4Sum](https://leetcode.com/problems/4sum/)**: Add one more outer loop to fix two numbers, making it $O(N^3)$.
- **[259. 3Sum Smaller](https://leetcode.com/problems/3sum-smaller/)**: Count triplets with sum strictly less than target.

## 🔗 Cross-Topic Connections
- **Two Pointers:** The core algorithmic engine powering the $O(N)$ search space reduction.
- **Sorting / Binary Search:** Sorting is the prerequisite enabler for both Two Pointers and Binary Search optimizations.

## ⚡ 2-Minute Revision Flash Card
- **Core Idea:** Sort array $\to$ Fix `nums[i]` $\to$ Two-Pointer search for `-nums[i]` in the remainder.
- **Duplicate Skipping (i):** `if (i > 0 && nums[i] == nums[i-1]) continue;`
- **Duplicate Skipping (L/R):** When match found, `while (nums[L] == nums[L+1]) L++;`
- **Early Exit:** `if (nums[i] > target) break;` (if target is 0).
- **Time/Space:** $O(N^2)$ Time, $O(1)$ Space.
