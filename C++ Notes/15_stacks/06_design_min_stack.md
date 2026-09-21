# Lecture 73: Design Min Stack (LeetCode 155)

> **One-Line Purpose:** Design a stack supporting `push`, `pop`, `top`, and retrieving the minimum element `getMin` in strict $O(1)$ time and $O(1)$ auxiliary space via mathematical value encoding ($2x - \text{minVal}$).

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #73  
> **Video ID:** `wHDm-N2m2XY`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=wHDm-N2m2XY)  
> **Duration:** 24:34  
> **Status:** AUDITED  

---

## 🔵 Value Encoding Invariant
If a newly pushed element $x < \text{minVal}$, push modified encoded value:
$$\text{encoded} = 2x - \text{minVal}$$
Because $x < \text{minVal}$, the encoded value is strictly less than $x$, acting as a flag.
When popping, if $\text{top} < \text{minVal}$, recover previous minimum:
$$\text{prevMin} = 2 \times \text{minVal} - \text{top}$$

---

## 💻 Complete C++ Implementation

```cpp
#include <stack>
#include <climits>
#include <iostream>

using namespace std;

class MinStack {
private:
    stack<long long> st;
    long long minVal;

public:
    MinStack() : minVal(LLONG_MAX) {}

    void push(int val) {
        long long x = val;
        if (st.empty()) {
            st.push(x);
            minVal = x;
        } else if (x < minVal) {
            st.push(2 * x - minVal); // Encoded flag value
            minVal = x;
        } else {
            st.push(x);
        }
    }

    void pop() {
        if (st.empty()) return;
        long long topVal = st.top();
        st.pop();

        if (topVal < minVal) {
            // Restore previous minVal
            minVal = 2 * minVal - topVal;
        }
    }

    int top() {
        long long topVal = st.top();
        if (topVal < minVal) {
            return (int)minVal;
        }
        return (int)topVal;
    }

    int getMin() {
        return (int)minVal;
    }
};

int main() {
    MinStack ms;
    ms.push(-2);
    ms.push(0);
    ms.push(-3);
    cout << "getMin: " << ms.getMin() << endl; // -3
    ms.pop();
    cout << "top:    " << ms.top()    << endl; // 0
    cout << "getMin: " << ms.getMin() << endl; // -2
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** Strict $O(1)$ for all operations.
- **Space Complexity:** $O(1)$ auxiliary memory (single stack with no auxiliary min stack).

---

## 🧠 Core Intuition — Why This Works

**The Challenge:** A regular stack gives O(1) for push/pop/top, but `getMin()` would require scanning all elements = O(N). How do we get O(1) for ALL operations?

**Two Approaches:**

**Approach 1 — Auxiliary Min Stack (O(N) space, easier to understand):**
Maintain a parallel `minStack` that always has the current minimum at its top. On every push, also push `min(val, minStack.top())`. On every pop, pop from both. `getMin()` = `minStack.top()`.

```
Push(-2): main=[-2],    minStack=[-2]
Push(0):  main=[-2,0],  minStack=[-2,-2]  ← min is still -2
Push(-3): main=[-2,0,-3], minStack=[-2,-2,-3]  ← new min
getMin() → minStack.top() = -3
Pop():    main=[-2,0],  minStack=[-2,-2]  ← automatically restores min to -2!
getMin() → -2 ✓
```

**Approach 2 — Encoding Trick (O(1) auxiliary space, the clever one):**
When pushing a new minimum `x`, store `2x - minVal` (an encoded "flag" value). Since `x < minVal`, the encoded value `< x`. Detection: whenever `top < minVal`, the actual top is `minVal` (the current min) and we must recover the previous min via `prevMin = 2*minVal - encoded`.

```
Why 2x - minVal is always < minVal:
  x < minVal  ⟹  x - minVal < 0  ⟹  x + (x - minVal) < x < minVal
  So encoded = 2x - minVal < x < minVal  → flag detected by top < minVal
