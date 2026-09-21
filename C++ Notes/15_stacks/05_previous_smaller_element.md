# Lecture 72: Previous Smaller Element

> **One-Line Purpose:** Find the nearest strictly smaller element to the left for each array element using a Monotonic Increasing Stack scanned from left to right in $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #72  
> **Video ID:** `WnjUfBn9nZM`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=WnjUfBn9nZM)  
> **Duration:** 09:24  
> **Status:** AUDITED  

---

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <stack>
#include <iostream>

using namespace std;

class PreviousSmallerElement {
public:
    static vector<int> solve(const vector<int>& nums) {
        int n = nums.size();
        vector<int> pse(n, -1);
        stack<int> st;

        for (int i = 0; i < n; ++i) {
            while (!st.empty() && st.top() >= nums[i]) {
                st.pop();
            }

            if (!st.empty()) {
                pse[i] = st.top();
            }

            st.push(nums[i]);
        }

        return pse;
    }
};

int main() {
    vector<int> arr = {4, 5, 2, 10, 8};
    vector<int> res = PreviousSmallerElement::solve(arr);
    cout << "Previous Smaller: ";
    for (int x : res) cout << x << " "; // Output: -1 4 -1 2 2
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

**Previous Smaller Element (PSE)** = for each element, find the nearest element to its **left** that is strictly smaller. This is the mirror of NGE but going leftward.

**Why Monotonic Increasing Stack?** Process left-to-right. Maintain a stack where elements are always in increasing order from bottom to top. When processing `nums[i]`:
- Pop elements ≥ `nums[i]` — they are bigger than the current element and cannot be the PSE for anything to the right (the current smaller element "dominates" them out).
- Stack top (if non-empty) is the nearest smaller element to the LEFT.

```
Array: [4, 5, 2, 10, 8]   (left-to-right scan)

i=0: val=4   Stack empty → PSE[0]=-1. Push 4.  Stack:[4]
i=1: val=5   top=4<5   → PSE[1]=4.  Push 5.  Stack:[4,5]
i=2: val=2   pop 5(5≥2), pop 4(4≥2), empty → PSE[2]=-1. Push 2. Stack:[2]
i=3: val=10  top=2<10  → PSE[3]=2.  Push 10. Stack:[2,10]
i=4: val=8   pop 10(10≥8), top=2<8 → PSE[4]=2.  Push 8.  Stack:[2,8]

Result: [-1, 4, -1, 2, 2]  ✓
```

---

## 🎯 Pattern Recognition — The Complete Monotonic Stack Map

| Problem | Scan Direction | Stack Order | Pop Condition |
|---------|---------------|-------------|---------------|
| NGE (right) | Right → Left | Decreasing | pop when `top ≤ current` |
| PGE (left) | Left → Right | Decreasing | pop when `top ≤ current` |
| NSE (right) | Right → Left | Increasing | pop when `top ≥ current` |
| PSE (left) | **Left → Right** | **Increasing** | **pop when `top ≥ current`** |

**Histogram connection:** Largest Rectangle in Histogram uses BOTH PSE-left and NSE-right to find the left and right boundaries for each bar's maximum rectangle.

---

## 🔍 Dry Run Trace

Array: `[3, 1, 4, 1, 5]`

```
i=0: val=3  Stack:[]  → PSE=-1. Push 3.  Stack:[3]
i=1: val=1  pop 3(≥1) Stack:[]  → PSE=-1. Push 1. Stack:[1]
i=2: val=4  top=1<4   → PSE=1.  Push 4.  Stack:[1,4]
i=3: val=1  pop 4(≥1), pop 1(≥1), Stack:[] → PSE=-1. Push 1. Stack:[1]
i=4: val=5  top=1<5   → PSE=1.  Push 5.  Stack:[1,5]

Result: [-1, -1, 1, -1, 1]
```

---

## ⚠️ Common Interview Mistakes

1. **Getting scan direction backwards:** PSE-Left scans LEFT-TO-RIGHT. NGE-Right scans RIGHT-TO-LEFT. Getting this wrong gives PGE or NSE instead.

2. **Off-by-one in strict vs non-strict:** "Strictly smaller" means pop when `top >= current`. If problem says "smaller or equal", pop when `top > current`.

3. **Not handling the case where stack is empty:** When stack is empty after popping, PSE = -1 (no smaller element to the left). Missing this gives garbage values.

4. **Confusing PSE with NSE:** PSE looks LEFT, NSE looks RIGHT. Same stack type (increasing), different scan direction.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] How does PSE relate to Largest Rectangle in Histogram?
**Answer:** In the histogram problem, for each bar at index $i$, the maximum rectangle with height `h[i]` extends leftward until it hits a bar shorter than `h[i]` (that's the PSE boundary) and rightward until it hits a bar shorter than `h[i]` (that's the NSE boundary). The width = `NSE_index[i] - PSE_index[i] - 1`. Computing both PSE and NSE with monotonic stacks gives the $O(N)$ solution.

