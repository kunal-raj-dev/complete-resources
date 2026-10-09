# Lecture 68 — Stock Span

[Topic Index](./00_master_index.md) · [Previous: Valid Parentheses](./02_valid_parentheses.md) · [Next: Next Greater Element](./04_next_greater_element.md)

**Source:** [Stock Span lecture](https://www.youtube.com/watch?v=01vBuZyMfqk). **Verification:** full auto-caption sequence reviewed; implementation frame checked. [Coverage record](../stacks_dsa_notes/SOURCE_COVERAGE.md#lecture-68).

**Prerequisites:** stack operations, array indices, and the meaning of consecutive days.

## Contents

- [1. Definition and consecutive-day examples](#1-definition-and-consecutive-day-examples)
- [2. Reframe the problem as previous greater](#2-reframe-the-problem-as-previous-greater)
- [3. Stack algorithm and dry run](#3-stack-algorithm-and-dry-run)
- [4. C++17 implementation](#4-c17-implementation)
- [5. Why popping is safe and why time is linear](#5-why-popping-is-safe-and-why-time-is-linear)
- [6. Interview/CP extension — online stock span](#6-interviewcp-extension--online-stock-span)
- [7. Pitfalls and revision](#7-pitfalls-and-revision)

## 1. Definition and consecutive-day examples

**Lecture flow: approximately 00:33–05:35.** For day i, its span counts the longest consecutive suffix ending at i whose prices are all **less than or equal to today's price**. Today's day is included, so a valid day's span is at least one.

The lecture illustrates the definition with `[100,80,60,70,60,75,85]`, producing `[1,1,1,2,1,4,6]`. Use this as a lecture checkpoint, then study the original example below.

For `[40,30,35,35,20,45]`, day 3 has price 35. Moving backward, include today's 35, the previous 35, and 30. Stop at 40. Span is **3**. Day 4's price 20 cannot reach the earlier 30 because the immediately preceding 35 blocks the consecutive run.

This is a counting problem over a **contiguous run**, not a count of every cheaper historical day. A price farther back can be small but irrelevant after a blocking higher day.

## 2. Reframe the problem as previous greater

**Lecture flow: approximately 05:35–10:52.** Instead of counting eligible days repeatedly, find the **nearest earlier strictly greater price**. The lecture calls this the *previous high*. This is not the maximum historical price; it is the nearest blocking position.

Let p be its index. Days `p+1` through i are all eligible, so:

```text
span[i] = i - p
if no earlier greater price exists: p = -1, so span[i] = i + 1
```

Store **indices**, because the answer needs a distance between days. Price values alone cannot tell you that distance. Once an index is known, its price is still available as `prices[index]`.

**Additional clarification:** no previous greater price means all earlier prices are at most today's price. It does **not** require the entire history to be increasing. In `[7,3,6,8]`, the final span is four although the history has dips.

## 3. Stack algorithm and dry run

**Lecture flow: approximately 10:52–22:42.** Maintain candidate indices with **strictly decreasing prices from bottom to top**. Traverse left to right.

1. Pop indices whose price is `<= prices[i]`: they do not block today's span.
2. The remaining top is the nearest previous strictly greater position, if one exists.
3. Calculate `i - top`, or `i+1` if the stack is empty.
4. Push i for future days.

**Original dry run:** prices `[40,30,35,35,20,45]`. Entries are `index:price`, bottom → top.

| i | Price | Stack before | Popped indices | Previous greater p | Span | Stack after push |
|---|---|---|---|---|---|---|
| 0 | 40 | `[]` | None | -1 | 1 | `[0:40]` |
| 1 | 30 | `[0:40]` | None | 0 | 1 | `[0:40,1:30]` |
| 2 | 35 | `[0:40,1:30]` | 1 | 0 | 2 | `[0:40,2:35]` |
| 3 | 35 | `[0:40,2:35]` | 2 | 0 | 3 | `[0:40,3:35]` |
| 4 | 20 | `[0:40,3:35]` | None | 3 | 1 | `[0:40,3:35,4:20]` |
| 5 | 45 | `[0:40,3:35,4:20]` | 4,3,0 | -1 | 6 | `[5:45]` |

Output is `[1,1,2,3,1,6]`. The equal price at day 3 must pop day 2; equality is part of the span, not a stopping condition.

## 4. C++17 implementation

**Lecture flow: approximately 22:42–24:57.** `stockSpan` returns one span per input day; the input is preserved. The baseline below is **additional explanation** for validating the optimized method, rather than a separate coded approach taught in this lecture.

```cpp
#include <stack>
#include <vector>

std::vector<int> stockSpanBrute(const std::vector<int>& prices) {
    const int n = static_cast<int>(prices.size());
    std::vector<int> answer(n, 1);
    for (int i = 0; i < n; ++i) {
        int j = i - 1;
        while (j >= 0 && prices[j] <= prices[i]) {
            ++answer[i];
            --j;
        }
    }
    return answer;
}

std::vector<int> stockSpan(const std::vector<int>& prices) {
    const int n = static_cast<int>(prices.size());
    std::vector<int> answer(n);
    std::stack<int> candidates;
    for (int i = 0; i < n; ++i) {
        while (!candidates.empty() && prices[candidates.top()] <= prices[i])
            candidates.pop();
        answer[i] = candidates.empty() ? i + 1 : i - candidates.top();
        candidates.push(i);
    }
    return answer;
}
```

Usage: `stockSpan({40,30,35,35,20,45})` returns `{1,1,2,3,1,6}`; an empty vector returns an empty result. Indices and spans are `int`; this pack assumes input lengths fit in `int`, as the referenced judge constraints do.

## 5. Why popping is safe and why time is linear

Suppose an older day j is popped by today's day i because `prices[j] <= prices[i]`. For any future price x:

- If x is at least today's price, neither j nor i is a greater-price blocker. A later intervening day may stop the span sooner, but j still cannot be its blocker.
- If x is below today's price, day i is a closer blocking day than j, so j cannot be the nearest blocker.

Thus j can never again be the nearest previous greater candidate. The stack retains only the useful frontier of history.

**Invariant:** candidate indices increase from bottom to top; their prices strictly decrease. After the popping step, the top is the nearest earlier price greater than the current price. Every skipped newer day has price at most the current one.

**Lecture analysis: approximately 24:57–26:08.** The outer loop visits n days. Every index is pushed once and popped at most once. Total work is O(n), even though one day can pop O(n) items. This is **amortized analysis**, not multiplication of the two loops' visible bounds.

| Method | Total time | Auxiliary space | Output space |
|---|---|---|---|
| Scan backward for each day | O(n²) worst case | O(1) | O(n) |
| Monotonic stack | O(n) | O(n) | O(n) |

The worst-case stack size occurs on decreasing prices, where every day remains a candidate. Increasing/equal prices may use little live stack space but still require scanning all n inputs.

## 6. Interview/CP extension — online stock span

The [official Online Stock Span problem](https://leetcode.com/problems/online-stock-span/) receives one price per `next(price)` call rather than an entire array. Store `(price, accumulated span)` so a popped block contributes its full length.

```cpp
#include <stack>
#include <utility>

class StockSpanner {
    std::stack<std::pair<int, int>> blocks;
public:
    int next(int price) {
        int span = 1;
        while (!blocks.empty() && blocks.top().first <= price) {
            span += blocks.top().second;
            blocks.pop();
        }
        blocks.push({price, span});
        return span;
    }
};
```

For calls `40,30,35,35`, blocks progress as `[(40,1)]`, `[(40,1),(30,1)]`, `[(40,1),(35,2)]`, `[(40,1),(35,3)]`. Span values are `1,1,2,3`. Each block represents a consecutive merged group ending at that stored price.

One `next` may take O(k); over k calls total time is O(k), or amortized O(1) per call. Live storage is O(k). The judge allows at most 10,000 calls, so `int` spans fit. For a longer stream, choose a sufficiently wide span type.

## 7. Pitfalls and revision

- Pop on `<=`, not `<`; `[5,5]` must produce `[1,2]`.
- Compare `prices[candidates.top()]`, not the stored index itself.
- Push after finding today's blocker, otherwise the current day can become its own blocker.
- Include today's day; span is not merely the number of earlier eligible days.
- The previous greater position is nearest by **position**, not greatest by price.

**Interview check:** explain the formula, why an old candidate can be discarded forever, and why one expensive day does not make total time quadratic. Convert the array approach to the streaming class without retaining every historical price.

**Revision:** scan left to right; remove prices `<= current`; span is distance to the remaining top, or `i+1` when none exists.
