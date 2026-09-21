# Lecture 144: DP 8: 0/1 Knapsack Problem: Recursion to 1D Space Optimization

> **One-Line Purpose:** Master the 0/1 Knapsack optimization problem from exponential recursive choices ($O(2^N)$) to 2D DP and 1D reverse-capacity space optimization.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #144  
> **Video ID:** `tEW-zDckvFw`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=tEW-zDckvFw)  
> **Duration:** 45:03  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- State transition: for item $i$, decide whether to **pick** or **not pick**.
- 2D Tabulation: `dp[i][w]` stores max value using first $i$ items with capacity $w$.
- The 1D Space Optimization trick: why iterating capacity $w$ in **reverse order** (`W` down to `wt[i]`) prevents using the same item multiple times.

---

## 🔵 Level 3: 1D Space-Optimized Implementation ($O(W)$ Space)

```cpp
#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;

class SolutionKnapsack {
public:
    int knapSack(int W, const vector<int>& wt, const vector<int>& val, int n) {
        // 1D DP array of size W + 1 initialized to 0
        vector<int> dp(W + 1, 0);

        for (int i = 0; i < n; i++) {
            // CRUCIAL: Iterate capacity backwards from W down to wt[i]!
            // This ensures dp[w - wt[i]] represents values from the PREVIOUS item row,
            // preventing the current item from being counted more than once.
            for (int w = W; w >= wt[i]; w--) {
                dp[w] = max(dp[w], val[i] + dp[w - wt[i]]);
            }
        }

        return dp[W];
    }
};

int main() {
    SolutionKnapsack sol;
    vector<int> val = {60, 100, 120};
    vector<int> wt = {10, 20, 30};
    int W = 50;
    cout << "Max Knapsack Value: " << sol.knapSack(W, wt, val, val.size()) << endl; // Output: 220
    return 0;
}
```
- **Time Complexity:** $O(N \times W)$ pseudo-polynomial time.
- **Space Complexity:** $O(W)$ strictly — 1D buffer.
