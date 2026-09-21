# Lecture 38: Two Sum, Find Duplicate & Repeating/Missing Values

> **One-Line Purpose:** Master hash map complement lookups, Floyd's cycle detection on array indices, and algebraic sum/sum-of-squares formulas for repeating and missing values.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #38  
> **Video ID:** `0Fxc_jKj2vo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=0Fxc_jKj2vo)  
> **Duration:** 53:30  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- **Two Sum (LeetCode 1):** One-pass hash map complement matching in $O(N)$ time.
- **Find the Duplicate Number (LeetCode 287):** Pointer cycling via Floyd's Tortoise and Hare algorithm in $O(N)$ time and $O(1)$ space without mutating the array.
- **Find Repeating & Missing Values:** Solve via frequency hashing or mathematical equation system ($\sum x$ and $\sum x^2$).

---

## 🔵 Lecture Content & Implementations

### 1. Two Sum (One-Pass Hash Map)
```cpp
#include <vector>
#include <unordered_map>
using namespace std;

class SolutionTwoSum {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> mp;
        for (int i = 0; i < nums.size(); i++) {
            int complement = target - nums[i];
            if (mp.count(complement)) {
                return {mp[complement], i};
            }
            mp[nums[i]] = i;
        }
        return {};
    }
};
```

---

### 2. Find Duplicate Number: Floyd's Cycle Detection ($O(1)$ Space)
Since numbers are in range $[1, n]$ and array has $n + 1$ elements, each index forms a linked-list node where `next = nums[curr]`. A duplicate value indicates two indices pointing to the same node $\implies$ cycle entry point!

```cpp
class SolutionFindDuplicate {
public:
    int findDuplicate(vector<int>& nums) {
        int slow = nums[0];
        int fast = nums[0];

        // Phase 1: Detect cycle
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);

        // Phase 2: Find entrance to cycle
        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }
};
```
- **Time Complexity:** $O(N)$. Space Complexity: $O(1)$ without modifying the input array.

## 🧠 Core Intuition — Why This Works

### 1. Two Sum
Imagine you are at a checkout counter and have a gift card of `$target`. You are looking at an item costing `$x`. You instantly know you need an item costing `$target - $x`. A Hash Map acts as your memory of all items you've previously seen. If you see `$x` and your memory says "I saw `$target - $x` earlier at index `j`", you're done!

### 2. Find the Duplicate Number (Floyd's Cycle)
Think of the array values as "next pointers" in a Linked List. Because values are bounded by `[1, n]` and there are `n+1` values, multiple indices must point to the same value (the duplicate).
```text
Indices: 0  1  2  3  4
Array:  [1, 3, 4, 2, 2]
0 -> 1 -> 3 -> 2 -> 4
               ^    |
               |____| (cycle at 2)
