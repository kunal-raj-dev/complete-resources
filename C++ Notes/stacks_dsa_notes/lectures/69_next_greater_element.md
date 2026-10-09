# Lecture 69 — Next Greater Element

[Study index](../README.md) · [Previous: Stock Span](68_stock_span.md) · [Next: Previous Smaller](70_previous_smaller_element.md)

**Source:** [Next Greater Element lecture](https://www.youtube.com/watch?v=NKbExYwvjb0). **Verification:** full auto-caption sequence reviewed; selected code frame checked. [Coverage record](../SOURCE_COVERAGE.md#lecture-69).

**Prerequisites:** stacks, reverse array traversal, strict comparisons, and key/value maps.

## Contents

- [1. Define next greater precisely](#1-define-next-greater-precisely)
- [2. Reverse traversal and the candidate stack](#2-reverse-traversal-and-the-candidate-stack)
- [3. Why discarded values are never needed](#3-why-discarded-values-are-never-needed)
- [4. C++17 implementation and complexity](#4-c17-implementation-and-complexity)
- [5. Next Greater Element I — two arrays](#5-next-greater-element-i--two-arrays)
- [6. Additional explanation, pitfalls, and revision](#6-additional-explanation-pitfalls-and-revision)

## 1. Define next greater precisely

**Lecture flow: approximately 00:33–02:59.** For position i, find the **first position j > i** such that `a[j] > a[i]`. Return that position's value, or `-1` if it does not exist.

“First” means closest in array order. It does not mean the largest value on the right, or the numerically smallest value greater than the current value. In `[4,9,6]`, the next greater value for 4 is **9**, even though 6 is smaller than 9 and still exceeds 4.

The lecture uses `[6,8,0,1,3]`, whose answers are `[8,-1,1,3,-1]`. The final element always lacks an element to its right. Equality is insufficient: the next greater answer for the first element of `[5,5]` is `-1`.

## 2. Reverse traversal and the candidate stack

**Lecture flow: approximately 02:59–07:23.** To answer a query about the right side, first process the right side. Scan from `n-1` toward 0. At position i, the stack contains useful candidates from the already processed suffix.

The top is the most recently encountered surviving suffix element, hence the nearest surviving candidate. Remove any top `<= a[i]`, since it cannot answer a strictly greater query. The remaining top, if any, is the answer. Push the current value **after** answering so it becomes a candidate for earlier positions.

**Original dry run:** `[4,7,2,2,6]`. Stacks contain values, bottom → top.

| i | Current | Before | Popped | Answer at i | After push |
|---|---|---|---|---|---|
| 4 | 6 | `[]` | None | -1 | `[6]` |
| 3 | 2 | `[6]` | None | 6 | `[6,2]` |
| 2 | 2 | `[6,2]` | 2 | 6 | `[6,2]` |
| 1 | 7 | `[6,2]` | 2,6 | -1 | `[7]` |
| 0 | 4 | `[7]` | None | 7 | `[7,4]` |

Output is `[7,-1,6,6,-1]`. Answer positions remain in original input order even though we compute them backward.

**Invariant:** stack positions, if tracked, decrease from bottom to top; candidate values strictly decrease from bottom to top. The top is the nearest remaining suffix candidate. The stack need not contain every suffix element.

## 3. Why discarded values are never needed

**Lecture flow: approximately 07:23–08:59.** This is the key correctness question. Suppose current value x removes a later value y with `y <= x`. For an earlier value z:

- If `z < x`, then x is a greater value and is closer than y. Even if y also exceeds z, y cannot be z's **first** greater value.
- If `z >= x`, then `y <= x <= z`, so y is not greater than z at all.

These cases cover z smaller than, equal to, or larger than x. Therefore y is dominated by x and can be discarded permanently. This argument is stronger than saying “y is useless for the current query”: it proves y is useless for **every future query in this traversal**.

With invalid tops removed, the nearest surviving candidate is a valid greater answer. Any removed candidate closer than it failed the comparison or was dominated by an even closer suitable candidate. This establishes both validity and nearestness.

## 4. C++17 implementation and complexity

**Lecture flow: approximately 08:59–15:20.** Values are enough when the required result is a value. Use indices when you need positions or distances.

```cpp
#include <stack>
#include <vector>

std::vector<int> nextGreaterValues(const std::vector<int>& a) {
    const int n = static_cast<int>(a.size());
    std::vector<int> answer(n, -1);
    std::stack<int> candidates;
    for (int i = n - 1; i >= 0; --i) {
        while (!candidates.empty() && candidates.top() <= a[i])
            candidates.pop();
        if (!candidates.empty()) answer[i] = candidates.top();
        candidates.push(a[i]);
    }
    return answer;
}
```

Usage: `nextGreaterValues({4,7,2,2,6})` returns `{7,-1,6,6,-1}`. Empty input returns empty output. `int i = static_cast<int>(size)-1` avoids the unsigned wraparound trap of computing `size()-1` before conversion.

Every occurrence is pushed once and popped at most once. The outer traversal costs O(n); all pops together cost O(n). Total time is O(n), auxiliary stack space O(n), and output space O(n). One iteration can still do many pops. A nested `while` exists syntactically; amortized operation counting explains why it does not produce O(n²) total work.

**Additional baseline:** scan `j=i+1,i+2,...` and stop at the first `a[j]>a[i]`. This is correct but O(n²) in the worst case. It is useful as a small-input oracle when testing the stack algorithm.

```cpp
#include <vector>

std::vector<int> nextGreaterBrute(const std::vector<int>& a) {
    const int n = static_cast<int>(a.size());
    std::vector<int> answer(n, -1);
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (a[j] > a[i]) { answer[i] = a[j]; break; }
        }
    }
    return answer;
}
```

Usage: `nextGreaterBrute({4,7,2,2,6})` also returns `{7,-1,6,6,-1}`. Scanning in position order and stopping at the first match establishes nearestness. Auxiliary space is O(1), output space O(n).

## 5. Next Greater Element I — two arrays

**Lecture flow: approximately 15:20–22:59.** The lecture next applies the concept to [LeetCode 496](https://leetcode.com/problems/next-greater-element-i/). `nums1` is a subset of `nums2`, and each array contains distinct values. For every query in `nums1`, find its next greater element **in the order of `nums2`**. Preserve the query order in the output.

The lecture illustrates queries `[4,1,2]` against `[1,3,4,2]`, yielding `[-1,3,-1]`. These arrays have different roles: `nums2` supplies neighborhood/order; `nums1` supplies query/output order.

The direct baseline searches for each query in `nums2` and then scans to its right. With m queries and n reference elements, worst-case time is O(mn). The optimized method separates preprocessing from queries:

1. Compute each `nums2` value's next greater value with the reverse stack scan.
2. Store the mapping `value → next greater value` in an unordered map.
3. Look up the queries in `nums1` order.

```cpp
#include <stack>
#include <stdexcept>
#include <unordered_map>
#include <vector>

std::vector<int> nextGreaterElementIBrute(const std::vector<int>& nums1,
                                        const std::vector<int>& nums2) {
    const int n = static_cast<int>(nums2.size());
    std::vector<int> answer;
    for (int query : nums1) {
        int position = 0;
        while (position < n && nums2[position] != query) ++position;
        if (position == n) throw std::out_of_range("query absent from reference");
        int value = -1;
        for (int j = position + 1; j < n; ++j) {
            if (nums2[j] > query) { value = nums2[j]; break; }
        }
        answer.push_back(value);
    }
    return answer;
}

std::vector<int> nextGreaterElementI(const std::vector<int>& nums1,
                                   const std::vector<int>& nums2) {
    std::unordered_map<int, int> next;
    next.reserve(nums2.size());
    std::stack<int> candidates;
    for (int i = static_cast<int>(nums2.size()) - 1; i >= 0; --i) {
        const int x = nums2[i];
        while (!candidates.empty() && candidates.top() <= x)
            candidates.pop();
        next[x] = candidates.empty() ? -1 : candidates.top();
        candidates.push(x);
    }
    std::vector<int> answer;
    answer.reserve(nums1.size());
    for (int x : nums1) answer.push_back(next.at(x));
    return answer;
}
```

Usage: queries `{7,4,2}` and reference `{4,7,2,6}` produce `{-1,7,6}`. The preprocessing map is `4→7`, `7→-1`, `2→6`, `6→-1`. `at()` makes an accidentally absent query visible through an exception; the official subset condition guarantees presence.

The baseline function produces the same answer with O(mn) time, O(1) auxiliary space, and O(m) output. The optimized function's map avoids repeating reference scans for each query.

Time is **expected O(n+m)** with an unordered map; hash-table worst-case behavior is not guaranteed constant. Auxiliary space is O(n), output space O(m). A balanced ordered map would give O((n+m) log n) time with deterministic logarithmic operations.

**Why uniqueness matters:** in `[2,3,2,4]`, the first 2's next greater is 3, while the second 2's is 4. A single key `2` cannot represent both. For occurrence-sensitive problems, preprocess by index and query by position instead of by value.

## 6. Additional explanation, pitfalls, and revision

- Use `<=` for candidate removal; keeping equality yields a non-greater answer.
- Store index results with sentinel `-1` if actual values can also be `-1` and the caller needs to distinguish absence from a real answer. The value-returning judge format deliberately uses `-1` for absence.
- Do not sort the array: next greater depends on positional order.
- Do not confuse “no answer yet” in a forward scan with “no answer exists” after finishing the scan.
- In a forward unresolved-index approach, pop while **current > old top value**. This is a different stack role from the reverse candidate method; copying its comparison blindly is a common bug. See [monotonic stack patterns](../supplements/monotonic_stack_patterns.md).

**Interview check:** prove domination; explain why reverse traversal helps; convert the result from values to distances; state why a value-keyed map works for 496 but fails with duplicate occurrences.

**Lecture follow-up:** the next lesson changes the target to previous smaller. Try deriving its scan direction and comparison before reading it.

**Revision:** reverse scan, discard `<= current`, read surviving top, push current. For two-array queries, preprocess the reference array and answer through a map.
