# Lecture 73 — Next Greater Element II

[Topic Index](./00_master_index.md) · [Previous: Histogram](./07_largest_rectangle_in_histogram.md) · [Next: Rainwater](./09_trapping_rainwater.md)

**Source:** [Lecture 73](https://www.youtube.com/watch?v=If--3pm9K3U). **Verification:** full auto-caption sequence reviewed; circular indexing and code frame checked. [Coverage record](../stacks_dsa_notes/SOURCE_COVERAGE.md#lecture-73).

**Prerequisites:** next greater, index stacks, modulo, and circular traversal.

## Contents

- [1. Circular next greater](#1-circular-next-greater)
- [2. Brute force and the doubled-array idea](#2-brute-force-and-the-doubled-array-idea)
- [3. Virtual indices and original dry run](#3-virtual-indices-and-original-dry-run)
- [4. C++17 implementation](#4-c17-implementation)
- [5. Correctness and complexity](#5-correctness-and-complexity)
- [6. Pitfalls and revision](#6-pitfalls-and-revision)

## 1. Circular next greater

**Lecture flow: approximately 01:06–02:49.** After the last position, traversal wraps to position 0. For i, search positions `i+1, ..., n-1, 0, ..., i-1` in that order. The first strictly greater value is the answer. If none exists, return `-1`.

The [official LeetCode 503 statement](https://leetcode.com/problems/next-greater-element-ii/) allows negative values and duplicate occurrences. Circularity changes the search order; it does not make equality count as greater.

The lecture first illustrates `[1,2,3,4,3]`, producing `[2,3,4,-1,4]`, then uses `[3,6,5,4,2]`, producing `[6,-1,6,6,3]`. The last 2 reaches 3 after wrapping; the 6 is a maximum and has no strictly greater answer anywhere.

## 2. Brute force and the doubled-array idea

**Lecture flow: approximately 02:49–08:34.** A baseline scans at most n-1 other positions for each starting position, using `(i+step)%n`. This is O(n²).

**Additional baseline implementation:** useful for checking the circular search order independently of a stack.

```cpp
#include <vector>

std::vector<int> nextGreaterCircularBrute(const std::vector<int>& a) {
    const int n = static_cast<int>(a.size());
    std::vector<int> answer(n, -1);
    for (int i = 0; i < n; ++i) {
        for (int step = 1; step < n; ++step) {
            const int j = static_cast<int>((i + 1LL * step) % n);
            if (a[j] > a[i]) { answer[i] = a[j]; break; }
        }
    }
    return answer;
}
```

Usage: `{2,5,3}` returns `{5,-1,5}`. The loop examines each other occurrence in circular order, stopping at the nearest greater one. It does not visit the starting occurrence. Empty input performs no modulo operation. Auxiliary space O(1), output O(n).

Imagine concatenating the array with itself. Every circular search beginning in the first copy now appears as a forward search through the doubled sequence. The original stack method can process this sequence backward.

Crucially, the second copy is **conceptual**. We do not need to allocate or append it. Loop over virtual positions `2*n-1` down to 0, and read original data through modulo. The lecture first demonstrates the doubled sequence, then removes the physical-copy requirement when writing pseudocode.

## 3. Virtual indices and original dry run

**Lecture flow: approximately 08:34–17:11.** A virtual position k refers to original position `k % n`. Store original indices in the stack, so value comparisons use `a[stack.top()]`.

The lecture updates each original answer in both visits and overwrites preliminary values on the later visit. Our equivalent implementation writes answers only during the final, original-copy pass `k < n`; the first pass simply prepares suffix candidates.

**Original dry run:** input `[2,5,3]`; virtual sequence `[2,5,3,2,5,3]`. Entries are original `index:value`, bottom → top.

| k | Original i | Value | Before | Popped | Candidate answer | After push |
|---|---|---|---|---|---|---|
| 5 | 2 | 3 | `[]` | None | Preliminary -1 | `[2:3]` |
| 4 | 1 | 5 | `[2:3]` | 2 | Preliminary -1 | `[1:5]` |
| 3 | 0 | 2 | `[1:5]` | None | Preliminary 5 | `[1:5,0:2]` |
| 2 | 2 | 3 | `[1:5,0:2]` | 0 | **5** | `[1:5,2:3]` |
| 1 | 1 | 5 | `[1:5,2:3]` | 2,1 | **-1** | `[1:5]` |
| 0 | 0 | 2 | `[1:5]` | None | **5** | `[1:5,0:2]` |

Final output: `[5,-1,5]`. At k=1, the copied occurrence of the same 5 is removed because equality is invalid; this prevents a self-match.

## 4. C++17 implementation

```cpp
#include <stack>
#include <vector>

std::vector<int> nextGreaterCircular(const std::vector<int>& a) {
    const int n = static_cast<int>(a.size());
    if (n == 0) return {}; // Avoid modulo by zero.
    std::vector<int> answer(n, -1);
    std::stack<int> candidates;
    for (long long k = 2LL * n - 1; k >= 0; --k) {
        const int i = static_cast<int>(k % n);
        while (!candidates.empty() && a[candidates.top()] <= a[i])
            candidates.pop();
        if (k < n && !candidates.empty()) answer[i] = a[candidates.top()];
        candidates.push(i);
    }
    return answer;
}
```

Usage: `nextGreaterCircular({2,5,3})` returns `{5,-1,5}`; `{7}` returns `{-1}`; `{4,4,4}` returns `{-1,-1,-1}`. A wide virtual index avoids overflow in `2*n`, although practical judge arrays are much smaller.

## 5. Correctness and complexity

The ordinary reverse next-greater algorithm finds the first larger value in the virtual suffix. For an original position i, all other original positions appear within its next n-1 virtual positions. Its own copied occurrence has equal value and cannot be an answer. Any virtual occurrence farther away repeats an original value already examined in the first circular lap. If that value were greater, its nearer occurrence would already have qualified. Thus the first greater answer in the doubled suffix is exactly the first circular greater answer.

The candidate domination proof from Lecture 69 still applies to virtual occurrences. Each virtual occurrence is pushed once and popped at most once; there are 2n visits. Total time is **O(n)**, auxiliary stack space **O(n)**, and output space **O(n)**. Two passes change the constant factor, not the asymptotic complexity.

**Additional refinement:** with strict candidate removal, equal-value candidates cannot coexist. The generic O(2n)=O(n) bound is sufficient; no second physical input array is required.

## 6. Pitfalls and revision

- Use modulo for virtual input positions; do not index the original array directly with k.
- Store and access stack indices consistently. Original indices are in `[0,n)`.
- Pop equality; otherwise a copied element can answer itself.
- Circular order after wrapping is still forward order, not a backward scan through the left prefix.
- One pass misses valid wraparound answers; indefinitely repeated passes are unnecessary.
- The `-1` value sentinel can also be a real value when negative data exists; use an index-returning variant if absence must be unambiguous.

**Interview/CP extension:** an alternative forward scan keeps unresolved indices and pushes each original index only during its first visit. That method resolves old queries when a larger value arrives. Its pop condition is `a[current] > a[pending.top()]`, reflecting a different stack role.

**Interview check:** explain the doubled-array reduction, why no allocation is needed, why only one circular lap matters, and how strict comparison prevents a self-match.

**Revision:** process a virtual doubled sequence; map by `%n`; apply ordinary next-greater logic; keep the final original-position answers.
