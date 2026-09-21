# Lecture 70: Stock Span Problem: Monotonic Decreasing Stack

> **One-Line Purpose:** Calculate consecutive days prior to today where stock price was less than or equal to today's price using a Monotonic Decreasing Stack of indices in amortized $O(1)$ per query.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #70  
> **Video ID:** `01vBuZyMfqk`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=01vBuZyMfqk)  
> **Duration:** 26:29  
> **Status:** AUDITED  

---

## 🔵 Monotonic Decreasing Stack Principle
Stack stores indices of strictly greater elements to the left.
$$\text{span}[i] = i - \text{indexOfPreviousGreaterElement}$$
If no greater element exists, $\text{span}[i] = i + 1$.

---

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <stack>
#include <iostream>

using namespace std;

class StockSpanner {
private:
    stack<pair<int, int>> st; // <price, span>

public:
    StockSpanner() {}

    int next(int price) {
        int span = 1;
        while (!st.empty() && st.top().first <= price) {
            span += st.top().second;
            st.pop();
        }
        st.push({price, span});
        return span;
    }
};

int main() {
    StockSpanner spanner;
    vector<int> prices = {100, 80, 60, 70, 60, 75, 85};
    cout << "Spans: ";
    for (int p : prices) cout << spanner.next(p) << " "; // 1 1 1 2 1 4 6
    cout << endl;
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** Amortized $O(1)$ per `next()` call ($O(N)$ total for $N$ queries).
- **Space Complexity:** $O(N)$ stack memory.

---

## 🧠 Core Intuition — Why This Works

**The Stock Span Problem is Next Greater Element on the LEFT in disguise.**

The span of day $i$ is the count of consecutive days (including day $i$) where price was ≤ today's price. To compute this, we need the index of the **most recent day where price was strictly GREATER than today**. The span = distance from that day to today.

**Why Monotonic Decreasing Stack?** We maintain a stack of `(price, span)` pairs where prices are always decreasing from bottom to top. When a new price comes in that is ≥ stack top, we **absorb** the span of those smaller prices (because they can't be the boundary for any future query either). This is the key leap: we accumulate spans rather than store indices.

```
Prices: 100  80  60  70  60  75  85
Index:    0   1   2   3   4   5   6

Day 0: price=100, span=1    Stack: [(100,1)]
Day 1: price=80,  span=1    Stack: [(100,1),(80,1)]
Day 2: price=60,  span=1    Stack: [(100,1),(80,1),(60,1)]
Day 3: price=70,  pop 60 (60≤70, absorb span=1), span=2
                            Stack: [(100,1),(80,1),(70,2)]
Day 4: price=60,  span=1    Stack: [(100,1),(80,1),(70,2),(60,1)]
Day 5: price=75,  pop 60 (absorb 1), pop 70 (absorb 2), span=4
                            Stack: [(100,1),(80,1),(75,4)]
Day 6: price=85,  pop 75 (absorb 4), pop 80 (absorb 1), span=6
                            Stack: [(100,1),(85,6)]
Output: 1 1 1 2 1 4 6
```

---

## 🎯 Pattern Recognition — When to Use This Pattern

- "How many consecutive previous elements are ≤ (or ≥) current element?" → Monotonic Stack with span accumulation.
- "Previous Greater Element" → Direct monotonic stack with index.
- **Distinguish from NGE:** Stock Span asks about *all* consecutive preceding elements, not just the nearest. The span trick avoids storing all indices by accumulating counts.

---

## 🔍 Dry Run Trace

Prices = `{100, 80, 60, 70, 60, 75, 85}`, traced through `next(price)`:

| Call | Price | Stack (price,span) before | Pops | Span | Stack after |
|------|-------|--------------------------|------|------|-------------|
| 1 | 100 | empty | 0 | 1 | [(100,1)] |
| 2 | 80 | [(100,1)] | 0 | 1 | [(100,1),(80,1)] |
| 3 | 60 | [(100,1),(80,1)] | 0 | 1 | [...,(60,1)] |
| 4 | 70 | [...,(60,1)] | pop(60) | 1+1=2 | [(100,1),(80,1),(70,2)] |
| 5 | 60 | [...,(70,2)] | 0 | 1 | [...,(60,1)] |
| 6 | 75 | [...,(60,1),(70,2) wait: (80,1)] | pop(60)+pop(70) | 1+1+2=4 | [(100,1),(80,1),(75,4)] |
| 7 | 85 | [(100,1),(80,1),(75,4)] | pop(75)+pop(80) | 1+4+1=6 | [(100,1),(85,6)] |

---

## ⚠️ Common Interview Mistakes

1. **Storing indices instead of (price, span) pairs:** Fine for single-pass offline, but the span-accumulation trick is needed for online query-by-query processing.

2. **Wrong comparison (`<` vs `<=`):** Span counts days with price ≤ today, so pop when `st.top().first <= price`. Using `<` would undercount ties.

3. **Forgetting to initialize span = 1:** Every day has a self-span of at least 1. Not initializing to 1 gives span = 0.

4. **Confusing amortized vs worst-case:** In a single call, `next()` can do $O(N)$ pops (when price is the all-time max). Interviewers often ask you to justify why it's $O(1)$ amortized — each element is pushed once and popped once.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] What is the relationship between Stock Span and Next Greater Element on the Left?
**Answer:** They are equivalent problems. The stock span for day $i$ equals `i - j` where `j` is the index of the Previous Greater Element (PGE) to the left of day $i$. If no PGE exists, span = `i + 1` (all days from 0 to i). So Stock Span = $i - \text{PGE\_index}[i]$, which is exactly the Nearest Greater Element to the Left problem computed efficiently with a monotonic decreasing stack.

### Q2: [Derivation] Prove that the total time for N queries is O(N) despite individual calls doing O(N) work.
**Answer:** Use an **amortized argument**. Each of the $N$ prices is pushed into the stack **exactly once** and popped **at most once**. Therefore, the total number of push + pop operations across all $N$ calls to `next()` is bounded by $2N$. Dividing by $N$ calls gives amortized $O(1)$ per call. The $\Sigma$ of all pops across all calls ≤ $N$.

### Q3: [Design] Can you solve this with O(1) space (no auxiliary stack)?
**Answer:** No, not in general with online queries. Without the stack, you'd need to scan all previous prices to find the previous greater element — taking $O(N)$ per query and $O(N^2)$ total. The stack is essential for the amortized $O(1)$ per query behavior. Note: if all prices are given upfront (offline), you can precompute spans in $O(N)$ using the Previous Greater Element pattern on the whole array.

### Q4: [Extension] How do you handle duplicate prices? Should the condition be `<` or `<=`?
**Answer:** The span counts days where price was **less than OR equal to** today's price (consecutive days including tie days). Therefore the pop condition must be `st.top().first <= price` (pop when top price ≤ current price). Using strict `<` would NOT absorb equal prices, causing incorrect shorter spans on tie days.

### Q5: [Output Prediction] What is the output for prices = {3, 3, 3}?
**Answer:** 
- Day 0: price=3, stack empty → span=1. Stack: [(3,1)]
- Day 1: price=3, pop (3,1) because 3≤3, span=1+1=2. Stack: [(3,2)]
- Day 2: price=3, pop (3,2) because 3≤3, span=1+2=3. Stack: [(3,3)]
Output: **1 2 3** — each day the span grows by absorbing all equal-price days.

### Q6: [Extension] How would you adapt this for a sliding window (only consider last K days)?
**Answer:** Store indices instead of span-accumulation, and add an expiry check: when the span would extend beyond K days, cap it. The condition becomes `span = min(accumulated_span, K)`. Alternatively, store `(price, index)` pairs and when `i - st.top().second >= K`, stop popping.

### Q7: [System Design] How would you design this for a real-time stock price feed with millions of tickers?
**Answer:** Each ticker maintains its own `StockSpanner` object (a stack per ticker). Since we process prices event-by-event, the amortized O(1) per event is ideal for real-time systems. For persistence, the stack state must be serialized to handle system restarts. For parallel tickers, no shared state means embarrassingly parallel processing — no locks needed.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Hint |
|---|---------|----------|
| 901 | Online Stock Span | This exact problem |
| 496 | Next Greater Element I | Offline NGE with hash map |
| 503 | Next Greater Element II | Circular array + modulo |
| 739 | Daily Temperatures | NGE variant with day distances |
| 84 | Largest Rectangle in Histogram | Previous smaller from both sides |

---

## 🔗 Cross-Topic Connections

- **Next/Previous Greater Element:** Stock Span is PGE-left, reframed as span counting.
- **Monotonic Stack family:** All "nearest boundary" problems share the same core mechanism.
- **Sliding Window:** Extending to "span within last K days" connects to sliding window max problems.

---

## ⚡ 2-Minute Revision Flash Card

- **Span[i]** = number of consecutive prior days with price ≤ today = `i - PGE_left_index`.
- **Store `(price, span)` pairs**, not indices — accumulate spans to avoid re-scanning.
- **Pop condition:** `st.top().first <= price` (absorb all ≤ days into current span).
- **Amortized O(1):** Each element pushed once, popped once → total $O(N)$ for N queries.
- **Gotcha:** `<=` not `<` — equal-price days must be absorbed into the span.
