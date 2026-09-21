# Lecture 143: Fractional Knapsack Algorithm: Greedy Method

> **One-Line Purpose:** Maximize total knapsack value when items can be broken into fractional units by greedily sorting items by value-to-weight ratio in $O(N \log N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #143  
> **Video ID:** `yggezlvUN2w`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=yggezlvUN2w)  
> **Duration:** 16:33  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Contrast the Greedy approach of Fractional Knapsack vs the DP approach of 0/1 Knapsack.
- Understand how sorting by a composite metric (`value / weight`) leads to a mathematically optimal result.
- Master custom sorting comparators in C++.
- Learn how to handle floating-point division and capacities precisely.

---

## 🧠 Core Intuition — Why This Works

You have a bag that holds 50kg. You are in a grocery store. Do you fill the bag with expensive saffron ($10,000/kg) or cheap potatoes ($2/kg)? 
Obviously, the saffron. You want the highest **"Bang for your Buck"**. 
In math terms, this is the **Value-to-Weight Ratio**.

**Why Greedy Works Here:**
Because we are allowed to take *fractions* of an item, there is absolutely no penalty for taking the highest density item until it runs out, then taking the next highest, and so on. If we hit the weight limit of the bag midway through an item, we can just cut that item and take exactly the amount that fills the bag perfectly. No space is wasted.

**Why Greedy FAILS for 0/1 Knapsack:**
If you CANNOT slice items, taking the highest density item might leave a gap in your bag (say, 2kg left) that goes completely wasted, whereas taking a slightly lower density item that perfectly fits the bag might yield more total value.

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Items can be broken down", "Divisible"**: Absolute giveaway for Fractional Knapsack (Greedy).
- **"Maximize profit / minimize cost" with a capacity constraint AND divisible goods**: (e.g., loading liquids into a tanker, buying fractional shares).

---

## 📐 Algorithm Walk-Through

1. **Calculate Ratios**: For each item, compute its density: `Ratio = Value / Weight`.
2. **Sort**: Sort all items in descending order based on this ratio. 
3. **Iterate & Accumulate**:
   - Set `current_weight = 0`, `total_value = 0.0`.
   - Loop through the sorted items:
     - If adding the entire item's weight keeps `current_weight <= Capacity (W)`:
       - Add the whole item. `current_weight += item.weight`, `total_value += item.value`.
     - Else (the bag will overflow if we take all of it):
       - Calculate remaining space: `remain = W - current_weight`.
       - Add the fractional value: `total_value += remain * (item.value / item.weight)`.
       - `break` the loop, because the bag is now 100% full.
4. **Return**: The `total_value`.

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct Item {
    int value;
    int weight;
};

class FractionalKnapsack {
public:
    static double getMaxValue(int W, vector<Item>& items) {
        // Sort items by value/weight ratio descending
        sort(items.begin(), items.end(), [](const Item& a, const Item& b) {
            double r1 = (double)a.value / a.weight;
            double r2 = (double)b.value / b.weight;
            return r1 > r2; // Descending order
        });

        double totalValue = 0.0;
        int currentWeight = 0;

        for (const auto& item : items) {
            if (currentWeight + item.weight <= W) {
                // Take item entirely
                currentWeight += item.weight;
                totalValue += item.value;
            } else {
                // Take fractional portion to exactly fill the knapsack
                int remain = W - currentWeight;
                totalValue += ((double)item.value / item.weight) * remain;
                break; // Knapsack is full
            }
        }

        return totalValue;
    }
};

