# Lecture 138: DP 2: Climbing Stairs (LeetCode 70)

> **One-Line Purpose:** Count total distinct ways to reach step $N$ by taking 1 or 2 steps via Fibonacci state transitions.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #138  
> **Video ID:** `3GzA0mz6wp0`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=3GzA0mz6wp0)  
> **Duration:** 26:26  
> **Status:** AUDITED  

---

## 🔵 Optimal $O(1)$ Space Implementation

```cpp
class SolutionClimbingStairs {
public:
    int climbStairs(int n) {
        if (n <= 2) return n;

        int prev2 = 1; // ways(1)
        int prev1 = 2; // ways(2)

        for (int i = 3; i <= n; i++) {
            int curr = prev1 + prev2;
            prev2 = prev1;
            prev1 = curr;
        }

        return prev1;
    }
};
```
- **Time Complexity:** $O(N)$. Space Complexity: $O(1)$.