### Q2: [Output Prediction] What is PSE for array `[5, 4, 3, 2, 1]` (strictly decreasing)?
**Answer:** For a strictly decreasing array, every element to the right is smaller than everything to its left. But PSE looks LEFT, so for element at index $i$, all elements to its left are LARGER. The stack will always be empty when we record PSE (since each new element causes all larger elements to be popped). Result: `[-1, -1, -1, -1, -1]`. All -1 because no element has a smaller element to its left.

### Q3: [Extension] How do you compute BOTH PSE and NSE for all elements in a single pass?
**Answer:** You can't do both in a true single pass with one stack. The standard approach is two separate O(N) passes: one left-to-right for PSE, one right-to-left for NSE. Total: O(N) time, O(N) space for both arrays. Alternatively, the single-pass histogram algorithm handles both implicitly — each pop event gives the NSE of the popped element, and the new stack top after popping gives the PSE.

### Q4: [Extension] What is "Previous Smaller or Equal" and how does it differ in implementation?
**Answer:** Change the pop condition from `st.top() >= nums[i]` to `st.top() > nums[i]`. Now we keep equal elements on the stack, so the top (after popping strictly greater elements) gives the previous element that is ≤ current. This is used in the Stock Span problem variant where ties are included in the span.

### Q5: [Complexity] Why is O(N) achievable when intuitively each element might be compared against many others?
**Answer:** Each element is pushed exactly once and popped at most once. Even though the while loop can do multiple pops for one element, summed across all $N$ iterations, total pops ≤ $N$. So total operations = pushes + pops ≤ $2N$ = $O(N)$. This is the amortized analysis — a single element might do many pops, but it "pays" for them with previous cheap pushes.

### Q6: [Design] How would you use PSE to solve the "Largest Rectangle in Histogram" problem?
**Answer:** For each bar $i$:
1. `left[i]` = PSE-left index of bar $i$ (first bar shorter than `h[i]` to the left), default to -1.
2. `right[i]` = NSE-right index of bar $i$ (first bar shorter than `h[i]` to the right), default to N.
3. Width = `right[i] - left[i] - 1`.
4. Area = `h[i] * width`.
5. Answer = max over all $i$.
This uses two monotonic stack passes, each O(N). Total O(N) time, O(N) space.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Hint |
|---|---------|----------|
| 84 | Largest Rectangle in Histogram | PSE-left + NSE-right boundaries |
| 85 | Maximal Rectangle | Apply histogram solution row by row |
| 496 | Next Greater Element I | Symmetric: NGE-right |
| 901 | Online Stock Span | PGE-left reframed as span |
| 907 | Sum of Subarray Minimums | PSE and NSE to count subarrays |

---

## 🔗 Cross-Topic Connections

- **Largest Rectangle in Histogram:** Directly uses PSE and NSE to find bar boundaries.
- **Stock Span:** PGE-Left (same stack type, different semantic: count vs index).
- **Sum of Subarray Minimums (907):** Each element is the minimum in some contiguous subarrays — boundaries defined by PSE and NSE.
- **Trapping Rainwater:** Can be solved using prefix and suffix max arrays which are analogous to monotonic array scans.

---

## ⚡ 2-Minute Revision Flash Card

- **PSE = Previous Smaller Element:** nearest strictly smaller element to the LEFT.
- **Algorithm:** Left-to-right scan, monotonic INCREASING stack, pop when `top ≥ current`.
- **Stack top after popping** = PSE of current element; push current.
- **Initialize to -1:** when stack is empty, no PSE exists.
- **Master combo:** PSE + NSE both needed for Largest Rectangle in Histogram.
