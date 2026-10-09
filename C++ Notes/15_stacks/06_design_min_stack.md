# Lecture 71 — Design a Min Stack

[Topic Index](./00_master_index.md) · [Previous: Previous Smaller](./05_previous_smaller_element.md) · [Next: Histogram](./07_largest_rectangle_in_histogram.md)

**Source:** [Min Stack lecture](https://www.youtube.com/watch?v=wHDm-N2m2XY). **Verification:** full auto-caption sequence reviewed; encoded implementation frame checked. [Coverage record](../stacks_dsa_notes/SOURCE_COVERAGE.md#lecture-71).

**Prerequisites:** stack operations, pairs, minimum calculations, and basic algebra.

## Contents

- [1. Requirements and the restoration problem](#1-requirements-and-the-restoration-problem)
- [2. Approach one — store a prefix minimum](#2-approach-one--store-a-prefix-minimum)
- [3. Approach two — encode minimum changes](#3-approach-two--encode-minimum-changes)
- [4. Encoded C++17 implementation](#4-encoded-c17-implementation)
- [5. Additional explanation — duplicate minima and numeric limits](#5-additional-explanation--duplicate-minima-and-numeric-limits)
- [6. Complexity, pitfalls, and revision](#6-complexity-pitfalls-and-revision)

## 1. Requirements and the restoration problem

**Lecture flow: approximately 00:40–02:38.** Support `push`, `pop`, `top`, and **`getMin`** in O(1) per operation. The [LeetCode 155 statement](https://leetcode.com/problems/min-stack/) guarantees nonempty calls to `pop`, `top`, and `getMin`; values may span the entire signed 32-bit range.

The lecture uses pushes `-2,0,-3`: minimum is -3; popping -3 restores minimum -2 while top becomes 0. The important challenge is **restoring an old minimum**, not merely finding a new smaller value during push.

**Additional baseline:** scanning the whole stack for every minimum costs O(n). Keeping only `minSoFar` works for push-only data, but loses history when a minimum is popped. Sorting destroys LIFO order. We need enough history to undo changes.

## 2. Approach one — store a prefix minimum

**Lecture flow: approximately 02:38–07:32.** Store a pair for every entry: `(actual value, minimum of all values up to this entry)`. A new entry's minimum is the smaller of the new value and the previous top's saved minimum.

**Invariant:** every pair contains the minimum of the logical stack prefix ending at that pair. Therefore the top pair's saved minimum is the current stack minimum. Pop removes the entire pair and automatically reveals the previous prefix's minimum.

```cpp
#include <algorithm>
#include <stack>
#include <stdexcept>
#include <utility>

class PairMinStack {
    std::stack<std::pair<int, int>> data;
    void requireValue() const {
        if (data.empty()) throw std::underflow_error("empty min stack");
    }
public:
    bool empty() const { return data.empty(); }
    void push(int value) {
        const int minimum = data.empty() ? value
            : std::min(value, data.top().second);
        data.push({value, minimum});
    }
    void pop() { requireValue(); data.pop(); }
    int top() const { requireValue(); return data.top().first; }
    int getMin() const { requireValue(); return data.top().second; }
};
```

**Original dry run:** pushes `7,4,4,9`. Pairs are shown bottom → top.

| Operation | Pairs after operation | Top | Minimum |
|---|---|---|---|
| Push 7 | `[(7,7)]` | 7 | 7 |
| Push 4 | `[(7,7),(4,4)]` | 4 | 4 |
| Push 4 | `[(7,7),(4,4),(4,4)]` | 4 | 4 |
| Push 9 | `[(7,7),(4,4),(4,4),(9,4)]` | 9 | 4 |
| Pop | `[(7,7),(4,4),(4,4)]` | 4 | 4 |
| Pop | `[(7,7),(4,4)]` | 4 | 4 |
| Pop | `[(7,7)]` | 7 | 7 |

Repeated minima need no special case: each prefix stores its own correct minimum. This is usually the easiest implementation to explain and maintain.

## 3. Approach two — encode minimum changes

**Lecture flow: approximately 07:32–20:41.** Keep one stack of numbers and one current minimum m. Ordinary values `x >= m` are pushed unchanged. A new smaller value must also retain the old minimum, so encode it.

Let old minimum be `old`, new value be x, with `x < old`. Store:

```text
encoded = 2*x - old
new minimum = x
```

The encoded value stores the relationship between the new and previous minima. On popping that entry, invert the equation:

```text
old = 2*new minimum - encoded
```

### How do we recognize an encoded entry?

Because `x < old`, the difference `x-old` is negative. Thus:

```text
encoded = x + (x-old) < x = new minimum
```

A number **smaller than the current minimum** cannot be a normal logical entry. It is a marker for a minimum transition. For a marker at the top, `top()` returns the current minimum, not the stored marker. `pop()` restores the old minimum before removing the marker.

### Original encoded dry run

Push `7,4,4,9`, then pop three times. Stored entries run bottom → top.

| Operation | Stored stack | Logical stack | m | Reason |
|---|---|---|---|---|
| Push 7 | `[7]` | `[7]` | 7 | First value initializes m |
| Push 4 | `[7,1]` | `[7,4]` | 4 | Store `2*4-7=1` |
| Push 4 | `[7,1,4]` | `[7,4,4]` | 4 | Equality is stored normally |
| Push 9 | `[7,1,4,9]` | `[7,4,4,9]` | 4 | Larger value is normal |
| Pop 9 | `[7,1,4]` | `[7,4,4]` | 4 | 9 is not a marker |
| Pop 4 | `[7,1]` | `[7,4]` | 4 | Equal minimum does not restore history |
| Pop logical 4 | `[7]` | `[7]` | 7 | Marker 1 restores `2*4-1=7` |

This explains the **strict `<` tests used in this implementation** for marker creation and recognition. Equal minima remain ordinary entries because they do not change minimum history. Encoding an equal value would produce that same value, so it would not be a distinguishable marker or a useful state transition.

## 4. Encoded C++17 implementation

**Lecture flow: approximately 20:41–23:51.** The lecture explicitly upgrades internal arithmetic to `long long`. The code below uses a 64-bit temporary before multiplication, retains the logical `int` interface, and adds empty-stack guards.

```cpp
#include <stack>
#include <stdexcept>

class EncodedMinStack {
    std::stack<long long> data;
    long long minimum = 0; // Meaningful only when data is nonempty.
    void requireValue() const {
        if (data.empty()) throw std::underflow_error("empty min stack");
    }
public:
    bool empty() const { return data.empty(); }
    void push(int value) {
        const long long x = value; // Widen BEFORE doing arithmetic.
        if (data.empty()) {
            data.push(x);
            minimum = x;
        } else if (x < minimum) {
            data.push(2LL * x - minimum);
            minimum = x;
        } else {
            data.push(x);
        }
    }
    void pop() {
        requireValue();
        const long long stored = data.top();
        if (stored < minimum) minimum = 2LL * minimum - stored;
        data.pop();
        if (data.empty()) minimum = 0;
    }
    int top() const {
        requireValue();
        return static_cast<int>(data.top() < minimum ? minimum : data.top());
    }
    int getMin() const {
        requireValue();
        return static_cast<int>(minimum);
    }
};
```

Usage: construct either stack, push `7,4,4,9`; `getMin()` returns 4. After three pops, `top()` and `getMin()` both return 7. Pushing after fully emptying the stack reinitializes the minimum correctly.

**Correctness:** normal pushes do not change the minimum; encoded pushes record an invertible minimum transition. Entries above a marker are popped first because of LIFO, so by the time the marker reaches the top its corresponding new minimum has been restored. The marker test and inverse formula therefore operate with the correct minimum. No scan is needed.

## 5. Additional explanation — duplicate minima and numeric limits

### A two-stack alternative

Use a normal value stack and a second stack of historical minima. Push to the minima stack whenever `x <= current minimum`, including equality. Pop from the minima stack whenever the removed value equals its top. The duplicate rule matters: pushes `5,3,3`, followed by one pop, must still have minimum 3.

This variation is not the lecture's second approach; the lecture's second approach is arithmetic encoding. The pair approach stores a minimum for **every prefix**, while the two-stack version can store only minima occurrences.

```cpp
#include <stack>
#include <stdexcept>

class TwoMinStack {
    std::stack<int> values, minima;
    void requireValue() const {
        if (values.empty()) throw std::underflow_error("empty min stack");
    }
public:
    bool empty() const { return values.empty(); }
    void push(int value) {
        values.push(value);
        if (minima.empty() || value <= minima.top()) minima.push(value);
    }
    void pop() {
        requireValue();
        if (values.top() == minima.top()) minima.pop();
        values.pop();
    }
    int top() const { requireValue(); return values.top(); }
    int getMin() const { requireValue(); return minima.top(); }
};
```

Usage: push `5,3,3`; the minima stack is `[5,3,3]` bottom → top. One pop leaves `[5,3]`, so the minimum stays 3; another leaves `[5]`, restoring 5. Each saved occurrence belongs to a live entry that was a minimum when pushed. LIFO pops reveal those saved minima in reverse order. Operations require O(1) underlying stack work; worst-case live storage O(n), with two stacks retaining all entries when values decrease or stay equal.

### Arithmetic safety

`long long encoded = 2 * value - minimum` is unsafe if `2*value` happens first in `int`. Use `2LL*value` or widen value first. For 32-bit inputs, the encoded expression fits in signed 64-bit storage, including pushes of `INT_MAX` followed by `INT_MIN`.

This does **not** prove safety for arbitrary 64-bit inputs. Doubling an arbitrary `long long` can overflow. Prefer the pair approach when the numeric domain is too wide or unspecified.

## 6. Complexity, pitfalls, and revision

**Lecture analysis: approximately 23:51–24:29.** Both approaches have O(1) push/pop/top/getMin data-structure work and O(n) total storage for n live entries. Pair storage uses two logical values per entry; encoding uses one stored numeric entry plus a global minimum.

**Clarification:** encoding adds only O(1) bookkeeping outside its stack, but its **total storage remains O(n)**. Also, a pair of two 32-bit integers and a single 64-bit integer can have the same payload size. Encoding does not automatically halve actual bytes. The benefit is the technique for reversible state changes, not a guaranteed physical-memory saving.

Common mistakes: returning a marker as the logical top; updating minimum before using its old value to encode; restoring with the wrong sign; losing equal minima in a two-stack variant; forgetting first-push initialization; and advertising O(1) total storage.

**Interview check:** derive the inverse equation, prove the marker inequality, walk through repeated minima, and explain why the pair approach is often preferable in production code.

**Revision:** save prefix minima for simplicity. For encoding, new smaller x stores `2*x-old`; marker pop restores `2*current-stored`; marker top is the current minimum.
