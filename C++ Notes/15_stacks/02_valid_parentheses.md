# Lecture 67 — Valid Parentheses

[Topic Index](./00_master_index.md) · [Previous: Stacks](./01_introduction_to_stacks.md) · [Next: Stock Span](./03_stock_span_problem.md)

**Source:** [Lecture 67](https://www.youtube.com/watch?v=NlHupEeDXzY). **Verification:** full auto-caption sequence reviewed; code frame checked. [Coverage record](../stacks_dsa_notes/SOURCE_COVERAGE.md#lecture-67).

**Prerequisites:** LIFO, `std::stack<char>`, strings, and Boolean conditions.

## Contents

- [1. What makes brackets valid?](#1-what-makes-brackets-valid)
- [2. Why a stack is the right tool](#2-why-a-stack-is-the-right-tool)
- [3. Algorithm and dry run](#3-algorithm-and-dry-run)
- [4. C++17 implementation](#4-c17-implementation)
- [5. Correctness and complexity](#5-correctness-and-complexity)
- [6. Additional explanation and revision](#6-additional-explanation-and-revision)

## 1. What makes brackets valid?

**Lecture flow: approximately 00:34–03:23.** Input contains the six characters `()[]{}`. The goal is to check matching types, nesting order, and whether every opening and closing bracket has a partner. The [official LeetCode 20 statement](https://leetcode.com/problems/valid-parentheses/) limits the input to brackets and a length of 1–10,000.

The phrase **correct order** means the most recently opened **unclosed** bracket must close first. It does not mean opening order and closing order are identical.

| Input | Valid? | Reason |
|---|---|---|
| `({[]})` | Yes | Each inner pair finishes before the outer pair |
| `[](){}` | Yes | Separate valid groups can be adjacent |
| `([)]` | No | `)` tries to close `(` while `[` is still open |
| `(]` | No | Types differ |
| `())` | No | The final closer has no opener |
| `(()` | No | One opener remains unfinished |

Equal counts of opening and closing brackets are **necessary, not sufficient**. `([)]` has matching counts but crossed nesting. A single counter works for a **single bracket type** if prefixes never go negative and the final count is zero; it loses the type/order information needed for three types.

## 2. Why a stack is the right tool

**Lecture flow: approximately 03:23–05:55.** A closing bracket needs the latest unmatched opening bracket. That is exactly the stack's top. The stack stores **unmatched openings**, not every character and not completed pairs.

For `([{}])`, after reading `([{`, the stack is `['(', '[', '{']` bottom → top. The next `}` must match `{`. After that pair is removed, `]` must match `[`, and finally `)` must match `(`.

This is a general interview pattern: use a stack when the current item resolves the **most recent unresolved dependency**. Examples later include expression evaluation and nested scopes.

## 3. Algorithm and dry run

**Lecture flow: approximately 05:55–12:42.** Scan left to right:

1. If the character is an opener, push it.
2. Otherwise, if the stack is empty, reject before accessing its top.
3. Compare the closer with the opening on the top. Reject a type mismatch.
4. If they match, pop the opener.
5. After the scan, accept only if the stack is empty.

**Original dry run:** `([]){}`. Stack notation is bottom → top.

| Position | Character | Stack before | Action | Stack after |
|---|---|---|---|---|
| 0 | `(` | `[]` | Push opener | `['(']` |
| 1 | `[` | `['(']` | Push opener | `['(', '[']` |
| 2 | `]` | `['(', '[']` | Match `[`; pop | `['(']` |
| 3 | `)` | `['(']` | Match `(`; pop | `[]` |
| 4 | `{` | `[]` | Push opener | `['{']` |
| 5 | `}` | `['{']` | Match `{`; pop | `[]` |

Result: `true`. Completed groups leave no residue, so the second group can begin independently.

The lecture explicitly handles three failure modes. A **mismatch** is detected during comparison; **too many closers** produce an empty stack before a match; **too many openers** leave a nonempty stack after the loop. Omitting any one of these checks admits invalid strings or causes an invalid top access.

## 4. C++17 implementation

**Lecture flow: approximately 12:42–15:25.** The implementation below follows the same algorithm, with a range loop and an explicit rejection of non-bracket characters as added defensive behavior.

```cpp
#include <stack>
#include <string>

bool isValid(const std::string& text) {
    std::stack<char> pending;
    for (char c : text) {
        if (c == '(' || c == '[' || c == '{') {
            pending.push(c);
            continue;
        }
        if (c != ')' && c != ']' && c != '}') return false;
        if (pending.empty()) return false;
        const char opening = pending.top();
        const bool matches =
            (opening == '(' && c == ')') ||
            (opening == '[' && c == ']') ||
            (opening == '{' && c == '}');
        if (!matches) return false;
        pending.pop();
    }
    return pending.empty();
}
```

Signature: a string is passed by const reference to avoid a copy; the result is a Boolean. On LeetCode, place this function as a public method of the expected `Solution` class and match the judge's method signature.

Usage: `isValid("([]){}")` is true; `isValid("([)]")` is false; `isValid(")")` is false. The empty string returns true as a deliberate mathematical extension, even though the official input is nonempty.

## 5. Correctness and complexity

**Invariant:** after each accepted prefix, the stack contains exactly its unmatched opening brackets, in encounter order.

An opener adds one unfinished bracket, so push preserves the invariant. A closer can only finish the most recent unfinished opener: if none exists, it is unmatched; if the top type differs, proper nesting is impossible. A matching pop removes exactly the newly completed dependency. At the end, an empty stack means every opener has been matched and every closer was validated. A nonempty stack means some opener is unfinished.

**Lecture analysis: approximately 15:25–16:05.** Every character is examined once: worst-case O(n) time. The maximum number of unmatched openings determines stack space, which is O(n) in the worst case. If the maximum nesting depth is d, actual stack usage is O(d). There is no output array: result space is O(1).

## 6. Additional explanation and revision

### Common wrong solutions

- **Only count brackets:** accepts `([)]` unless order is tracked.
- **Check the stack's top before checking emptiness:** fails on `]` and risks undefined behavior.
- **Always return true after the loop:** accepts `(((`.
- **Forget to pop after a match:** leaves completed openings in the stack.
- **Require one outer pair around the entire string:** wrongly rejects `()[]`.

An odd-length bracket-only string cannot be valid, because brackets are consumed in pairs. An early odd-length check is optional; the algorithm already rejects it correctly.

**Interview/CP extension:** for parsing source code, brackets inside string literals and comments must be ignored according to the language grammar. The six-character problem does not require that lexer. If a task includes wildcards such as `*`, this exact algorithm is insufficient because an ambiguous character can have multiple roles.

**Interview questions:** What precisely does your stack represent? Why do we reject a mismatch immediately? Can you reduce space to O(1) without changing the three-bracket problem's assumptions? Explain why counting alone fails.

**Revision:** push openings; close only the top; reject empty/mismatched tops; require an empty stack at the end.
