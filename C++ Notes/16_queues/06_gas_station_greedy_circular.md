# Lecture 84: Gas Station: Circular Tour Problem (LeetCode 134)

> **One-Line Purpose:** Find the unique starting gas station from which a car can complete a full circular tour in $O(N)$ single-pass greedy time and $O(1)$ space.

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

## 🎯 Learning Objectives
- Formulate the Global Solvability Theorem for circular zero-sum games.
- Master the Local Skip Invariant to avoid $O(N^2)$ brute-force simulations.
- Understand why a single linear pass can determine a circular path without wrapping around manually.

---

## 🧠 Core Intuition — Why This Works

There are two massive mathematical shortcuts in this problem that reduce it from a complex $O(N^2)$ simulation into a trivial $O(N)$ pass.

**1. The Global Feasibility Theorem:**
If the total amount of gas available at all stations combined is less than the total cost of gas to drive around the entire circle, it is physically impossible to complete the loop, no matter where you start.
Conversely, if `total_gas >= total_cost`, a valid starting station **always exists**. (Assuming the solution is guaranteed to be unique if it exists, per problem description).

**2. The "Skip Ahead" Invariant (Greedy Choice):**
Suppose you start at station $A$, and you successfully travel through $B$, $C$, and $D$. But when trying to go from $D \to E$, you run out of gas! (Your tank hits negative).
Can you succeed by starting at $B$ instead? **NO.**
Because when you started at $A$, you arrived at $B$ with $\ge 0$ gas. Starting fresh at $B$ gives you *less* (or equal) gas than you had when passing through $B$ from $A$. If you couldn't make it to $E$ with a running start from $A$, you definitely can't make it starting from $B$, $C$, or $D$.
**Conclusion:** If you fail at $E$, the next potential starting candidate MUST be $E+1$. Every station between $A$ and $E$ is mathematically doomed to fail at or before $E$.

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Circular tour / circuit", "Car and gas", "Cost vs Reward array"**: Classic Gas Station.
- **"Find the starting point that guarantees never dipping below zero"**: Prefix sum arrays with greedy jump-aheads.

---

## 📐 Algorithm Walk-Through

1. Initialize `totalSurplus = 0` (tracks global feasibility).
2. Initialize `currentSurplus = 0` (tracks local tank since the current starting candidate).
3. Initialize `startIdx = 0`.
4. Loop `i` from $0$ to $N-1$:
   - Calculate `net = gas[i] - cost[i]`.
   - Add to both `totalSurplus += net` and `currentSurplus += net`.
   - **The Skip Invariant:** If `currentSurplus < 0`:
     - You just ran out of gas trying to *leave* station `i`.
     - None of the stations from `startIdx` to `i` can be the answer.
     - Set `startIdx = i + 1`.
     - Reset `currentSurplus = 0` (start fresh from the new candidate).
5. After the loop, if `totalSurplus < 0`, it's impossible. Return `-1`.
6. Else, return `startIdx`.

---

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <iostream>

using namespace std;

class SolutionGasStation {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        int totalSurplus = 0;   // Net gas across the entire circle
        int currentSurplus = 0; // Gas accumulated since the 'startIdx'
        int startIdx = 0;

        for (int i = 0; i < (int)gas.size(); ++i) {
            int net = gas[i] - cost[i];
            
            totalSurplus += net;
            currentSurplus += net;

            // If we run out of gas at station i...
            if (currentSurplus < 0) {
                // ...then NO station from startIdx to i can be the start.
                // The next viable candidate is i + 1.
                startIdx = i + 1;
                currentSurplus = 0; // Reset tank for the new candidate
            }
        }

        // If total gas >= total cost, the recorded startIdx is guaranteed to work
        return totalSurplus >= 0 ? startIdx : -1;
    }
};

