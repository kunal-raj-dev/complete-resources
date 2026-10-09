# Practice roadmap

[Study index](../README.md) · [Interview questions](interview_questions.md) · [Quick revision](quick_revision.md)

**Scope:** Interview/CP practice beyond the lecture explanations. Problem titles, destination links, and LeetCode difficulty labels were checked against official pages on **2026-10-09**. CSES has no comparable official Easy/Medium/Hard label. These are exercises; keep the notes closed for the first attempt.

## Contents

- [1. Suggested order](#1-suggested-order)
- [2. Progressive hints](#2-progressive-hints)
- [3. Implementation drills](#3-implementation-drills)
- [4. A repeatable practice routine](#4-a-repeatable-practice-routine)
- [5. Readiness checkpoints](#5-readiness-checkpoints)

## 1. Suggested order

| Stage | Official problem | Difficulty | Pattern | Notes to review after attempting |
|---|---|---|---|---|
| 1 | [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Easy | Latest unmatched opener | [67](../lectures/67_valid_parentheses.md) |
| 1 | [150. Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | Medium | Expression value stack | [Evaluation](additional_stack_applications.md#1-postfix-expression-evaluation) |
| 1 | [232. Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) | Easy | Lazy reversal | [Queue](additional_stack_applications.md#6-queue-using-two-stacks) |
| 2 | [155. Min Stack](https://leetcode.com/problems/min-stack/) | Medium | Reversible minimum history | [71](../lectures/71_min_stack.md) |
| 2 | [496. Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) | Easy | Precompute nearest greater; queries | [69](../lectures/69_next_greater_element.md) |
| 2 | [CSES: Nearest Smaller Values](https://cses.fi/problemset/task/1645) | CP indexing drill | Previous strictly smaller index | [70](../lectures/70_previous_smaller_element.md) |
| 2 | [901. Online Stock Span](https://leetcode.com/problems/online-stock-span/) | Medium | Merge dominated blocks | [68](../lectures/68_stock_span.md) |
| 2 | [739. Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Medium | Resolve waiting indices with distance | [Forward pattern](monotonic_stack_patterns.md#5-the-unresolved-index-alternative) |
| 3 | [503. Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) | Medium | Circular virtual traversal | [73](../lectures/73_next_greater_element_ii.md) |
| 3 | [735. Asteroid Collision](https://leetcode.com/problems/asteroid-collision/) | Medium | Survivor simulation | [Simulation](additional_stack_applications.md#3-stack-based-simulation) |
| 3 | [402. Remove K Digits](https://leetcode.com/problems/remove-k-digits/) | Medium | Greedy deletions | [Digit removal](additional_stack_applications.md#4-greedy-digit-removal) |
| 4 | [84. Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Hard | Smaller blockers, widths | [72](../lectures/72_largest_rectangle_in_histogram.md) |
| 4 | [42. Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Hard | Boundary maxima, two pointers | [74](../lectures/74_trapping_rainwater.md) |
| 4 | [85. Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | Hard | Row-wise histogram reduction | [Matrix reduction](additional_stack_applications.md#7-maximal-rectangle-in-a-binary-matrix) |
| 5 | [907. Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/) | Medium | Contribution ownership | [Contributions](additional_stack_applications.md#8-subarray-contributions) |
| 5 | [2104. Sum of Subarray Ranges](https://leetcode.com/problems/sum-of-subarray-ranges/) | Medium | Maxima minus minima contributions | [Contributions](additional_stack_applications.md#8-subarray-contributions) |

Celebrity has a useful [lecture-backed implementation drill](../lectures/75_celebrity_problem.md). Implement both the stack and constant-space forms against the stated matrix contract, then generate inputs with no celebrity. Its absence from the table avoids claiming a third-party judge's interface or diagonal convention is identical to this lecture.

Difficulty labels describe the official problem, not the order you personally must learn it. For example, pair-based min-stack is often simpler to understand than some Easy query-interface details. Learn the invariant before optimizing constants.

## 2. Progressive hints

Open one level at a time. Try at least a concrete trace after each hint before revealing the next. Fully worked examples belong in the linked notes rather than here.

### Valid parentheses

<details><summary>Hint 1: what information do counts lose?</summary>

Construct two strings with identical counts but different nesting. Ask which opening bracket a closing bracket is allowed to match.

</details>
<details><summary>Hint 2: choose the state</summary>

Keep unmatched opening brackets. The most recent one determines the next permissible closing type.

</details>
<details><summary>Hint 3: complete all rejection conditions</summary>

Reject an early closer or mismatched top. Also reject leftover opening brackets after the scan.

</details>

### Neighbor queries, temperatures, and stock span

<details><summary>Hint 1: write the slow solution first</summary>

For each position, scan toward the desired answer. Specify whether equality qualifies, and stop at the first valid item.

</details>
<details><summary>Hint 2: decide what an entry represents</summary>

Previous queries can scan left to right with a stack of candidate indices. Next queries can scan backward with candidates, or forward with unresolved positions.

</details>
<details><summary>Hint 3: derive the comparison from the meaning</summary>

Stock span removes prices less than or equal to current. Temperatures need indices because the result is a distance; equal temperatures cannot resolve a strictly warmer query. CSES expects one-based positions with zero for absence.

</details>

### Min stack

<details><summary>Hint 1: why does the global minimum fail?</summary>

Push a new minimum, then pop it. What information would restore the previous minimum without scanning?

</details>
<details><summary>Hint 2: start with the simpler design</summary>

Save a prefix minimum beside every pushed value. Pop reveals the previous prefix's saved minimum.

</details>
<details><summary>Hint 3: challenge the optimized design</summary>

Try repeated minima and extreme integer values. If using an encoding, derive both the marker inequality and inverse formula before coding.

</details>

### Circular next greater

<details><summary>Hint 1: describe the legal search order</summary>

For one element, inspect later positions, wrap to the start, and stop before returning to the same occurrence.

</details>
<details><summary>Hint 2: avoid copying the array</summary>

A virtual doubled traversal can map each position back with modulo n. Retain the ordinary strict next-greater comparison.

</details>
<details><summary>Hint 3: test self-matches</summary>

Try one value and an all-equal array. Every answer should be absent. In reverse scanning, equal candidates must be removed.

</details>

### Simulation and greedy deletion

<details><summary>Hint 1: identify the next local interaction</summary>

For collision, ask which adjacent directions can approach each other. For digit removal, ask whether deleting the last kept digit improves an earlier position.

</details>
<details><summary>Hint 2: allow repeated resolution</summary>

One asteroid can destroy several prior survivors. One small digit can justify several deletions, limited by the remaining budget.

</details>
<details><summary>Hint 3: handle the leftover state</summary>

An equal asteroid pair destroys both. For a nondecreasing digit sequence with unused deletions, remove from the end, then normalize leading zeros.

</details>

### Histogram and maximal rectangle

<details><summary>Hint 1: fix the rectangle height</summary>

If a bar supplies the limiting height, how far can a rectangle extend before meeting a lower bar?

</details>
<details><summary>Hint 2: derive width with imaginary boundaries</summary>

Use smaller blockers at L and R; count indices strictly between them. Missing boundaries lie just outside the array.

</details>
<details><summary>Hint 3: lift the one-dimensional solution</summary>

For a binary matrix, accumulate consecutive vertical 1s ending at each row. Every rectangle has some bottom row.

</details>

### Rainwater

<details><summary>Hint 1: separate water level from water volume</summary>

At each bar, find the tallest wall available on each side. The lower one limits the level; subtract the bar itself.

</details>
<details><summary>Hint 2: remove repeated scans</summary>

Compute prefix and suffix maxima once. Derive this version before reducing storage.

</details>
<details><summary>Hint 3: explain which side can be finalized</summary>

If one known maximum is smaller, an already known wall on the opposite side proves sufficient containment. Unknown middle bars cannot erase that wall.

</details>

### Contribution sums

<details><summary>Hint 1: reverse the counting question</summary>

Count how many subarrays choose a particular index as their minimum instead of computing each subarray separately.

</details>
<details><summary>Hint 2: make duplicate ownership explicit</summary>

Pick the rightmost or leftmost minimum. One boundary comparison must be strict and the other non-strict.

</details>
<details><summary>Hint 3: multiply independent choices safely</summary>

Count permissible starts and ends. Multiply by the value using sufficiently wide arithmetic. Ranges can be split into total maximum contribution minus total minimum contribution.

</details>

## 3. Implementation drills

These exercises have no ready-made judge wrapper here. Use the input contracts in the notes and write your own checks.

- Implement fixed-capacity and node-based stacks; test underflow, capacity zero, capacity full, and object destruction. Explain copying policy.
- Implement all eight nearest-neighbor variants with indices. Compare each against a direct scan on random small arrays.
- Rewrite reverse next greater as forward waiting indices, then explain why the pop conditions differ.
- Implement stock span from a full array and as an online stream; compare every stream prefix with the array answer.
- Implement celebrity with a stack and with one candidate; test diagonal 0 and 1, one person, and no candidate satisfying both conditions.
- Write iterative DFS with explicit resume frames and compare its entry order to recursive DFS on a graph with cross edges.
- Convert tokenized infix to postfix, then evaluate it. Include subtraction and division to catch operand-order mistakes.

## 4. A repeatable practice routine

1. State the contract and construct a small example yourself.
2. Write a brute-force baseline and its time/space bounds.
3. Describe the optimized stack invariant in one sentence.
4. Derive strictness, scan direction, sentinel, and index formula before coding.
5. Test one empty/singleton case where allowed, duplicates, monotone input, and a missing-answer case.
6. Compare with the baseline on small randomized inputs.
7. Explain correctness aloud; write the exact mistake that would have broken your solution.

Revisit a problem after a day, several days, and about a week if useful. Reimplement from its invariant, rather than memorizing lines. A problem is learned when you can transfer the reasoning to a changed comparison or output interface.

## 5. Readiness checkpoints

**Foundations:** write a guarded stack, bracket validator, and RPN evaluator; explain LIFO and operand order.

**Monotonic patterns:** derive all eight candidate rules, explain forward versus reverse next greater, and prove total linear work.

**Boundaries:** derive histogram width, handle equal heights, and explain the flush step. Solve the row-wise matrix reduction.

**Advanced reasoning:** justify two-pointer rainwater, celebrity's final verification, encoded minimum restoration, and asymmetric contribution ownership.

**CP readiness:** adapt one-based output, choose wide arithmetic from constraints, avoid unsigned reverse-loop underflow, and validate against a brute oracle. Time limits and platform constraints should be checked on the linked problem page when submitting.
