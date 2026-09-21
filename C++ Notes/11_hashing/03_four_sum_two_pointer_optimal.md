# Lecture 40: 4 Sum: Optimal Multi-Pointer Reduction (LeetCode 18)

> **One-Line Purpose:** Extend two-pointer quadratic reduction to 4-quadruplet discovery with 64-bit integer overflow protection.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #40  
> **Video ID:** `X6sL8JTROLY`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=X6sL8JTROLY)  
> **Duration:** 23:02  
> **Status:** AUDITED  

---

## 🔵 Lecture Content & Implementation

```cpp
#include <vector>
#include <algorithm>
using namespace std;

class SolutionFourSum {
public:
    vector<vector<int>> fourSum(vector<int>& nums, int target) {
        vector<vector<int>> res;
        int n = nums.size();
        sort(nums.begin(), nums.end());

        for (int i = 0; i < n - 3; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;

            for (int j = i + 1; j < n - 2; j++) {
                if (j > i + 1 && nums[j] == nums[j - 1]) continue;

                int left = j + 1;
                int right = n - 1;

                while (left < right) {
                    // Use 64-bit integer to prevent overflow during sum
                    long long sum = (long long)nums[i] + nums[j] + nums[left] + nums[right];

                    if (sum == target) {
                        res.push_back({nums[i], nums[j], nums[left], nums[right]});
                        while (left < right && nums[left] == nums[left + 1]) left++;
                        while (left < right && nums[right] == nums[right - 1]) right--;
                        left++;
                        right--;
                    } else if (sum < target) {
                        left++;
                    } else {
                        right--;
                    }
                }
            }
        }
        return res;
    }
};
```
- **Time Complexity:** $O(N^3)$.
- **Space Complexity:** $O(1)$ auxiliary.


## 🧠 Core Intuition — Why This Works
Four Sum is an extension of Three Sum. While a naive solution takes $O(N^4)$, we can reduce this to $O(N^3)$ by fixing two numbers and using the two-pointer technique to find the remaining two. Sorting is necessary to make the two-pointer approach work and to effortlessly skip duplicates. By fixing the first two elements (`nums[i]` and `nums[j]`), the problem reduces to the classic Two Sum (on a sorted array) for a new target `target - (nums[i] + nums[j])`.

## 🎯 Pattern Recognition — When to Use This
- **"Find all unique quadruplets/triplets"**: Signals sorting the array first to avoid duplicate results without needing a heavy Hash Set.
- **"Sum of $K$ elements equals Target"**: The general pattern is $O(N^{K-1})$. For $K=4$, it takes $O(N^3)$.
- **Skipping Duplicates**: `if (i > 0 && nums[i] == nums[i-1]) continue;` is the standard blueprint for bypassing adjacent duplicates in a sorted array to guarantee unique subsets.

## 🔍 Dry Run Trace
**Example:** `nums = [1, 0, -1, 0, -2, 2]`, `target = 0`
- **Sorted Array:** `[-2, -1, 0, 0, 1, 2]`
- **i = 0 (`nums[0] = -2`)**:
  - **j = 1 (`nums[1] = -1`)**: `new_target = 0 - (-3) = 3`. 
    - `left = 2` (`0`), `right = 5` (`2`). Sum = 2 < 3. `left++`.
    - `left = 3` (`0`), `right = 5` (`2`). Sum = 2 < 3. `left++`.
    - `left = 4` (`1`), `right = 5` (`2`). Sum = 3 == 3. Found! `[-2, -1, 1, 2]`. 
  - **j = 2 (`nums[2] = 0`)**: `new_target = 0 - (-2) = 2`.
    - `left = 3` (`0`), `right = 5` (`2`). Sum = 2 == 2. Found! `[-2, 0, 0, 2]`.
- (Continues, skipping duplicate logic kicks in effectively).

## ⚠️ Common Interview Mistakes
1. **Integer Overflow:** `nums[i] + nums[j] + nums[left] + nums[right]` can exceed 32-bit limits. Always use `long long` to cast the sum before comparing it to `target`.
2. **Forgetting to skip duplicates for `j`**: Many candidates remember `if (i > 0 && nums[i] == nums[i-1]) continue;` but forget `if (j > i + 1 && nums[j] == nums[j-1]) continue;`. Both are critical to avoid duplicate quadruplets.
3. **Using Hash Sets for Uniqueness:** While you can dump answers into a `set<vector<int>>`, it adds $O(\log(\text{unique triplets}))$ overhead and extra space. It is viewed as unoptimized in top interviews.

## 📊 Complexity Analysis
- **Time Complexity:** $O(N^3)$. Two nested loops for $i$ and $j$ give $O(N^2)$, and the two-pointer while loop takes $O(N)$. Overall $O(N \log N + N^3) \approx O(N^3)$.
- **Space Complexity:** $O(1)$ auxiliary space (or $O(N)$ depending on sorting algorithm implementation under the hood, but typically $O(1)$ extra space).

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Can we optimize 4Sum to $O(N^2)$?
**Answer:** We can reduce the average time to $O(N^2)$ using a Hash Map by storing the sum of all pairs `(nums[i] + nums[j])` and their indices. However, avoiding duplicate quadruplets in this approach makes the implementation extremely complex, and the worst-case space complexity blows up to $O(N^2)$. Thus, the $O(N^3)$ two-pointer approach is the standard expected optimal solution.

### Q2: What if we needed 5Sum or kSum?
**Answer:** We can generalize this into a recursive `kSum` function. For `kSum`, we fix one element and recursively call `(k-1)Sum` until `k == 2`, at which point we use the standard two-pointer approach. Time complexity for `kSum` is $O(N^{k-1})$.

## 🏆 Related Problems
- **[15. 3Sum](https://leetcode.com/problems/3sum/)**: The precursor. $O(N^2)$.
- **[16. 3Sum Closest](https://leetcode.com/problems/3sum-closest/)**: Similar idea but minimizing `abs(target - sum)`.
- **[454. 4Sum II](https://leetcode.com/problems/4sum-ii/)**: Given 4 separate arrays, find tuples. Best solved in $O(N^2)$ using a Hash Map since duplicates don't need filtering.

## 🔗 Cross-Topic Connections
- **Two Pointers:** The core mechanism for the innermost loops.
- **Recursion / Generalization:** Transitioning from 3Sum to 4Sum to `kSum`.

## ⚡ 2-Minute Revision Flash Card
- **Pattern:** `kSum` $\rightarrow$ Sort + $(k-2)$ loops + Two Pointers.
- **Condition:** Fix `i`, fix `j`, `left = j+1`, `right = n-1`.
- **Avoid Duplicates:** `if (idx > start_idx && nums[idx] == nums[idx-1]) continue;`
- **Trap:** Beware of integer overflow when summing 4 large integers!
