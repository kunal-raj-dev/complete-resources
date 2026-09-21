# Lecture 71: Next Greater Element I (LeetCode 496)

> **One-Line Purpose:** Find the first strictly greater element to the right for each array element using a Monotonic Stack scanned backwards from right to left in $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #71  
> **Video ID:** `NKbExYwvjb0`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=NKbExYwvjb0)  
> **Duration:** 23:32  
> **Status:** AUDITED  

---

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <stack>
#include <iostream>

using namespace std;

class NextGreaterElement {
public:
    static vector<int> solve(const vector<int>& nums) {
        int n = nums.size();
        vector<int> nge(n, -1);
        stack<int> st; // Monotonic decreasing stack storing values

        for (int i = n - 1; i >= 0; --i) {
            while (!st.empty() && st.top() <= nums[i]) {
                st.pop();
            }

            if (!st.empty()) {
                nge[i] = st.top();
            }

            st.push(nums[i]);
        }

        return nge;
    }
};

int main() {
    vector<int> arr = {4, 5, 2, 25};
    vector<int> res = NextGreaterElement::solve(arr);
    cout << "Next Greater Elements: ";
    for (int x : res) cout << x << " "; // Output: 5 25 25 -1
    cout << endl;
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(N)$

---

## 🧠 Core Intuition — Why This Works

**The Key Insight:** When processing from right to left, we want the first element to the right that is strictly greater. The stack holds **candidates** for being the NGE of future (leftward) elements. When we're at index $i$ with value `nums[i]`, any stack element ≤ `nums[i]` can NEVER be the NGE of any element to the left of $i$ (because `nums[i]` would block them). So we pop them — they're eliminated forever.

**Monotonic Decreasing Stack (right-to-left scan):** The stack always holds elements in decreasing order. When processing index $i$:
1. Pop all elements ≤ `nums[i]` (they can never be NGE for anything to i's left).
2. If stack non-empty, top is the NGE of `nums[i]`.
3. Push `nums[i]`.

```
Array: [4, 5, 2, 25]   (right-to-left scan)

i=3: val=25, stack empty → NGE[3]=-1. Push 25. Stack: [25]
i=2: val=2,  top=25>2  → NGE[2]=25.  Push 2.  Stack: [25,2]
i=1: val=5,  pop 2(2≤5), top=25>5   → NGE[1]=25. Push 5. Stack: [25,5]
i=0: val=4,  top=5>4   → NGE[0]=5.  Push 4.  Stack: [25,5,4]

Result: NGE = [5, 25, 25, -1]  ✓
```

---

## 🎯 Pattern Recognition — When to Use Monotonic Stack

| Signal | Direction | Stack Type |
|--------|-----------|------------|
| "Next Greater to the RIGHT" | Right → Left | Monotonic Decreasing |
| "Previous Greater to the LEFT" | Left → Right | Monotonic Decreasing |
| "Next Smaller to the RIGHT" | Right → Left | Monotonic Increasing |
| "Previous Smaller to the LEFT" | Left → Right | Monotonic Increasing |

**Alternative left-to-right approach for NGE:** Process left-to-right, maintain a stack of **unresolved** elements. When you see element `x` that is greater than stack top, the top's NGE is `x` — pop and record. Push `x` as a new unresolved element.

---

## 🔍 Dry Run Trace

Array: `[2, 7, 4, 3, 5]`

```
Right-to-left: i=4,3,2,1,0

i=4: val=5   Stack: []→ NGE[4]=-1. Push 5.  Stack:[5]
i=3: val=3   top=5>3 → NGE[3]=5.  Push 3.  Stack:[5,3]
i=2: val=4   pop 3(3≤4), top=5>4 → NGE[2]=5. Push 4. Stack:[5,4]
i=1: val=7   pop 4(4≤7), pop 5(5≤7), empty → NGE[1]=-1. Push 7. Stack:[7]
i=0: val=2   top=7>2 → NGE[0]=7. Push 2. Stack:[7,2]

Result: [7, -1, 5, 5, -1]
```

---

## ⚠️ Common Interview Mistakes

1. **Processing left-to-right with wrong stack type:** NGE right-to-left with decreasing stack is cleanest. Left-to-right requires an "unsatisfied" stack approach — different invariant.

2. **Storing values instead of indices:** When NGE needs to return the actual greater value, store values. When it needs to return distances (like Daily Temperatures), store indices.

3. **Wrong comparison (`<` vs `<=`):** For STRICTLY greater, use `st.top() <= nums[i]` to pop. For "greater or equal", use `st.top() < nums[i]`.

4. **Not initializing NGE array to -1:** If no greater element exists, result should be -1. Use `vector<int> nge(n, -1)` for clean initialization.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] What is the invariant of the monotonic stack in this right-to-left NGE algorithm?
**Answer:** After processing index $i$, the stack contains all values from `nums[i..n-1]` that are still "live" as potential NGE answers for elements at indices ≤ $i$. These values are in **strictly decreasing order** from bottom to top. Elements that were popped are permanently discarded — they were dominated by a larger element to their left, so they can never be an NGE for anyone further left.

### Q2: [Conceptual] Why does a Monotonic Decreasing Stack work for "Next Greater" but an Increasing Stack works for "Next Smaller"?
**Answer:** For NGE, we want the **first larger** element. We pop elements that are ≤ current value because they can never be the NGE of anything to the left (current value blocks them). The surviving stack is decreasing. For NSE (Next Smaller Element), we want the first smaller element, so we pop elements that are ≥ current value. The surviving stack is increasing.

### Q3: [Extension] LeetCode 496: Given two arrays `nums1` (subset of `nums2`), find NGE of each nums1 element in nums2. How?
**Answer:** Compute NGE for all elements in `nums2` using the standard monotonic stack. Store results in a hash map: `nge_map[val] = next_greater_val`. Then for each element in `nums1`, look up `nge_map[elem]`. Time: $O(M + N)$, Space: $O(N)$ for the map.

### Q4: [Output Prediction] What does this buggy code produce for `[3, 1, 2]`?
```cpp
for (int i = 0; i < n; ++i) {        // LEFT-to-RIGHT (wrong direction for this approach)
    while (!st.empty() && st.top() <= nums[i]) st.pop();
    nge[i] = st.empty() ? -1 : st.top();
    st.push(nums[i]);
}
```
**Answer:** This is actually computing **Previous Greater Element (PGE)**, not NGE! Processing left-to-right, the stack top represents elements seen BEFORE index $i$, so we're finding the previous greater, not the next greater. For `[3,1,2]`: PGE = `[-1, 3, 3]`. The correct NGE = `[-1, 2, -1]`.

### Q5: [Extension] How would you modify NGE to find the "Next Greater or Equal" element?
**Answer:** Change the pop condition from `st.top() <= nums[i]` to `st.top() < nums[i]`. Now we only pop elements strictly less than current, so elements equal to current are not popped and survive as valid candidates. This gives Next Greater or Equal.

### Q6: [Complexity] Prove the O(N) time bound despite the nested while loop.
**Answer:** Each element is pushed into the stack exactly once and popped at most once. The while loop does at most one pop per element across the entire algorithm. Total push operations: $N$. Total pop operations: at most $N$. Total work = $O(N)$. The nested loop is misleading — it does NOT give $O(N^2)$.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Hint |
|---|---------|----------|
| 496 | Next Greater Element I | Hash map + NGE on nums2 |
| 503 | Next Greater Element II | Circular + modulo trick |
| 739 | Daily Temperatures | Store indices, compute distances |
| 901 | Online Stock Span | PGE-left = span accumulation |
| 84 | Largest Rectangle in Histogram | PSE from both sides |

---

## 🔗 Cross-Topic Connections

- **Stock Span:** PGE-left variant with span counting.
- **Largest Histogram:** Uses PSE-left and NSE-right to find boundaries.
- **Trapping Rainwater:** Uses prefix max arrays which can be computed with monotonic stack style logic.
- **Circular Array:** NGE-II extends this with modulo indexing over 2N.

---

## ⚡ 2-Minute Revision Flash Card

- **NGE right-to-left:** monotonic decreasing stack → pop all ≤ current → top is NGE.
- **Left-to-right alternative:** maintain "unresolved" stack, pop when you find a greater element.
- **Store indices not values** when you need position-based answers (distances).
- **Pop condition:** `st.top() <= nums[i]` for strictly greater; `st.top() < nums[i]` for ≥.
- **Initialize result to -1** — default when no greater element exists.