```

---

## 🎯 Pattern Recognition — When to Use This

- "Stack with O(1) min/max" → Auxiliary stack (easy) or encoding trick (space-optimal).
- "getMin after each pop" → Both approaches handle this naturally.
- If values are `long long` or very large: watch for overflow in the encoding trick.

---

## 💻 Approach 1: Auxiliary Stack Implementation

```cpp
class MinStackAux {
    stack<int> mainStack;
    stack<int> minStack;
public:
    void push(int val) {
        mainStack.push(val);
        if (minStack.empty() || val <= minStack.top())
            minStack.push(val);
        else
            minStack.push(minStack.top()); // Push current min again
    }
    void pop() {
        mainStack.pop();
        minStack.pop();
    }
    int top() { return mainStack.top(); }
    int getMin() { return minStack.top(); }
};
```

**Trade-off:** This uses $O(N)$ extra space for the min stack. The encoding trick uses $O(1)$ extra space but requires `long long` and is harder to understand.

---

## 🔍 Dry Run Trace (Encoding Trick)

```
push(-2): stack empty → push(-2) directly, minVal=-2. Stack:[-2]
push(0):  0 >= minVal(-2), push 0 normally.      Stack:[-2, 0]
push(-3): -3 < minVal(-2), encode = 2(-3)-(-2) = -4 (flag!), minVal=-3. Stack:[-2,0,-4]
getMin(): return minVal = -3 ✓
top():    top=-4 < minVal(-3) → actual top is minVal = -3 ✓
pop():    top=-4 < minVal(-3), recover prevMin = 2(-3)-(-4) = -2. minVal=-2. Stack:[-2,0]
top():    top=0 >= minVal(-2), return 0 ✓
getMin(): return minVal = -2 ✓
```

---

## ⚠️ Common Interview Mistakes

1. **Integer overflow in encoding trick:** `2x - minVal` can overflow `int`. ALWAYS use `long long` for the stack and `minVal` when using this approach.

2. **Forgetting to pop from BOTH stacks in auxiliary approach:** If you pop only from mainStack and forget minStack, getMin() is wrong for all future operations.

3. **Incorrect top() in encoding trick:** When `topVal < minVal`, the actual `top()` is `minVal` (not `topVal`). Beginners return `topVal` directly — wrong!

4. **Off-by-one in auxiliary push:** When pushing to minStack in auxiliary approach, you must always push (even if val > min) so both stacks stay synchronized in size. Some implementations only push to minStack when val ≤ current min, then pop only when top matches min — this is an alternative correct approach but the stack sizes diverge.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Explain WHY the encoding `2x - minVal` works as a recovery mechanism.
**Answer:** When we detect that `top < minVal` (the flag), it means the encoded value = `2 * newMin - oldMin`. We currently have `minVal = newMin`. To recover `oldMin`:
$$\text{encoded} = 2 \cdot \text{newMin} - \text{oldMin}$$
$$\Rightarrow \text{oldMin} = 2 \cdot \text{newMin} - \text{encoded} = 2 \cdot \text{minVal} - \text{top}$$
This is a lossless encoding: the encoded value uniquely encodes both `newMin` and `oldMin` given that we know `newMin` (stored in `minVal`).

### Q2: [Design] How would you implement a Max Stack similarly?
**Answer:** Identical structure — replace `minVal` with `maxVal` and flip the comparison:
```cpp
void push(int val) {
    if (val > maxVal) {
        st.push(2LL * val - maxVal); // Encode new max
        maxVal = val;
    } else st.push(val);
}
int getMax() { return maxVal; }
// In pop(): if top > maxVal, prevMax = 2*maxVal - top; maxVal = prevMax;
```

### Q3: [Extension] What if you need getMin() AND getMax() both in O(1)?
**Answer:** Use two auxiliary stacks in parallel (not the encoding trick, which handles only one). `minStack` and `maxStack` both track their respective extremes. On push, push `min(val, minStack.top())` to minStack and `max(val, maxStack.top())` to maxStack. On pop, pop from all three. Space: $O(N)$ total (three synchronized stacks).

### Q4: [Debugging] What is wrong with this auxiliary min stack implementation?
```cpp
void push(int val) {
    mainStack.push(val);
    if (minStack.empty() || val < minStack.top())  // Note: < not <=
        minStack.push(val);
}
void pop() {
    if (mainStack.top() == minStack.top()) minStack.pop(); // Only pop if it's the min
    mainStack.pop();
}
```
**Answer:** This is actually a **valid alternative approach** — only push to minStack when val is a new minimum (using `<`), and only pop from minStack when we're popping the actual minimum value. The sizes diverge but that's OK. The subtle bug risk: if there are **duplicate minimums** like `push(3), push(1), push(1)` — using `<` (strict) means the second `1` is NOT pushed to minStack, so after one `pop()`, minStack incorrectly says there's no `1` anymore. Fix: use `<=` in the push condition.

### Q5: [Output Prediction] What does the encoding trick produce for `push(INT_MIN)`?
**Answer:** When pushing `INT_MIN`:
- `x = INT_MIN`, and if stack is empty, `minVal = INT_MIN`.
- First push: go directly to main push since stack empty.
- Second push of `INT_MIN`: `x < minVal`? `INT_MIN < INT_MIN` is false, so pushed normally.
- But `2*INT_MIN - minVal` = `2*INT_MIN - INT_MIN` = `INT_MIN` (overflows in 32-bit int!).
This is the overflow hazard. Solution: use `long long` throughout.

### Q6: [Proof] Prove that getMin() always returns the correct minimum after any sequence of push/pop operations.
**Answer:** **Induction on number of operations:**
- Base: After push(x) on empty stack, `minVal = x = min{x}`. Correct.
- Inductive step (push): If `x < minVal`, we encode and set `minVal = x`. Now min is `x`. If `x >= minVal`, we push `x` normally; `minVal` unchanged. Either way, `minVal = min of all elements`.
- Inductive step (pop): If `top < minVal` (encoded value), we recover `prevMin = 2*minVal - top` and set `minVal = prevMin`. This undoes the last minVal update, restoring the previous minimum. If `top >= minVal`, no minVal change needed. By induction, `minVal` always equals the current stack minimum. ∎

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Hint |
|---|---------|----------|
| 155 | Min Stack | This exact problem |
| 716 | Max Stack | Symmetric, also needs O(1) max + popMax |
| 232 | Implement Queue using Stacks | Two-stack model |
| 895 | Maximum Frequency Stack | Freq-based push priority |
| 1381 | Design a Stack With Increment Operation | Lazy propagation on stack |

---

## 🔗 Cross-Topic Connections

- **Design Problems:** Min Stack is the prototypical "design a data structure with extra O(1) operation" problem.
- **Encoding Tricks:** The `2x - minVal` encoding is similar to XOR tricks used in linked-list reversal with O(1) space.
- **Amortized Analysis:** While individual operations are O(1), the overall space analysis is amortized.

---

## ⚡ 2-Minute Revision Flash Card

- **Two approaches:** Auxiliary min-stack (O(N) space, easy) or encoding trick `2x - minVal` (O(1) extra space, clever).
- **Encoding:** push `2x - minVal` when new min; flag = `top < minVal` → actual top is `minVal`.
- **Recovery:** `prevMin = 2 * minVal - encodedTop` when popping an encoded value.
- **MUST use `long long`** with encoding trick to prevent integer overflow.
- **Auxiliary approach bug:** use `<=` not `<` when pushing to minStack — handles duplicate minimums.
