# Lecture 74 — Trapping Rainwater

[Topic Index](./00_master_index.md) · [Previous: Circular Next Greater](./08_next_greater_element_ii.md) · [Next: Celebrity](./10_the_celebrity_problem.md)

**Source:** [Lecture 74](https://www.youtube.com/watch?v=UHHp8USwx4M). **Verification:** full auto-caption sequence reviewed; two-pointer update and branch logic visually checked. [Coverage record](../stacks_dsa_notes/SOURCE_COVERAGE.md#lecture-74).

**Prerequisites:** arrays, maxima, prefixes/suffixes, and two-pointer traversal. The main lecture solutions do not require a stack.

## Contents

- [1. Derive the water formula](#1-derive-the-water-formula)
- [2. Approach one — repeated boundary scans](#2-approach-one--repeated-boundary-scans)
- [3. Approach two — prefix and suffix maxima](#3-approach-two--prefix-and-suffix-maxima)
- [4. Approach three — two pointers](#4-approach-three--two-pointers)
- [5. Why the two-pointer decision is safe](#5-why-the-two-pointer-decision-is-safe)
- [6. Interview/CP extension — a stack solution](#6-interviewcp-extension--a-stack-solution)
- [7. Complexity, pitfalls, and revision](#7-complexity-pitfalls-and-revision)

## 1. Derive the water formula

**Lecture flow: approximately 00:32–07:20.** Each nonnegative height is a solid bar of width one. Water above a bar needs containment on both sides and spills over the lower boundary. The [official LeetCode 42 statement](https://leetcode.com/problems/trapping-rain-water/) asks for the total trapped amount; input has at most 20,000 bars and heights at most 100,000.

For i, let `L[i]` be the maximum height from 0 through i, and `R[i]` the maximum from i through n-1. Include the current bar in both maxima. Then:

```text
water level at i = min(L[i], R[i])
water above i    = min(L[i], R[i]) - height[i]
total           = sum over all positions
```

Because both maxima include the current bar, the difference cannot be negative. If you instead use maxima strictly outside the bar, you must clamp the difference to at least zero and carefully handle missing boundaries.

The lecture's `[4,2,0,3,2,5]` checkpoint has water amounts `[0,2,4,1,2,0]`, summing to 9. The end bars contribute zero because the water can escape outward.

**Important distinction from histogram:** the histogram asks for **one rectangle's maximum area**; rainwater sums separate water contributions. For rainwater, seek the highest boundary on each side, not the nearest smaller boundary.

## 2. Approach one — repeated boundary scans

**Lecture flow: approximately 07:20–08:28.** For each index, scan left to find the maximum and scan right to find the maximum, then apply the formula. The lecture describes this naive method briefly; the independently authored baseline below supports testing.

```cpp
#include <algorithm>
#include <vector>

long long trapBrute(const std::vector<int>& height) {
    const int n = static_cast<int>(height.size());
    long long answer = 0;
    for (int i = 0; i < n; ++i) {
        int leftMax = height[i], rightMax = height[i];
        for (int j = 0; j < i; ++j) leftMax = std::max(leftMax, height[j]);
        for (int j = i + 1; j < n; ++j) rightMax = std::max(rightMax, height[j]);
        answer += std::min(leftMax, rightMax) - height[i];
    }
    return answer;
}
```

Time O(n²), auxiliary space O(1), result space O(1). There are no nested water cells to simulate: compute each bar's contribution directly.

## 3. Approach two — prefix and suffix maxima

**Lecture flow: approximately 08:28–16:58.** Neighboring queries repeat the same maximum calculations. Compute and retain all prefix and suffix maxima once:

```text
L[0]   = height[0]
L[i]   = max(L[i-1], height[i])
R[n-1] = height[n-1]
R[i]   = max(R[i+1], height[i])
```

Build L left to right; build R right to left; sum the water formula in a third pass. The lecture calls this its prefix-array approach; the right array is specifically a suffix maximum array.

**Original dry run:** `[3,0,2,0,4]`.

| i | Height | L[i] | R[i] | Water level | Water above bar |
|---|---|---|---|---|---|
| 0 | 3 | 3 | 4 | 3 | 0 |
| 1 | 0 | 3 | 4 | 3 | 3 |
| 2 | 2 | 3 | 4 | 3 | 1 |
| 3 | 0 | 3 | 4 | 3 | 3 |
| 4 | 4 | 4 | 4 | 4 | 0 |

Total is **7**. A boundary height describes a water **level**, not water alone; subtract the solid bar's height to get the actual amount.

```cpp
#include <algorithm>
#include <vector>

long long trapPrefix(const std::vector<int>& height) {
    const int n = static_cast<int>(height.size());
    if (n == 0) return 0;
    std::vector<int> left(n), right(n);
    left[0] = height[0];
    right[n - 1] = height[n - 1];
    for (int i = 1; i < n; ++i)
        left[i] = std::max(left[i - 1], height[i]);
    for (int i = n - 2; i >= 0; --i)
        right[i] = std::max(right[i + 1], height[i]);
    long long answer = 0;
    for (int i = 0; i < n; ++i)
        answer += std::min(left[i], right[i]) - height[i];
    return answer;
}
```

Usage: `trapPrefix({3,0,2,0,4})` returns 7. The empty-input guard comes before array indexing. Time O(n), auxiliary space O(n), result space O(1).

## 4. Approach three — two pointers

**Lecture flow: approximately 16:58–21:49, with dry run/code at 26:20–29:50.** Maintain `left`, `right`, `leftMax`, and `rightMax`, rather than retaining two arrays. Update both maxima from the current endpoints. Process the side whose known maximum is smaller, then move that side inward.

```cpp
#include <algorithm>
#include <vector>

long long trapTwoPointers(const std::vector<int>& height) {
    const int n = static_cast<int>(height.size());
    int left = 0, right = n - 1;
    int leftMax = 0, rightMax = 0;
    long long answer = 0;
    while (left < right) {
        leftMax = std::max(leftMax, height[left]);
        rightMax = std::max(rightMax, height[right]);
        if (leftMax < rightMax) {
            answer += leftMax - height[left];
            ++left;
        } else {
            answer += rightMax - height[right];
            --right;
        }
    }
    return answer;
}
```

This follows the lecture's **maximum-comparison** version. Other valid implementations compare endpoint heights or use `left <= right`; their invariants differ. Understand one complete version before mixing lines from different versions.

**Original pointer dry run:** `[3,0,2,0,4]`. Maxima are shown after the updates in that row.

| Left | Right | leftMax | rightMax | Processed position | Added water | Total |
|---|---|---|---|---|---|---|
| 0 | 4 | 3 | 4 | 0 | 0 | 0 |
| 1 | 4 | 3 | 4 | 1 | 3 | 3 |
| 2 | 4 | 3 | 4 | 2 | 1 | 4 |
| 3 | 4 | 3 | 4 | 3 | 3 | 7 |

Pointers meet at the rightmost maximum. Its contribution is zero, so the loop returns 7. With no bars or one bar, the loop never executes and returns 0.

## 5. Why the two-pointer decision is safe

**Lecture flow: approximately 21:49–26:20.** After updating the maxima, `leftMax` summarizes everything seen from the left through the current left position, and `rightMax` summarizes everything seen from the right through the current right position.

If `leftMax < rightMax`, the true right maximum for the current left position is **at least** `rightMax`, because that right-side wall is already known. Therefore the smaller limiting boundary is exactly `leftMax`. Any unseen tall bar can only make the right maximum even larger; an unseen short bar does not remove the wall already found. We can finalize `leftMax-height[left]` without knowing the entire middle.

The symmetric argument applies when `rightMax <= leftMax`: the right position is limited by its known right maximum. That also covers equality. Each step finalizes one position and never revisits it.

**Additional explanation for `left < right`:** the final meeting position is at a global maximum. If a lower meeting bar had a taller processed wall on both sides, the side retaining the larger maximum could not have advanced past its taller wall under the smaller-maximum rule. Thus the unprocessed meeting bar contributes zero. A `<=` version can explicitly process the last zero contribution instead; either is correct when used consistently.

## 6. Interview/CP extension — a stack solution

This method is additional material, not one of the three approaches taught in the lecture. A decreasing stack holds unresolved bar indices. A higher incoming bar completes a basin above a popped bottom.

After popping bottom b, the new stack top is a left wall L, and current i is a right wall. The newly enclosed layer has:

```text
width         = i - L - 1
layer height  = min(height[L], height[i]) - height[b]
added volume  = width * layer height
```

```cpp
#include <algorithm>
#include <stack>
#include <vector>

long long trapStack(const std::vector<int>& height) {
    std::stack<int> pending;
    long long answer = 0;
    for (int i = 0; i < static_cast<int>(height.size()); ++i) {
        while (!pending.empty() && height[i] > height[pending.top()]) {
            const int bottom = pending.top();
            pending.pop();
            if (pending.empty()) break; // No left wall: no basin.
            const int left = pending.top();
            const long long width = i - left - 1LL;
            const int layer = std::min(height[left], height[i]) - height[bottom];
            answer += width * layer;
        }
        pending.push(i);
    }
    return answer;
}
```

For `[3,0,2,0,4]`, index 2 encloses a layer of height 2 over width 1, adding 2. Index 4 first encloses height 2 over width 1, adding 2; then height 1 over width 3, adding 3. Total `2+2+3=7`. Layers are vertically disjoint, so the layered accounting does not double-count the water already added.

Time O(n), auxiliary stack space O(n), result space O(1). The two-pointer method has the stronger O(1) auxiliary-space bound.

## 7. Complexity, pitfalls, and revision

| Method | Time | Auxiliary space | Main idea |
|---|---|---|---|
| Repeated maxima scans | O(n²) | O(1) | Apply the formula independently |
| Prefix/suffix maxima | O(n) | O(n) | Precompute boundaries |
| Two pointers | O(n) | O(1) | Finalize the side with the smaller known maximum |
| Stack extension | O(n) | O(n) | Complete horizontal basin layers |

- Never use nearest greater or smaller neighbors in place of the **maximum** boundary needed by the per-bar formula.
- Update maxima before subtracting to avoid negative contributions.
- A monotone increasing or decreasing array traps zero water; a large wall alone is insufficient.
- Keep heights nonnegative; these initial maxima of zero rely on that contract.
- Widen the accumulated total for broader CP limits. Current LeetCode limits fit signed 32-bit totals, but generic inputs may not.
- Do not move both pointers after accounting for only one endpoint.

**Interview check:** derive `min(leftMax,rightMax)-height`; explain why the larger unknown boundary is unnecessary; discuss prefix arrays as an easier-to-audit alternative; distinguish water layers from per-bar contributions.

**Revision:** lower of the two maximum walls limits water. Prefix arrays retain all maxima; two pointers retain only the maxima needed to settle the next endpoint.