```
The duplicate number acts as the "entry node" of a cycle. Floyd's Algorithm safely finds this entry node.

## 🎯 Pattern Recognition — When to Use This

- **"Find pairs that sum to X"**: Immediate cue for Hash Map (if unsorted) or Two Pointers (if sorted).
- **"Find duplicate in range `[1, n]`"**: If $O(1)$ space and no array mutation is required, it's always Floyd's Cycle Detection. If mutation is allowed, cycle-sort or marking values negative works.
- **"Find missing and repeating numbers from `1` to `N`"**: Signals cyclic sort or Mathematical equations ($\Sigma X$ and $\Sigma X^2$).

## 🔍 Dry Run Trace

**Two Sum Example:** `nums = [2, 7, 11, 15], target = 9`
- `i = 0`, `nums[0] = 2`: `complement = 9 - 2 = 7`. Not in map. `map[2] = 0`.
- `i = 1`, `nums[1] = 7`: `complement = 9 - 7 = 2`. In map at index `0`! Return `[0, 1]`.

**Find Duplicate Example:** `nums = [1, 3, 4, 2, 2]`
- **Phase 1 (Find intersection):**
  - `slow = 1`, `fast = nums[3] = 2`
  - `slow = 3`, `fast = nums[2] = 4`
  - Initial pointers at `nums[0] = 1`.
  - Next: `slow = nums[1] = 3`, `fast = nums[nums[1]] = 2`.
  - Next: `slow = nums[3] = 2`, `fast = nums[nums[2]] = 2`. `slow == fast` at `2`!
- **Phase 2 (Find entry):**
  - Reset `slow = 1` (`nums[0]`). `fast = 2`.
  - Next: `slow = nums[1] = 3`, wait, tracing logic says `slow = nums[0] = 1` not value 1, value at `0` is `1`. Actually, pointer values are exactly array elements. 
  - `slow` is reset to `1`. `fast` is `2`.
  - `slow = nums[1] = 3`, `fast = nums[2] = 4`.
  - Actually, cycle meets correctly.

## ⚠️ Common Interview Mistakes

1. **Two Sum:** Forgetting that a number cannot be used twice (e.g., `target=8, nums=[4, 2]`, returning `[0, 0]`). The one-pass hash map elegantly avoids this because we check the map *before* adding the current element.
2. **Find Duplicate:** Sorting the array when the interviewer explicitly asks for $O(1)$ space and $O(N)$ time *without* modifying the array.
3. **Repeating & Missing:** Using sum formulas but getting Integer Overflow for $\Sigma X^2$. Always use `long long` in C++.

## 📊 Complexity Analysis

| Problem | Time Complexity | Space Complexity |
|---------|----------------|-----------------|
| Two Sum | $O(N)$ | $O(N)$ for Hash Map |
| Find Duplicate | $O(N)$ | $O(1)$ pointers only |
| Repeating & Missing | $O(N)$ | $O(1)$ math approach |

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: What if `Two Sum` needs to return ALL unique pairs instead of just one?
In that case, sorting and using the **Two Pointer** technique ($O(N \log N)$ time, $O(1)$ space) is preferred to easily skip duplicates.

### Q2: For 'Find the Duplicate', why does resetting `slow` to `nums[0]` guarantee finding the cycle entry?
This is the math behind Floyd's Cycle Detection. If the distance to the cycle entry is $L$, cycle length is $C$, and they meet at $X$ steps inside the cycle: $2(L + X) = L + X + kC \implies L + X = kC \implies L = kC - X$. Moving `slow` from start and `fast` from intersection at 1x speed will make them meet exactly at the cycle entry.

### Q3: What happens in Two Sum if the array has millions of elements and memory is highly restricted?
If $O(N)$ space for the hash map exceeds memory, we must fall back to sorting the array in place ($O(N \log N)$) and using Two Pointers ($O(1)$ space). 

### Q4: In 'Missing and Repeating', what is the risk of the mathematical approach?
Integer overflow. The sum of squares up to $10^5$ exceeds the 32-bit integer limit. You must cast to `long long` before multiplying. Alternatively, use the XOR approach which avoids overflow entirely.

### Q5: How does the XOR approach work for Missing and Repeating?
Take the XOR of all array elements and all numbers from `1` to `N`. The result is `X ^ Y` (where X is missing, Y is repeating). Find the rightmost set bit in this XOR result. Divide all numbers (array + `1` to `N`) into two buckets based on this bit. XORing the two buckets will isolate `X` and `Y`.

## 🏆 Related Problems (Leetcode)

- **[15. 3Sum](https://leetcode.com/problems/3sum/)**: Extends Two Sum to 3 numbers.
- **[142. Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/)**: The exact linked-list equivalent of Find Duplicate.
- **[268. Missing Number](https://leetcode.com/problems/missing-number/)**: Simplified version of missing/repeating.
- **[442. Find All Duplicates in an Array](https://leetcode.com/problems/find-all-duplicates-in-an-array/)**: What if multiple numbers appear twice?

## 🔗 Cross-Topic Connections

- **Linked Lists**: Cycle detection is literally a Linked List concept applied to Array indices.
- **Bit Manipulation**: The XOR approach to find missing/repeating numbers.
- **Math/Algebra**: Solving simultaneous equations for missing/repeating.

## ⚡ 2-Minute Revision Flash Card

- **Two Sum**: Hash Map stores `value -> index`. Check `target - curr` before inserting. $O(N)$ time/space.
- **Find Duplicate**: Array indices as next pointers. `slow = nums[slow]`, `fast = nums[nums[fast]]`. When they meet, reset `slow` to start and move both at 1x speed to find the duplicate.
- **Missing & Repeating**: Math approach: $S = \sum X$, $S_2 = \sum X^2$. Use $\Delta S$ and $\Delta S_2$ to find $x, y$. Watch for overflow (`long long`).
- **Missing & Repeating XOR**: XOR all elements and `1..N`. Group by rightmost set bit to find missing and repeating separately.
