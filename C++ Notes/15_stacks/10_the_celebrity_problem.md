# Lecture 75 — The Celebrity Problem

[Topic Index](./00_master_index.md) · [Previous: Rainwater](./09_trapping_rainwater.md) · [Next: Infix & Postfix](./11_infix_postfix_prefix_conversions.md) · [Monotonic Stack Patterns](../stacks_dsa_notes/supplements/monotonic_stack_patterns.md)

**Source:** [Lecture 75](https://www.youtube.com/watch?v=OZPmEA_8FM8). **Verification:** full auto-caption sequence reviewed; candidate verification and diagonal exclusion visually checked. [Coverage record](../stacks_dsa_notes/SOURCE_COVERAGE.md#lecture-75).

**Prerequisites:** matrix indexing, directed relationships, stacks, and candidate elimination.

## Contents

- [1. Matrix meaning and celebrity conditions](#1-matrix-meaning-and-celebrity-conditions)
- [2. Eliminate one candidate per comparison](#2-eliminate-one-candidate-per-comparison)
- [3. A survivor still needs verification](#3-a-survivor-still-needs-verification)
- [4. Stack algorithm and original dry run](#4-stack-algorithm-and-original-dry-run)
- [5. C++17 implementation](#5-c17-implementation)
- [6. Correctness and complexity](#6-correctness-and-complexity)
- [7. Interview/CP extension — constant extra space](#7-interviewcp-extension--constant-extra-space)
- [8. Pitfalls and revision](#8-pitfalls-and-revision)

## 1. Matrix meaning and celebrity conditions

**Lecture flow: approximately 00:32–03:44.** Given a square binary matrix M for n people, `M[i][j] == 1` means **person i knows person j**. This is directed: knowing someone does not imply they know you.

A celebrity c satisfies both conditions for every **other** person i:

```text
M[i][c] = 1   everyone else knows c
M[c][i] = 0   c knows nobody else
```

Return c's index, or `-1` if no celebrity exists. The lecture's three-person example has rows `[0,1,0]`, `[0,0,0]`, `[0,1,0]`; person 1 is the celebrity.

The diagonal `M[c][c]` is **ignored**. Requiring it to be both 1 and 0 would be contradictory. The lesson explicitly excludes `i == c` in its final check. A different judge may define diagonal entries, but that does not alter the “other people” test used here.

**Input contract:** these functions assume an n×n matrix with entries 0 or 1. Reading and validating a whole matrix is O(n²); the advertised algorithmic time measures work **after valid input is already available**.

## 2. Eliminate one candidate per comparison

**Lecture flow: approximately 03:44–06:18.** Compare two different candidates a and b with one matrix lookup:

| Lookup | Certain conclusion | Possible survivor |
|---|---|---|
| `M[a][b] == 1` | a knows someone, so a cannot be a celebrity | b |
| `M[a][b] == 0` | a does not know b, so b is not known by everyone | a |

The survivor is only **possible**. Neither branch proves celebrity status. It proves that one of the two candidates is impossible.

This distinction is a common interview theme: elimination can narrow a search with less information than full validation requires.

## 3. A survivor still needs verification

**Lecture flow: approximately 06:18–07:57.** Any pairwise elimination process ends with a survivor even when the actual input has no celebrity. Therefore check its entire incoming column and outgoing row, excluding the diagonal.

For example, start with a celebrity-shaped matrix for person 2, then change `M[2][0]` from 0 to 1. A certain elimination order can still leave person 2 alive without examining that relationship. The final row check rejects it because the survivor knows person 0.

The verification fails if **either** someone does not know c **or** c knows someone else. Correct grouping is:

```text
i != c AND (M[i][c] == 0 OR M[c][i] == 1)
```

The parentheses matter: an ungrouped expression can accidentally apply the diagonal exclusion to only one branch.

## 4. Stack algorithm and original dry run

**Lecture flow: approximately 07:57–11:37.** Push all indices 0 through n-1. While at least two remain, pop two, eliminate one using the table above, and push the possible survivor. Verify the final survivor.

**Original example:**

```text
M = [ [0,1,1,0],
      [0,0,1,0],
      [0,0,0,0],
      [1,0,1,0] ]
```

Person 2 is the celebrity. Stack displays are bottom → top.

| Before | a,b popped in order | Lookup | Eliminated | After pushing survivor |
|---|---|---|---|---|
| `[0,1,2,3]` | 3,2 | `M[3][2]=1` | 3 | `[0,1,2]` |
| `[0,1,2]` | 2,1 | `M[2][1]=0` | 1 | `[0,2]` |
| `[0,2]` | 2,0 | `M[2][0]=0` | 0 | `[2]` |

Now verify: `M[0][2]=M[1][2]=M[3][2]=1`, and `M[2][0]=M[2][1]=M[2][3]=0`. Return **2**.

## 5. C++17 implementation

**Lecture flow: approximately 11:37–13:57.** The empty-input guard is added context; it prevents calling `top()` when there are no people.

```cpp
#include <stack>
#include <vector>

int celebrityStack(const std::vector<std::vector<int>>& knows) {
    const int n = static_cast<int>(knows.size());
    if (n == 0) return -1;
    std::stack<int> candidates;
    for (int i = 0; i < n; ++i) candidates.push(i);
    while (candidates.size() > 1) {
        const int a = candidates.top(); candidates.pop();
        const int b = candidates.top(); candidates.pop();
        candidates.push(knows[a][b] == 1 ? b : a);
    }
    const int c = candidates.top();
    for (int i = 0; i < n; ++i) {
        if (i != c && (knows[i][c] == 0 || knows[c][i] == 1))
            return -1;
    }
    return c;
}
```

Usage: the matrix above returns 2. Changing `M[2][0]` to 1 returns -1. A one-person matrix returns 0 under the chosen “other people” convention regardless of its diagonal value.

## 6. Correctness and complexity

**Invariant:** if a genuine celebrity exists, it remains among the live candidates. A celebrity never knows another person and is known by every other person, so neither elimination rule can discard it. Each comparison removes one provably impossible candidate. After n-1 comparisons, only one possible candidate remains. Verification checks exactly the two defining conditions, making the final result sound even when no celebrity exists.

**Additional uniqueness proof:** suppose two distinct people a and b were both celebrities. Since a is a celebrity, a does not know b. Since b is a celebrity, a must know b. Contradiction. At most one celebrity exists.

**Lecture analysis: approximately 13:57–14:35.** Initialization costs O(n); elimination costs O(n); verification costs O(n). Total algorithm time is **O(n)** and auxiliary stack space **O(n)**. Input storage is O(n²), while the result is O(1). There is no contradiction between a quadratic input and linear additional matrix lookups: random access permits examining selected entries.

## 7. Interview/CP extension — constant extra space

The stack organizes pair selection but is not essential to elimination. Keep one possible candidate and compare it with each new person. This is an extension, not the lecture's main coded approach.

```cpp
#include <vector>

int celebrityConstantSpace(const std::vector<std::vector<int>>& knows) {
    const int n = static_cast<int>(knows.size());
    if (n == 0) return -1;
    int candidate = 0;
    for (int person = 1; person < n; ++person) {
        if (knows[candidate][person] == 1) candidate = person;
        // Otherwise person is impossible, and candidate remains possible.
    }
    for (int person = 0; person < n; ++person) {
        if (person != candidate &&
            (knows[person][candidate] == 0 || knows[candidate][person] == 1))
            return -1;
    }
    return candidate;
}
```

Time O(n), auxiliary space O(1), with the same final verification requirement. In an API version `knows(a,b)`, elimination uses n-1 queries and validation uses at most `2(n-1)` additional queries; short-circuiting may use fewer.

## 8. Pitfalls and revision

- Do not return the survivor without checking both row and column.
- Do not reverse matrix meaning: the row index is the person doing the knowing.
- Ignore diagonal entries during verification.
- The survivor need not be an actual celebrity; elimination proves impossibility for others.
- Explain the distinction between input-reading cost and the algorithm's additional work.
- Handle n=0 before using the stack's top.

**Interview check:** justify each elimination branch; prove a real celebrity cannot disappear; show a no-celebrity counterexample; remove the explicit stack without changing correctness.

**Revision:** one relationship eliminates one person. Narrow to one candidate, then verify everyone knows them and they know nobody else.
