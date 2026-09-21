# Lecture 143: Fractional Knapsack: Greedy Paradigm

> **One-Line Purpose:** Maximize knapsack value when items can be subdivided into fractional parts using greedy value-to-weight ratio sorting.

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

## 🔵 Greedy Strategy & Complete Implementation

Items can be divided: always select items with the highest value density $\frac{\text{val}_i}{\text{weight}_i}$.

```cpp
#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;

struct Item {
    int value;
    int weight;
};

bool compareItems(const Item& a, const Item& b) {
    double r1 = (double)a.value / a.weight;
    double r2 = (double)b.value / b.weight;
    return r1 > r2; // Sort in descending order of value per unit weight
}

double fractionalKnapsack(int W, vector<Item>& items) {
    sort(items.begin(), items.end(), compareItems);

    double totalValue = 0.0;
    int currentWeight = 0;

    for (const auto& item : items) {
        if (currentWeight + item.weight <= W) {
            currentWeight += item.weight;
            totalValue += item.value;
        } else {
            int remain = W - currentWeight;
            totalValue += item.value * ((double)remain / item.weight);
            break; // Knapsack is fully packed
        }
    }

    return totalValue;
}
```
- **Time Complexity:** $O(N \log N)$ sorting time.
- **Space Complexity:** $O(1)$.
- **Crucial Distinction:** Greedy works **only** for Fractional Knapsack. For 0/1 Knapsack, greedy fails because an item must be taken in its entirety or left behind; DP is strictly required!
