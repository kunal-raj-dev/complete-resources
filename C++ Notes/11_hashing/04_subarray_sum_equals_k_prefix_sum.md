# Lecture 41: Subarray Sum Equals K: Prefix Sum & Hash Map (LeetCode 560)

> **One-Line Purpose:** Master the prefix sum hash table technique to count arbitrary-sum subarrays in $O(N)$ linear time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #41  
> **Video ID:** `KDH4mhFVvHw`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=KDH4mhFVvHw)  
> **Duration:** 34:45  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- Understand why Two Pointers / Sliding Window fails when arrays contain negative integers.
- The Prefix Sum algebraic relation:
  $$\text{sum}(i, j) = \text{prefixSum}[j] - \text{prefixSum}[i - 1] = K \implies \text{prefixSum}[i - 1] = \text{prefixSum}[j] - K$$
- Why the hash map must be pre-populated with `mp[0] = 1` (accounting for subarrays starting at index $0$).

---

## 🔵 Complete C++ Implementation

```cpp
#include <vector>
#include <unordered_map>
#include <iostream>
using namespace std;

class SolutionSubarraySum {
public:
    int subarraySum(vector<int>& nums, int k) {
        unordered_map<int, int> prefixFreq;
        prefixFreq[0] = 1; // Base case: prefix sum of 0 appears once before any elements

        int currentSum = 0;
        int count = 0;

        for (int x : nums) {
            currentSum += x;
            int targetPrefix = currentSum - k;

            if (prefixFreq.count(targetPrefix)) {
                count += prefixFreq[targetPrefix];
            }

            prefixFreq[currentSum]++;
        }

        return count;
    }
};
```
- **Time Complexity:** $O(N)$ — Single linear scan with $O(1)$ average hash map lookups.
- **Space Complexity:** $O(N)$ — Hash table storing distinct prefix sums.

## 🧠 Core Intuition — Why This Works
Think of prefix sum as a "running total" of expenses. If by day 10 you spent $1000, and you want to know if there was a contiguous period where you spent exactly $200 (your `k`). If by day 10 your total is $1000, you just need to look back and ask: "Was there any previous day where my running total was exactly $800?"
If there was (say, day 3), then the expenses from day 4 to day 10 must be exactly $200!
Because the array can have negative numbers, the running total can go up and down. Thus, a previous total of $800 could have happened multiple times. We use a Hash Map to keep track of *how many times* each running total occurred.

## 🎯 Pattern Recognition — When to Use This
- **"Find a subarray with sum K"**: If the array has negative numbers, Sliding Window will fail (because expanding the window doesn't strictly increase the sum). Prefix Sum + Hash Map is the universal $O(N)$ solution.
- **"Count number of subarrays satisfying a condition"**: e.g., sum is divisible by K, or equal number of 0s and 1s. Always use this Prefix Sum Hash Map technique.

## 🔍 Dry Run Trace
**Example:** `nums = [1, -1, 1, 1, 1, 1]`, `k = 3`
Initialize: `prefixFreq = {0: 1}`, `currentSum = 0`, `count = 0`

- `x = 1`: `currentSum = 1`. `target = 1 - 3 = -2`. Not in map. `prefixFreq = {0:1, 1:1}`.
- `x = -1`: `currentSum = 0`. `target = 0 - 3 = -3`. Not in map. `prefixFreq = {0:2, 1:1}`.
- `x = 1`: `currentSum = 1`. `target = 1 - 3 = -2`. Not in map. `prefixFreq = {0:2, 1:2}`.
- `x = 1`: `currentSum = 2`. `target = 2 - 3 = -1`. Not in map. `prefixFreq = {0:2, 1:2, 2:1}`.
- `x = 1`: `currentSum = 3`. `target = 3 - 3 = 0`. In map (count is 2)! `count += 2` (Subarrays: index 0 to 4, and index 2 to 4). `prefixFreq[3] = 1`.
- `x = 1`: `currentSum = 4`. `target = 4 - 3 = 1`. In map (count is 2)! `count += 2`. Total `count = 4`.

Final Count = 4.

## ⚠️ Common Interview Mistakes
1. **Forgetting `prefixFreq[0] = 1`:** If a subarray starting from index 0 exactly matches `k`, `currentSum - k` will be `0`. If `0` isn't in the map, you'll miss this valid subarray.
2. **Updating the map before checking:** You MUST check if `currentSum - k` exists and add to `count` *before* incrementing `prefixFreq[currentSum]`. If `k = 0`, doing it in the wrong order will count the current element itself as a valid subarray even if it's not.
3. **Using Sliding Window:** Trying to use a `left` and `right` pointer. Sliding window only works if the array contains strictly non-negative numbers.

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Why does sliding window fail when negative numbers are present?
Sliding window relies on a monotonic property: expanding the window (moving `right`) always increases or maintains the sum, and shrinking the window (moving `left`) always decreases or maintains it. With negative numbers, expanding the window might *decrease* the sum. You wouldn't know whether to move `left` or `right` to hit `target K`.

### Q2: What if we are asked to return the *longest* subarray with sum K instead of the count?
Instead of storing the *frequency* of each prefix sum, store the *first index* at which each prefix sum occurred. `if (mp.count(currentSum - k))`, update `maxLength = max(maxLength, i - mp[currentSum - k])`. Do *not* update the index in the map if the prefix sum is already present, to maximize the length.

### Q3: How do we solve "Subarray sum divisible by K" using this pattern?
Instead of storing `currentSum`, store `currentSum % K`. If the modulo is negative (in C++), adjust it by `(mod + K) % K`. If you see the same modulo again, it means the subarray between the two points has a sum divisible by K.

### Q4: Can this be optimized to $O(1)$ space?
No. To look up any arbitrary previous prefix sum in $O(1)$ time, we fundamentally need an auxiliary data structure to store them.

## 🏆 Related Problems (Leetcode)
- **[974. Subarray Sums Divisible by K](https://leetcode.com/problems/subarray-sums-divisible-by-k/)**: Uses the exact same pattern but with modulo math.
- **[525. Contiguous Array](https://leetcode.com/problems/contiguous-array/)**: Find longest subarray with equal 0s and 1s (replace 0 with -1 and find target sum 0).
- **[437. Path Sum III](https://leetcode.com/problems/path-sum-iii/)**: Prefix sum hash map technique applied to a Binary Tree DFS!

## 🔗 Cross-Topic Connections
- **Trees (DFS)**: This exact pattern is used to find paths summing to K going downwards in a Binary tree (Path Sum III).
- **Math**: Divisibility rules and modulo arithmetic for variant problems.

## ⚡ 2-Minute Revision Flash Card
- **Pattern:** Subarray Sum == K (array with negatives).
- **Core Equation:** `PrefixSum[j] - K = PrefixSum[i-1]`.
- **Implementation:** `map[0] = 1`. Iterate, add to `currentSum`. Check `currentSum - k` in map, add its frequency to answer. Finally, increment `map[currentSum]`.
- **Sliding Window Trap:** Fails on negative numbers because the sum function is not monotonic.
