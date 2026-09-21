# Lecture 84: Gas Station: Circular Greedy Tour (LeetCode 134)

> **One-Line Purpose:** Solve the circular petroleum circuit problem in a single pass using total surplus deficit proofs and greedy starting station reset.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #84  
> **Video ID:** `SmTow5Ht4iU`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=SmTow5Ht4iU)  
> **Duration:** 22:16  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Greedy Implementation

```cpp
#include <vector>
#include <numeric>
using namespace std;

class SolutionGasStation {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        int totalGas = 0, totalCost = 0;
        for (int g : gas) totalGas += g;
        for (int c : cost) totalCost += c;

        if (totalGas < totalCost) return -1;

        int startStation = 0;
        int currentTank = 0;

        for (int i = 0; i < gas.size(); i++) {
            currentTank += gas[i] - cost[i];

            if (currentTank < 0) {
                startStation = i + 1;
                currentTank = 0;
            }
        }

        return startStation;
    }
};
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$.
