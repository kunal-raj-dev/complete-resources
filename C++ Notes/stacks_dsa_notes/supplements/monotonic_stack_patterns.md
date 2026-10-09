# Monotonic stack patterns

[Study index](../README.md) · [Applications](additional_stack_applications.md) · [Practice](practice_roadmap.md) · [Quick revision](quick_revision.md)

**Scope:** Interview/CP extension synthesizing Lectures [68](../lectures/68_stock_span.md), [69](../lectures/69_next_greater_element.md), [70](../lectures/70_previous_smaller_element.md), [72](../lectures/72_largest_rectangle_in_histogram.md), and [73](../lectures/73_next_greater_element_ii.md). This is additional material, not a claim that every variant was taught in those videos.

**Prerequisites:** arrays, zero-based indices, stack operations, and inequalities. All stack displays run **bottom → top**.

## Contents

- [1. Recognize the problem](#1-recognize-the-problem)
- [2. Candidate stacks and scan direction](#2-candidate-stacks-and-scan-direction)
- [3. All eight comparison rules](#3-all-eight-comparison-rules)
- [4. A reusable C++17 boundary template](#4-a-reusable-c17-boundary-template)
- [5. The unresolved-index alternative](#5-the-unresolved-index-alternative)
- [6. Why nested popping is linear](#6-why-nested-popping-is-linear)
- [7. Duplicates and ownership](#7-duplicates-and-ownership)
- [8. Choose the right representation](#8-choose-the-right-representation)

## 1. Recognize the problem

A monotonic stack keeps its entries ordered by value while preserving useful positional information. It is useful when a question asks for the **nearest** previous/next item meeting a comparison, or for the interval over which an item remains a minimum/maximum.

For `[5,2,2,7]`, the previous **strictly smaller** index for the second 2 is absent: equality does not qualify. Its previous **smaller-or-equal** index is 1. Changing one comparison changes the answer and the stack invariant.

Nearest means minimum positional distance in the specified direction. It does not mean smallest numerical difference, greatest value, or any qualifying element. Sorting is generally unsuitable because it destroys this positional order.

## 2. Candidate stacks and scan direction

In the candidate-stack version, the stack contains possible answers from the already scanned side. Choose the scan so that this side is available:

| Query | Scan | Answer after removing invalid candidates |
|---|---|---|
| Previous qualifying item | Left → right | Remaining top |
| Next qualifying item | Right → left | Remaining top |

Before pushing the current index, pop entries that fail the desired relationship with the current value. Then read the answer, then push the current index. Reading **before** pushing prevents the current index from answering its own query.

Why can we discard an entry permanently? For previous strictly smaller, suppose older value y is popped by newer x because `y >= x`. For a future value z, if y is smaller than z, x is also smaller and lies closer. If y is not smaller than z, it cannot answer that query anyway. The reverse-scan proof is symmetric. Greater queries reverse the inequalities. Non-strict variants pop only strictly invalid values, so equal candidates remain available.

**Worked example:** previous strictly smaller indices for `[4,2,2,5,1]`. Stack entries below are `index:value`.

| i | Value | Pops | Answer index | Stack after push |
|---|---|---|---|---|
| 0 | 4 | None | -1 | `[0:4]` |
| 1 | 2 | `0:4` | -1 | `[1:2]` |
| 2 | 2 | `1:2` | -1 | `[2:2]` |
| 3 | 5 | None | 2 | `[2:2,3:5]` |
| 4 | 1 | `3:5,2:2` | -1 | `[4:1]` |

Output `[-1,-1,-1,2,-1]`. If the query is smaller-or-equal instead, index 2 keeps the equal 2 at index 1, and the output is `[-1,-1,1,2,-1]`.

## 3. All eight comparison rules

These rules apply to **scan, pop invalid candidates, read top, push current**. Compare `a[top]` with `a[i]`. They are not blindly transferable to a forward unresolved-index algorithm.

| Desired answer | Scan | Pop while | Values remaining bottom → top |
|---|---|---|---|
| Previous greater `>` | Left → right | `a[top] <= a[i]` | Strictly decreasing |
| Previous greater-or-equal `>=` | Left → right | `a[top] < a[i]` | Nonincreasing |
| Previous smaller `<` | Left → right | `a[top] >= a[i]` | Strictly increasing |
| Previous smaller-or-equal `<=` | Left → right | `a[top] > a[i]` | Nondecreasing |
| Next greater `>` | Right → left | `a[top] <= a[i]` | Strictly decreasing |
| Next greater-or-equal `>=` | Right → left | `a[top] < a[i]` | Nonincreasing |
| Next smaller `<` | Right → left | `a[top] >= a[i]` | Strictly increasing |
| Next smaller-or-equal `<=` | Right → left | `a[top] > a[i]` | Nondecreasing |

**Derive rather than memorize:** a strict greater answer must satisfy `candidate > current`. Its invalid complement is `candidate <= current`, so pop those entries.

## 4. A reusable C++17 boundary template

This returns **indices**, with -1 for absence on either side. Input size must fit `int`. `previous` selects direction; `smaller` selects the relationship; `strict` selects whether equality qualifies. Flags make the eight variants testable through one implementation; named wrappers may be clearer in an interview.

```cpp
#include <stack>
#include <vector>

std::vector<int> nearestIndices(const std::vector<int>& a,
                               bool previous, bool smaller, bool strict) {
    const int n = static_cast<int>(a.size());
    std::vector<int> answer(n, -1);
    std::stack<int> candidates;
    auto invalid = [&](int candidate, int current) {
        if (smaller) return strict ? candidate >= current : candidate > current;
        return strict ? candidate <= current : candidate < current;
    };
    const int step = previous ? 1 : -1;
    for (int i = previous ? 0 : n - 1; i >= 0 && i < n; i += step) {
        while (!candidates.empty() && invalid(a[candidates.top()], a[i]))
            candidates.pop();
        if (!candidates.empty()) answer[i] = candidates.top();
        candidates.push(i);
    }
    return answer;
}
```

Usage: `nearestIndices({4,2,2,5,1}, true, true, true)` returns `{-1,-1,-1,2,-1}`. Changing the final argument to false yields `{-1,-1,1,2,-1}`. For next greater, use `(a, false, false, true)`.

**Invariant:** entries are on the already scanned side and ordered according to the table. Popped entries are dominated by a closer entry for any later query. After the invalid entries disappear, the top is the nearest surviving valid candidate. Pushing preserves the invariant.

The generic template deliberately uses -1 for both missing sides. For histogram geometry, convert missing **right** answers to n before computing width. Absence encoding is an interface decision, not an inequality decision.

## 5. The unresolved-index alternative

Next-greater queries also support a **forward** scan. Here the stack holds indices still waiting for an answer, not ready-made candidates for the current position. When a larger current value arrives, it answers all smaller waiting entries that it pops.

```cpp
#include <stack>
#include <vector>

std::vector<int> nextGreaterForwardIndices(const std::vector<int>& a) {
    std::vector<int> answer(a.size(), -1);
    std::stack<int> waiting;
    for (int i = 0; i < static_cast<int>(a.size()); ++i) {
        while (!waiting.empty() && a[waiting.top()] < a[i]) {
            answer[waiting.top()] = i;
            waiting.pop();
        }
        waiting.push(i);
    }
    return answer;
}
```

For `[2,2,4]`, indices 0 and 1 both wait through the equal second 2; at index 2 both receive answer 2. Output `[2,2,-1]`. Compare this with reverse candidate scanning: **forward pops `<`, reverse pops `<=`** for the same strict next-greater problem, because popping performs different jobs.

Correctness: a waiting index has seen no greater item yet. The first greater item encountered resolves it immediately, so its answer is nearest. The nonincreasing waiting values allow all resolvable entries to appear at the top consecutively. Entries left at the end have no greater item. Time O(n), auxiliary space O(n), output O(n).

This formulation naturally solves waiting-time problems: assign `i-j` when index j is resolved, as in [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/).

## 6. Why nested popping is linear

For n input positions, there are exactly n pushes and at most n pops. An entry removed today cannot be removed again tomorrow. Loop overhead is O(n), so total work is O(n), even if one iteration pops the entire stack.

A potential argument says the same thing more formally. Let potential Φ be the number of stack entries. An iteration with k pops and one push has actual stack work `k+1` and potential change `1-k`. Its amortized stack work is `(k+1)+(1-k)=2`. Starting from an empty stack and ending with nonnegative potential bounds total actual work by O(n).

This does **not** mean every individual query has worst-case O(1) latency. Batch complexity is O(n); an online stock-span call may cost O(n) in the worst case but is amortized O(1) over calls.

## 7. Duplicates and ownership

There are two different duplicate questions:

1. **Is equality a valid answer?** For strict nearest smaller/greater, no. For smaller-or-equal/greater-or-equal, yes. The eight-rule table answers this.
2. **Who owns an interval with repeated minima?** For summing subarray contributions, choose one occurrence deterministically. Otherwise intervals can be counted twice or omitted.

For minima contributions, using previous **strictly smaller** and next **smaller-or-equal** assigns an interval to its **rightmost** minimum. Its rightmost equal minimum can extend left through equal values; an earlier equal minimum is stopped by a later equal value on the right. Swapping the strict side assigns ownership to the leftmost minimum instead.

For `[2,2]`, strict-left boundaries are `[-1,-1]`, non-strict-right boundaries are `[1,2]`. Counts `(i-L)*(R-i)` are 1 and 2: the three subarrays are owned exactly once. Strict on both sides would count the length-two interval twice. Non-strict on both sides would omit it.

Histogram is different: overlapping candidate rectangles are harmless because we take a **maximum**, not a sum. Strictly smaller boundaries on both sides correctly allow each equal bar to consider the full plateau. The [applications chapter](additional_stack_applications.md#8-subarray-contributions) develops contribution counting in detail.

## 8. Choose the right representation

| Need | Store | Convert answer using |
|---|---|---|
| Neighbor value only | Values can suffice | Top value |
| Distances/widths | Indices | `i-j` or `R-L-1` |
| Duplicate occurrence identity | Indices | Query the correct occurrence |
| Online stock span | `(price, merged span)` | Sum popped block spans + 1 |
| Circular neighbor | Original indices, virtual traversal | `virtualIndex % n` |

Keep the input unchanged while stack indices refer into it. Test all-equal data, monotone data, a singleton, negative values, and absence. A value sentinel -1 can be indistinguishable from a valid answer of value -1; use indices or `std::optional` when the interface must distinguish them.

**Revision:** define direction and strictness first; decide what popping accomplishes; choose values versus indices; prove domination; count each occurrence once; handle equality according to the problem's meaning.
