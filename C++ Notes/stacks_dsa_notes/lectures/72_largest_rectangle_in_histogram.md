# Lecture 72 — Largest Rectangle in a Histogram

[Study index](../README.md) · [Previous: Min Stack](71_min_stack.md) · [Next: Circular Next Greater](73_next_greater_element_ii.md)

**Source:** [Histogram lecture](https://www.youtube.com/watch?v=ysy1o-QEj3k). **Verification:** full auto-caption sequence reviewed; right-boundary correction and final code visually checked. [Coverage record](../SOURCE_COVERAGE.md#lecture-72).

**Prerequisites:** previous/next smaller elements, index stacks, contiguous ranges, and area = height × width.

## Contents

- [1. The rectangle problem](#1-the-rectangle-problem)
- [2. Brute force — enumerate intervals](#2-brute-force--enumerate-intervals)
- [3. Fix the limiting height and find its boundaries](#3-fix-the-limiting-height-and-find-its-boundaries)
- [4. Compute right smaller, then left smaller](#4-compute-right-smaller-then-left-smaller)
- [5. Correct the missing-right-boundary sentinel](#5-correct-the-missing-right-boundary-sentinel)
- [6. C++17 implementation](#6-c17-implementation)
- [7. Correctness, complexity, and lecture homework](#7-correctness-complexity-and-lecture-homework)
- [8. Interview/CP extension — one-pass stack](#8-interviewcp-extension--one-pass-stack)
- [9. Pitfalls and revision](#9-pitfalls-and-revision)

## 1. The rectangle problem

**Lecture flow: approximately 00:33–01:48.** Given nonnegative bar heights, each with width 1, find the largest rectangular area lying inside the histogram. A rectangle can cover adjacent bars but cannot rise above the shortest included bar. The [official LeetCode 84 statement](https://leetcode.com/problems/largest-rectangle-in-histogram/) allows up to 100,000 bars, each at most 10,000 high.

For an interval `[l,r]`, the tallest permitted rectangle has height `min(heights[l..r])` and width `r-l+1`. Bars need not all have the same height: taller bars can contribute their lower portions to a shorter rectangle.

The lecture's `[2,1,5,6,2,3]` checkpoint has answer 10: take the adjacent heights 5 and 6 at limiting height 5 and width 2.

## 2. Brute force — enumerate intervals

**Lecture flow: approximately 01:48–03:26.** Choose each start l and extend the endpoint r. Maintain the minimum height seen as the interval grows, and compare every interval area with the best so far.

There are `n(n+1)/2` nonempty intervals, so this implementation costs O(n²), not O(n³). Recomputing the interval minimum from scratch would introduce a third factor. The lecture discusses this baseline briefly and concentrates on the optimal approach.

```cpp
#include <algorithm>
#include <vector>

long long largestRectangleBrute(const std::vector<int>& heights) {
    const int n = static_cast<int>(heights.size());
    long long best = 0;
    for (int left = 0; left < n; ++left) {
        int minimum = heights[left];
        for (int right = left; right < n; ++right) {
            minimum = std::min(minimum, heights[right]);
            best = std::max(best, 1LL * minimum * (right - left + 1));
        }
    }
    return best;
}
```

For `[3,1,3,3]`, intervals starting at index 0 have areas 3, 2, 3, 4. The interval `[2,3]` has height 3 and width 2, producing the best area **6**.

## 3. Fix the limiting height and find its boundaries

**Lecture flow: approximately 03:26–11:49.** Instead of enumerating every interval, let each bar i define a candidate rectangle whose height is **fixed to `heights[i]`**. Extend left and right while bars are at least that high. Stop at the nearest **strictly smaller** bar on each side.

Let L[i] and R[i] be the positions of those blocking bars. They are **excluded** from the rectangle. The included range is `[L[i]+1, R[i]-1]`, so:

```text
width[i] = R[i] - L[i] - 1
area[i]  = heights[i] * width[i]
answer   = max over all area[i]
```

**Additional precision:** “largest rectangle for a bar” here means the largest rectangle **at that bar's height**. The best rectangle containing a tall bar may actually have a lower height. The algorithm remains complete because every optimal rectangle has at least one shortest bar that supplies its limiting height.

Equal heights do not block extension. In `[3,3]`, the full width is 2 and area is 6. Boundaries must therefore be strictly smaller; pop candidates on `>=` in each independent boundary scan.

## 4. Compute right smaller, then left smaller

**Lecture flow: approximately 11:49–26:48.** The explanation first calculates the **right nearest smaller index** by scanning right to left, then calculates the **left nearest smaller index** by scanning left to right. Both reuse the candidate-stack ideas from Lectures 69 and 70.

Store **indices**, because width depends on positions. Compare heights through those indices. After finishing the right scan, clear the stack before the left scan: the leftover suffix candidates are not valid previous candidates.

**Original boundary dry run:** `[3,1,3,3]`. Entries are `index:height`, bottom → top.

| Right scan i | Before | Popped | R[i] | After push |
|---|---|---|---|---|
| 3 | `[]` | None | 4 | `[3:3]` |
| 2 | `[3:3]` | 3 | 4 | `[2:3]` |
| 1 | `[2:3]` | 2 | 4 | `[1:1]` |
| 0 | `[1:1]` | None | 1 | `[1:1,0:3]` |

Clear the stack.

| Left scan i | Before | Popped | L[i] | After push |
|---|---|---|---|---|
| 0 | `[]` | None | -1 | `[0:3]` |
| 1 | `[0:3]` | 0 | -1 | `[1:1]` |
| 2 | `[1:1]` | None | 1 | `[1:1,2:3]` |
| 3 | `[1:1,2:3]` | 2 | 1 | `[1:1,3:3]` |

The final boundaries are L=`[-1,-1,1,1]`, R=`[1,4,4,4]`.

## 5. Correct the missing-right-boundary sentinel

**Lecture flow: approximately 27:30–30:00.** During the initial derivation, the lecture temporarily represents absent right neighbors by `-1`, then explicitly changes this for width calculations. The final right sentinel must be **n**, while the left sentinel stays **-1**.

These are imaginary blocking positions just outside the array. When neither blocker exists, width is `n-(-1)-1 = n`. Using `-1` on both sides makes width negative and breaks the geometry.

This is a **correction made inside the lecture**, not an unresolved error in the final solution. The final implementation below uses the corrected sentinel from the beginning. A spoken/caption slip near 29:23 still mentions `-1`; the final code's empty-right case uses n.

## 6. C++17 implementation

The helper returns `(left indices, right indices)` using the corrected sentinels. `largestRectangle` evaluates the candidate at each bar. Empty input returns 0 as an extension; the official problem is nonempty.

```cpp
#include <algorithm>
#include <stack>
#include <utility>
#include <vector>

std::pair<std::vector<int>, std::vector<int>>
histogramBounds(const std::vector<int>& heights) {
    const int n = static_cast<int>(heights.size());
    std::vector<int> left(n, -1), right(n, n);
    std::stack<int> candidates;
    for (int i = n - 1; i >= 0; --i) {
        while (!candidates.empty() && heights[candidates.top()] >= heights[i])
            candidates.pop();
        if (!candidates.empty()) right[i] = candidates.top();
        candidates.push(i);
    }
    while (!candidates.empty()) candidates.pop();
    for (int i = 0; i < n; ++i) {
        while (!candidates.empty() && heights[candidates.top()] >= heights[i])
            candidates.pop();
        if (!candidates.empty()) left[i] = candidates.top();
        candidates.push(i);
    }
    return {left, right};
}

long long largestRectangle(const std::vector<int>& heights) {
    const auto [left, right] = histogramBounds(heights);
    long long best = 0;
    for (int i = 0; i < static_cast<int>(heights.size()); ++i) {
        const long long width = right[i] - left[i] - 1LL;
        best = std::max(best, 1LL * heights[i] * width);
    }
    return best;
}
```

Usage: `largestRectangle({3,1,3,3})` returns 6. The return type is deliberately `long long` for broader CP inputs. Under LeetCode's checked limits, the maximum possible area is at most 10⁹, so converting the result to the judge's `int` return type is safe there.

## 7. Correctness, complexity, and lecture homework

Take any optimal rectangle. Its limiting height equals a shortest bar in its covered interval. The nearest strictly smaller boundaries around that bar cannot lie inside the interval, so the maximal interval computed for the bar contains the optimal interval. Extending to those boundaries cannot reduce area at the fixed nonnegative height. Our candidate is therefore at least as good. Every candidate is itself a valid rectangle, so the maximum candidate area equals the optimum.

Each boundary pass pushes each index once and pops it at most once. Clearing the stack is also O(n); the final area pass is O(n). Total time is **O(n)**, auxiliary space **O(n)**, and returned result space **O(1)**. The helper returns O(n) boundary arrays internally; the scalar solver retains them as working storage.

**Lecture homework: approximately 31:18–32:37.** Calculate every bar's area from the left/right index arrays. The lecture checkpoint is:

| i | Height | L | R after correction | Width | Area |
|---|---|---|---|---|---|
| 0 | 2 | -1 | 1 | 1 | 2 |
| 1 | 1 | -1 | 6 | 6 | 6 |
| 2 | 5 | 1 | 4 | 2 | 10 |
| 3 | 6 | 2 | 4 | 1 | 6 |
| 4 | 2 | 1 | 6 | 4 | 8 |
| 5 | 3 | 4 | 6 | 1 | 3 |

Verify the table yourself before using it as a solution check. For the original dry run, candidate areas are `[3,4,6,6]`, giving 6.

## 8. Interview/CP extension — one-pass stack

The lecture teaches the two-boundary-array approach. A further implementation computes areas when a bar is popped, avoiding the two arrays while still using O(n) stack space.

Maintain strictly increasing heights by index. A smaller or equal incoming height closes a stored bar's current interval. After removing that bar, the remaining top supplies its left blocker; the current index supplies the right endpoint. A final virtual iteration at i=n flushes everything.

```cpp
#include <algorithm>
#include <stack>
#include <vector>

long long largestRectangleOnePass(const std::vector<int>& heights) {
    const int n = static_cast<int>(heights.size());
    std::stack<int> pending;
    long long best = 0;
    for (int i = 0; i <= n; ++i) {
        while (!pending.empty() &&
               (i == n || heights[pending.top()] >= heights[i])) {
            const int bar = pending.top();
            pending.pop();
            const int left = pending.empty() ? -1 : pending.top();
            const long long width = i - left - 1LL;
            best = std::max(best, 1LL * heights[bar] * width);
        }
        if (i < n) pending.push(i);
    }
    return best;
}
```

The `i == n` check must come before `heights[i]` so short-circuiting prevents reading past the input. Do not push n as an actual bar.

**Equality nuance:** this one-pass variant may close an older equal-height bar before its full plateau width is seen. Its newer equal replacement inherits the left reach and eventually accounts for the full plateau. It finds the same maximum, but its per-pop widths are not necessarily the same as the two-sided strictly smaller boundary table.

## 9. Pitfalls and revision

- Width is `R-L-1`, because blockers are outside the rectangle.
- Equal bars must permit a rectangle to extend across them.
- Reset candidate state between independent passes.
- Widen multiplication before multiplying, not after an overflowed `int` result.
- The largest height alone is insufficient; width can compensate for a shorter height.
- In one pass, failure to flush misses rectangles ending at the final bar: `[2,3,4]` is a useful test.

**Interview check:** derive width from excluded boundaries; prove considering limiting bars is sufficient; explain why equal bars are handled differently in some one-pass implementations.

**Revision:** fix height at each bar, extend to strictly smaller blockers, use sentinels `-1,n`, maximize `height*(R-L-1)`.
