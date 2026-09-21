# ⚡ Topic 11 Revision: Hashing & Prefix Sum Patterns

> **High-Density Review:** Two Sum hash lookup, Prefix sum frequency equations, and k-Sum generalizations.

---

## 1. Core Hashing Patterns

| Problem | Optimal Technique | Time Complexity | Auxiliary Space | Core Invariant |
|---|---|---|---|---|
| **Two Sum** | Hash Map Complement | $O(N)$ | $O(N)$ | Lookup `target - nums[i]` |
| **3-Sum** | Sort + Two Pointers | $O(N^2)$ | $O(1)$ aux | Skip duplicate values |
| **4-Sum** | Sort + Double Loop + 2-Pointer | $O(N^3)$ | $O(1)$ aux | Cast sums to `long long` |
| **Subarray Sum = K** | Prefix Sum Frequency Hash Map | $O(N)$ | $O(N)$ | `prefix[j] - prefix[i] = K` |

---

## 2. Subarray Sum Equals K Template
```cpp
int subarraySum(vector<int>& nums, int k) {
    unordered_map<int, int> prefixCounts;
    prefixCounts[0] = 1; // Base case: prefix sum 0 occurs once before index 0

    int currentSum = 0, totalCount = 0;
    for (int x : nums) {
        currentSum += x;
        if (prefixCounts.find(currentSum - k) != prefixCounts.end()) {
            totalCount += prefixCounts[currentSum - k];
        }
        prefixCounts[currentSum]++;
    }
    return totalCount;
}
```
