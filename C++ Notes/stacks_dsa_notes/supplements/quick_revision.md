# Quick revision: stacks

[Study index](../README.md) · [Patterns](monotonic_stack_patterns.md) · [Interview questions](interview_questions.md) · [Practice](practice_roadmap.md)

**Scope:** compact revision of Lectures 66–75 plus explicitly added interview/CP patterns. Read the full chapters for proofs. All indices below are zero-based; stacks run bottom → top; n is input length; output space is listed separately from auxiliary space.

## Contents

- [1. Core operations](#1-core-operations)
- [2. Neighbor comparison rules](#2-neighbor-comparison-rules)
- [3. Problem formulas and invariants](#3-problem-formulas-and-invariants)
- [4. Complexity table](#4-complexity-table)
- [5. Additional applications](#5-additional-applications)
- [6. Debugging checklist](#6-debugging-checklist)

## 1. Core operations

LIFO: latest surviving push is removed first. `top` reads, `pop` removes and returns void, `empty` guards access. Vector top is back; singly linked stack top is head. A vector push is amortized O(1), worst-case O(n) on growth; node insertion/removal has O(1) structural work. A fixed array must distinguish underflow from capacity overflow. [Lecture 66](../lectures/66_introduction_to_stacks.md).

Do not retain vector references across a potentially reallocating push. Raw owning nodes require a destructor and an explicit copying/moving policy. Runtime recursion also consumes stack memory.

## 2. Neighbor comparison rules

For a **candidate** stack: previous scans left → right, next scans right → left. Pop invalid top candidates, read the remaining top, then push current. Compare candidate with current:

| Wanted relationship | Pop while | Surviving order bottom → top |
|---|---|---|
| Strict greater `>` | `candidate <= current` | Strictly decreasing |
| Greater-or-equal `>=` | `candidate < current` | Nonincreasing |
| Strict smaller `<` | `candidate >= current` | Strictly increasing |
| Smaller-or-equal `<=` | `candidate > current` | Nondecreasing |

For **forward unresolved next greater**, pop waiting indices when `a[waiting] < a[current]` and assign their answer. Equality stays unresolved. This is a different pop role.

Linear proof: every occurrence is pushed once and popped at most once. One iteration may cost O(n); the whole traversal costs O(n). Use indices when distance, width, or occurrence identity matters. [Full patterns](monotonic_stack_patterns.md).

## 3. Problem formulas and invariants

| Topic | Key state / formula | Critical detail |
|---|---|---|
| [67: Brackets](../lectures/67_valid_parentheses.md) | Stack is exactly unmatched openers | Reject early closer, wrong top type, and leftover openers |
| [68: Stock span](../lectures/68_stock_span.md) | Previous greater p; `span=i-p`, absent p=-1 | Pop `<=`; today counts; days must be consecutive |
| [69: NGE](../lectures/69_next_greater_element.md) | Reverse decreasing candidate stack | Nearest strictly larger, not suffix maximum |
| [70: Previous smaller](../lectures/70_previous_smaller_element.md) | Forward increasing candidate stack | Pop `>=`; distinguish index from value |
| [71: Pair min-stack](../lectures/71_min_stack.md) | `(value, minimum of prefix)` | Pop restores prior prefix automatically |
| [71: Encoded min-stack](../lectures/71_min_stack.md) | New smaller x: `e=2*x-old`; marker if `stored<minimum` | Marker top returns minimum; pop restores `2*minimum-e` |
| [72: Histogram](../lectures/72_largest_rectangle_in_histogram.md) | Strict smaller blockers L,R; `width=R-L-1`; `area=height*width` | Missing L=-1, missing R=n; pop `>=` in both boundary passes |
| [73: Circular NGE](../lectures/73_next_greater_element_ii.md) | Reverse virtual positions `2n-1..0`, index `%n` | Prepare second copy; write original answers; pop `<=` |
| [74: Rainwater](../lectures/74_trapping_rainwater.md) | `min(prefixMax,suffixMax)-height` | Maxima include current; process smaller running maximum |
| [75: Celebrity](../lectures/75_celebrity_problem.md) | `knows(a,b)` eliminates a if 1, b if 0 | Survivor must pass incoming column + outgoing row; skip diagonal |

Encoded minima require arithmetic widened **before** doubling. Duplicate minima are stored normally when equal; a two-minimum-stack variant must retain equal minima occurrences. Both pair and encoded stacks use O(n) total storage.

Histogram one-pass extension computes a popped bar's area with right boundary=current index and left boundary=new top or -1. A virtual end iteration flushes remaining bars. Equal bars may pop, with the later equal bar eventually spanning the wider plateau.

Rainwater stack extension: after popping bottom b, if a left wall L remains, add `(i-L-1) * (min(h[L],h[i])-h[b])`. These are horizontal layers; avoid counting the full basin depth on every pop.

## 4. Complexity table

| Solver | Time | Auxiliary space | Output space |
|---|---|---|---|
| Bracket validation | O(n) | O(n) worst case | O(1) |
| Span / nearest neighbor array | O(n) | O(n) | O(n) |
| NGE I, n reference + m queries | Expected O(n+m) with hashing | O(n) | O(m) |
| Online span, k calls | O(k) total; amortized O(1)/call | O(k) live storage | O(1)/returned span |
| Pair / encoded min-stack | O(1) underlying stack work/operation | O(n) total stored state | O(1)/query |
| Histogram two-array / one-pass | O(n) | O(n) | O(1) |
| Circular NGE | O(n) | O(n) | O(n) |
| Rainwater repeated scans | O(n²) | O(1) | O(1) |
| Rainwater prefix / two-pointer / stack | O(n) each | O(n) / O(1) / O(n) | O(1) |
| Celebrity stack / scalar candidate | O(n) lookups | O(n) / O(1) | O(1) |

Celebrity excludes already stored O(n²) matrix input and its reading cost. Hashing has expected bounds; a balanced ordered map gives deterministic O(log n) operations. Stateful storage is the space of the data structure, not extra output memory.

## 5. Additional applications

See [complete explanations and templates](additional_stack_applications.md).

| Application | Remember |
|---|---|
| Postfix evaluation | Pop right, then left; apply `left op right`; division truncates toward zero |
| Infix conversion | Output operands; stack operators; drain parentheses; left-associative incoming operator pops equal precedence |
| Prefix | Operator before operands; direct reverse evaluation pops left first |
| Collision simulation | Only surviving positive left neighbor versus incoming negative can collide |
| Remove k digits | Pop a larger kept last digit while deletions remain; remove unused budget from suffix; strip leading zeros |
| Iterative DFS | Frames retain vertex and next neighbor; visited prevents cycles |
| Two-stack queue | Transfer only if outgoing is empty; each value transfers once |
| Matrix rectangle | Consecutive-1 heights for each bottom row; histogram per row |
| Sum of minima | Previous strict smaller + next smaller-or-equal; rightmost equal minimum owns the interval |
| Sum of ranges | Sum maximum contributions minus sum minimum contributions |

For contributions: `count=(i-L)*(R-i)`. Asymmetric strictness avoids duplicate ownership. Histogram may use strict smaller on both sides because overlapping candidate maxima do not add duplicate counts.

## 6. Debugging checklist

- Write the exact relationship: `<`, `<=`, `>`, or `>=`. Test `[2,2]`.
- Name what each stack entry means: candidate, waiting index, saved minimum, operator, frame, or survivor.
- Match scan direction to that meaning. Read candidate answers before pushing current.
- Guard top/pop when empty; guard empty arrays before reading first/last; avoid unsigned `size()-1` loops.
- Verify whether output needs values, zero-based indices, one-based positions, distances, or areas.
- Derive imaginary boundaries: absence -1 for neighbor output, -1 and n for histogram geometry, 0 for CSES absent one-based position.
- Clear temporary stacks between independent boundary passes.
- Make circular answers strict and test singleton/all-equal/wraparound cases.
- Promote operands before multiplication/negation; check total and intermediate numeric bounds.
- Restore historical minima on pop; test repeated minima and full empty/reuse cycles.
- Verify celebrity's row and column even after successful elimination; exclude diagonal.
- Distinguish O(n) input/output/working storage and per-operation worst-case/amortized work.
- Test increasing, decreasing, zero-height, duplicate-heavy, and missing-answer inputs against a brute baseline.

**Small checkpoints:** span `[4,4]→[1,2]`; NGE `[2,2,3]→[3,3,-1]`; previous smaller `[2,2]→[-1,-1]`; histogram `[2,2]→4`; circular `[2,3,1]→[3,-1,2]`; water `[3,0,3]→3`; minimum sum `[2,2]→6`.
