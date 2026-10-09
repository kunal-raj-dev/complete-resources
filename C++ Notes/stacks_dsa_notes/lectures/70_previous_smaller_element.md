# Lecture 70 — Previous Smaller Element

[Study index](../README.md) · [Previous: Next Greater](69_next_greater_element.md) · [Next: Min Stack](71_min_stack.md)

**Source:** [Previous Smaller Element lecture](https://www.youtube.com/watch?v=WnjUfBn9nZM). **Verification:** full auto-caption sequence reviewed; selected code frame checked. [Coverage record](../SOURCE_COVERAGE.md#lecture-70).

**Prerequisites:** the candidate-stack explanation and domination proof from Lecture 69.

## Contents

- [1. Define the target](#1-define-the-target)
- [2. Adapt the previous pattern](#2-adapt-the-previous-pattern)
- [3. Original dry run](#3-original-dry-run)
- [4. C++17 values and indices](#4-c17-values-and-indices)
- [5. Correctness and complexity](#5-correctness-and-complexity)
- [6. Interview/CP extension and revision](#6-interviewcp-extension-and-revision)

## 1. Define the target

**Lecture flow: approximately 00:33–01:47.** For each position i, find the **largest index j < i** such that `a[j] < a[i]`. Largest index means nearest on the left; return that element's value, or `-1` if no such element exists.

The lecture's `[3,1,0,8,6]` example produces `[-1,-1,-1,0,0]`. For 6, the nearer 8 is too large; 0 is the nearest valid smaller value. “Previous smaller” is not the minimum of the prefix. In `[1,4,6]`, the answer for 6 is **4**, not 1.

Strictly smaller excludes equality. For `[2,2,3]`, the second 2 has no previous smaller value; 3's nearest smaller is the second 2.

## 2. Adapt the previous pattern

**Lecture flow: approximately 01:47–04:39.** We need information from the left, so traverse **left to right**. The stack contains surviving previous candidates, and its top is the most recent candidate. Remove any top `>= current`, because it cannot be a strictly smaller answer.

After removal, either the stack is empty and the answer is `-1`, or its top supplies the nearest smaller value. Push the current value for future elements.

| Pattern | Candidate scan direction | Pop invalid candidates |
|---|---|---|
| Next greater | Right → left | `top <= current` |
| Previous smaller | Left → right | `top >= current` |

We changed both **which side is processed first** and **which values can answer the query**. LIFO still gives us the nearest surviving candidate.

## 3. Original dry run

Use `[5,2,2,6,4]`. Stack entries are values, bottom → top.

| i | Current | Stack before | Popped | Answer | Stack after push |
|---|---|---|---|---|---|
| 0 | 5 | `[]` | None | -1 | `[5]` |
| 1 | 2 | `[5]` | 5 | -1 | `[2]` |
| 2 | 2 | `[2]` | 2 | -1 | `[2]` |
| 3 | 6 | `[2]` | None | 2 | `[2,6]` |
| 4 | 4 | `[2,6]` | 6 | 2 | `[2,4]` |

Output: `[-1,-1,-1,2,2]`. For an index-returning version, the result is `[-1,-1,-1,2,2]` too, coincidentally: the useful value 2 sits at index 2. Try `[8,3,7]` to expose the difference: values are `[-1,-1,3]`; indices are `[-1,-1,1]`.

## 4. C++17 values and indices

**Lecture flow: approximately 04:39–08:36.** The first function matches the lecture's value-returning problem. The index-returning function is an **Interview/CP extension** used for distances and histogram boundaries.

```cpp
#include <stack>
#include <vector>

std::vector<int> previousSmallerValues(const std::vector<int>& a) {
    const int n = static_cast<int>(a.size());
    std::vector<int> answer(n, -1);
    std::stack<int> candidates;
    for (int i = 0; i < n; ++i) {
        while (!candidates.empty() && candidates.top() >= a[i])
            candidates.pop();
        if (!candidates.empty()) answer[i] = candidates.top();
        candidates.push(a[i]);
    }
    return answer;
}

std::vector<int> previousSmallerIndices(const std::vector<int>& a) {
    const int n = static_cast<int>(a.size());
    std::vector<int> answer(n, -1);
    std::stack<int> candidates;
    for (int i = 0; i < n; ++i) {
        while (!candidates.empty() && a[candidates.top()] >= a[i])
            candidates.pop();
        if (!candidates.empty()) answer[i] = candidates.top();
        candidates.push(i);
    }
    return answer;
}
```

Usage: `previousSmallerValues({8,3,7})` returns `{-1,-1,3}`. `previousSmallerIndices` on the same input returns `{-1,-1,1}`. Both return an empty vector for empty input.

When a stack holds indices, compare **`a[top]`**, not top itself. Return top when the requested answer is an index; return `a[top]` when it is a value. State this distinction before coding.

## 5. Correctness and complexity

**Invariant:** surviving indices increase from bottom to top, and their values strictly increase. Any greater or equal top is removed before the current value is pushed, preserving strict increase.

Suppose older y is popped by newer x because `y >= x`. For a future target z:

- If `z > x`, x is a valid smaller candidate and is nearer than y.
- If `z <= x`, then y is not strictly smaller than z either.

So y can never again be the nearest smaller answer. Once invalid candidates are popped, the top is the closest surviving valid one. This is the smaller-value mirror of Lecture 69's domination proof.

**Lecture analysis: approximately 08:36–09:10.** Each occurrence is pushed once and popped at most once. Total time is O(n), auxiliary space O(n), output space O(n). An increasing array keeps many candidates alive; a decreasing array repeatedly pops and can have a very small live stack. Both take linear total time.

## 6. Interview/CP extension and revision

For [CSES Nearest Smaller Values](https://cses.fi/problemset/task/1645), output **1-based positions**, and output **0** for absence. Convert a zero-based index result p with `p+1`: `-1` becomes 0 automatically. The CSES limit is 200,000 elements, so a quadratic scan is unsuitable.

For `[8,3,7]`, internal indices `[-1,-1,1]` become CSES positions `[0,0,2]`. Do not return the smaller values themselves to that judge.

**Pitfalls:** forgetting equality in the pop condition; searching the right side; using the smallest historical value instead of the nearest; mixing 0-based sentinels with 1-based output; and pushing before answering.

If negative values are allowed, a value answer of `-1` can be a real smaller value as well as the absence marker. For unambiguous downstream logic, use the index result. Do not make a blanket statement that all negative answers mean absence.

**Interview check:** derive next smaller by changing only direction; derive previous greater by changing only comparison. Explain why the most recent equal candidate can replace the old equal candidate.

**Revision:** left-to-right scan; discard `>= current`; remaining top is previous strictly smaller; push current.