int main() {
    int W = 50;
    // Items: {value, weight}
    vector<Item> items = {{60, 10}, {100, 20}, {120, 30}};
    
    // Ratios: 
    // Item 0: 60/10 = 6
    // Item 1: 100/20 = 5
    // Item 2: 120/30 = 4
    
    cout << "Max Fractional Value: " << FractionalKnapsack::getMaxValue(W, items) << endl; 
    // Output: 240.0
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Capacity `W` = 50**
Items = `[{60, 10}, {100, 20}, {120, 30}]`

1. **Calculate Ratios and Sort**:
   - Item A: `60/10 = 6`
   - Item B: `100/20 = 5`
   - Item C: `120/30 = 4`
   - Already sorted: A, B, C.

2. **Iteration**:
   - `currW = 0, totalV = 0.0`
   - **Look at A**: weight 10. `currW + 10 = 10 <= 50`. 
     - Add A. `currW = 10`, `totalV = 60`.
   - **Look at B**: weight 20. `currW + 20 = 30 <= 50`.
     - Add B. `currW = 30`, `totalV = 60 + 100 = 160`.
   - **Look at C**: weight 30. `currW + 30 = 60 > 50`. OVERFLOW!
     - Space remaining = `50 - 30 = 20`.
     - Value ratio of C = 4.
     - Add fraction of C = `20 * 4 = 80`.
     - `totalV = 160 + 80 = 240`.
     - Break.

**Result:** 240.0.

---

## ⚠️ Common Interview Mistakes

1. **Integer Division Truncation**: When calculating the ratio `value / weight`, if both are integers, C++ does integer division. `5 / 2 = 2` instead of `2.5`. You MUST cast to double `(double)value / weight` to get the correct ratio for sorting.
2. **Precision Loss in Sorting**: Comparing floating-point numbers can be flaky, but for ratios it's usually fine. To be extremely robust against floating-point errors, you can cross-multiply: `a.value * b.weight > b.value * a.weight` instead of `a.value / a.weight > b.value / b.weight` (careful of integer overflow if values/weights are large).
3. **Not handling the fractional logic correctly**: People often multiply `remain * (item.weight / item.value)` (inverted). Double check your dimensional analysis! Value = Weight * (Value / Weight).

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N \log N)$ due to the sorting step. The iteration itself takes $O(N)$.
- **Space Complexity:** $O(1)$ auxiliary memory (ignoring the memory used by the sorting algorithm, which can be $O(\log N)$ for QuickSort in standard library).

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Is the Greedy Approach ever optimal for 0/1 Knapsack?
**Answer:** Generally, no. However, if the items happen to have perfectly divisible sizes or very specific properties (like weight being identical for all items), greedy might work. But as a general rule, it fails unless fractions are allowed.

### Q2: What if we have multiple items with the exact same Value/Weight ratio? Does their order matter?
**Answer:** No. Since they have the same density, replacing $X$ kg of one with $X$ kg of another yields the exact same value.

### Q3: How do you prevent floating-point accuracy issues during the sort?
**Answer:** As mentioned, cross-multiplication: 
```cpp
return (long long)a.value * b.weight > (long long)b.value * a.weight;
```
This is computationally cheaper (no division) and perfectly accurate.

### Q4: What is the optimal data structure if items are continuously arriving in a stream and we have multiple knapsacks to fill?
**Answer:** A Max-Heap (Priority Queue) ordered by the value-to-weight ratio. As an item arrives, push it in $O(\log N)$. When a knapsack needs filling, pop the top elements.

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 1710: Maximum Units on a Truck](https://leetcode.com/problems/maximum-units-on-a-truck/)** — Exact replica of Fractional Knapsack, disguised with boxes and units.
2. **[Leetcode 135: Candy](https://leetcode.com/problems/candy/)** — Another classic Greedy problem that requires localized optimal choices.
3. **[Leetcode 416: Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/)** — DP Knapsack variant to study the contrast.

---

## 🔗 Cross-Topic Connections
- **Greedy Algorithms vs Dynamic Programming:** This is the quintessential problem used worldwide to teach the boundary where Greedy stops working and DP becomes necessary.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Maximize total value, fractions of items allowed.
- **Rule:** GREEDY wins. Sort by `Value / Weight`.
- **Trap:** Integer division. Use `(double)v/w` or cross-multiply `v1*w2 > v2*w1`.
- **Logic:** Take full items as long as they fit. For the first item that doesn't fit, take `remaining_capacity * ratio` and stop.
- **Time/Space:** $O(N \log N)$ Time | $O(1)$ Space.