int main() {
    SolutionGasStation solver;
    // Classic LeetCode example
    vector<int> gas = {1, 2, 3, 4, 5};
    vector<int> cost = {3, 4, 5, 1, 2};
    cout << "Starting Station Index: " << solver.canCompleteCircuit(gas, cost) << endl; 
    // Output: 3
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Input:** `gas = [1, 2, 3, 4, 5]`, `cost = [3, 4, 5, 1, 2]`
Net arrays (Gas - Cost) = `[-2, -2, -2, 3, 3]`

- `i = 0`: net = -2. 
  - `total = -2`, `current = -2`. 
  - `current < 0`. Tank empty! `startIdx = 1`. `current = 0`.
- `i = 1`: net = -2.
  - `total = -4`, `current = -2`.
  - `current < 0`. Tank empty! `startIdx = 2`. `current = 0`.
- `i = 2`: net = -2.
  - `total = -6`, `current = -2`.
  - `current < 0`. Tank empty! `startIdx = 3`. `current = 0`.
- `i = 3`: net = 3.
  - `total = -3`, `current = 3`. Tank has gas. Keep `startIdx = 3`.
- `i = 4`: net = 3.
  - `total = 0`, `current = 6`. Tank has gas. Keep `startIdx = 3`.

**Loop Ends.** 
`totalSurplus = 0`. Since `0 >= 0`, return `startIdx = 3`.

---

## ⚠️ Common Interview Mistakes

1. **Simulating the Wrap-Around**: Candidates often try to literally simulate going from $N-1$ back to $0$ using `i % N` in a nested loop. That makes the time complexity $O(N^2)$ and will Time Limit Exceed. The beauty of this algorithm is that the global `totalSurplus >= 0` check *implicitly guarantees* the wrap-around will succeed. No actual simulation is needed.
2. **Assuming positive net is enough**: If you just find the first station where `gas[i] - cost[i] > 0` and return it, you will fail. (e.g., net array `[1, -100, 100]`. Station 0 is positive, but will fail immediately at 1. Station 2 is the correct answer).

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$ single pass.
- **Space Complexity:** $O(1)$ auxiliary memory.

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Can there be multiple valid starting stations?
**Answer:** The classic LeetCode problem guarantees that *if* a solution exists, it is **unique**. If the problem allowed multiple solutions, this algorithm would just return the *first* valid starting station it encounters that doesn't fail before the end of the array.

### Q2: Why don't we need to check if the candidate `startIdx` can make it from $0$ to `startIdx - 1`?
**Answer:** Because of the `totalSurplus >= 0` check. Let the array be split into two parts: $A$ (from $0$ to `startIdx-1`) and $B$ (from `startIdx` to $N-1$). 
We know `net(A) + net(B) = totalSurplus`. We are given `totalSurplus >= 0`. Therefore, `net(A) + net(B) >= 0`.
We also know that we arrived at `startIdx` because part $A$ failed. Thus, `net(A) < 0`. 
If `net(B) + net(A) >= 0` and `net(A)` is negative, `net(B)` MUST be extremely positive (specifically, `net(B) >= -net(A)`). Therefore, the surplus we build up while driving through $B$ is mathematically guaranteed to be large enough to absorb the deficit of $A$ when we wrap around!

### Q3: How is this problem related to Maximum Subarray (Kadane's Algorithm)?
**Answer:** It's extremely similar! In Kadane's, if the running sum drops below 0, you reset the sum to 0 and start a new subarray. In Gas Station, if the running surplus drops below 0, you reset the surplus to 0 and designate a new `startIdx`. Both rely on the idea that a negative prefix ruins the total.

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 53: Maximum Subarray](https://leetcode.com/problems/maximum-subarray/)** — The foundational algorithm (Kadane's) that shares the exact same negative-reset logic.
2. **[Leetcode 238: Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/)** — Another problem that requires $O(N)$ time without division, leveraging prefix/suffix properties.

---

## 🔗 Cross-Topic Connections
- **Greedy Algorithms:** The local skip invariant is a pure greedy choice.
- **Prefix Sums:** We are essentially evaluating the running prefix sum of the `gas - cost` array.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Find start index for circular tour.
- **Core Invariant:** If `currentSurplus < 0` at station $i$, NO station from `start` to $i$ can be the answer. Next candidate is $i+1$.
- **Global Check:** If `totalSurplus < 0` at the end, return `-1`. Else return `start`.
- **Why no simulation?** If total gas $\ge$ total cost, the last candidate that survives to the end of the array is guaranteed to survive the wrap-around.
- **Time/Space:** $O(N)$ Time | $O(1)$ Space.
