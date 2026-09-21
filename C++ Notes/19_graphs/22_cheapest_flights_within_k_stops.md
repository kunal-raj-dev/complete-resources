# Lecture 132: Cheapest Flights Within K Stops (LeetCode 787)

> **One-Line Purpose:** Find the cheapest price from source to destination with at most $K$ intermediate stops using a Modified BFS / Dijkstra approach.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #132  
> **Video ID:** `CLmykzpeCCs`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=CLmykzpeCCs)  
> **Duration:** 30:29  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Understand why standard Dijkstra fails when edge limits (number of stops) are introduced.
- Learn to order graph traversal by "stops" (level) rather than "cost" to strictly enforce the $K$ constraint.
- Master modifying BFS with state tuples `(stops, node, cost)`.
- See how relaxation logic changes when multiple constrained pathways to a node exist.

---

## 🧠 Core Intuition — Why This Works

If you use pure **Dijkstra's Algorithm**, you prioritize the absolute cheapest path. But what if the cheapest path takes 10 stops, and your limit $K$ is 2? Dijkstra might permanently mark the destination node as "visited" using the cheap 10-stop path, completely ignoring a slightly more expensive 2-stop path that actually satisfies the constraint.

**The Solution:**
Instead of prioritizing by *cost* (using a Priority Queue / Min-Heap), we prioritize by *stops* (using a standard Queue / BFS). 
Since every jump costs exactly 1 stop, a standard queue guarantees we explore the graph purely level-by-level (0 stops, then 1 stop, then 2 stops).
We keep a `dist` array to record the cheapest cost to reach node `v`. We ONLY push a new path to `v` onto the queue if it improves the cost we've seen so far, AND it's within the stop limit.

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Within K steps/stops/jumps"**: Immediate red flag that standard Dijkstra is wrong. You need level-by-level BFS.
- **"Cheapest / Shortest path with an extra constraint"**: Often requires augmenting the queue payload (e.g., passing state `(stops, node, cost)` instead of just `(cost, node)`).

---

## 📐 Algorithm Walk-Through

1. **Build Adjacency List**: `vector<vector<pair<int, int>>> adj` where `adj[u]` contains `{v, weight}`.
2. **Initialize Distance Array**: `vector<int> dist(n, INT_MAX)`. Set `dist[src] = 0`.
3. **Initialize Standard Queue**: `queue<tuple<stops, node, current_cost>>`. Push `{0, src, 0}`.
4. **BFS Traversal**:
   - Loop while queue is not empty:
     - Pop `{stops, u, cost}`.
     - **Optimization**: If `stops > k`, we cannot take any more flights from this path. `continue`.
     - Iterate through neighbors `v` with flight cost `weight`.
     - **Relaxation**: If `cost + weight < dist[v]`, we found a cheaper way to reach `v` within the allowable stops!
       - Update `dist[v] = cost + weight`.
       - Push `{stops + 1, v, cost + weight}` to the queue.
5. **Result**: After BFS, if `dist[dst] == INT_MAX`, return `-1` (unreachable within $K$ stops). Else, return `dist[dst]`.

---

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <queue>
#include <climits>
#include <iostream>

using namespace std;

class SolutionCheapestFlights {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        vector<vector<pair<int, int>>> adj(n);
        for (const auto& f : flights) {
            adj[f[0]].push_back({f[1], f[2]});
        }

        // Queue stores: pair<stops, pair<u, currentCost>>
        // A standard FIFO queue guarantees monotonically increasing stops (level order).
        queue<pair<int, pair<int, int>>> q;
        vector<int> dist(n, INT_MAX);

        q.push({0, {src, 0}});
        dist[src] = 0;

        while (!q.empty()) {
            auto [stops, nodeCost] = q.front();
            auto [u, cost] = nodeCost;
            q.pop();

            // If we've reached the stop limit, we can't take outgoing flights from here.
            // (Note: K stops means K+1 flights/edges).
            if (stops > k) continue;

            for (const auto& edge : adj[u]) {
                int v = edge.first;
                int weight = edge.second;

                // Only push if it offers a cheaper path to v
                if (cost + weight < dist[v]) {
                    dist[v] = cost + weight;
                    q.push({stops + 1, {v, cost + weight}});
                }
            }
        }

        return dist[dst] == INT_MAX ? -1 : dist[dst];
    }
};

int main() {
    // 0->1 (100), 1->2 (100), 2->0 (100), 1->3 (600), 2->3 (200)
    vector<vector<int>> flights = {{0, 1, 100}, {1, 2, 100}, {2, 0, 100}, {1, 3, 600}, {2, 3, 200}};
    SolutionCheapestFlights solver;
    
    // 0->1->3 costs 700 (1 stop). 0->1->2->3 costs 400 (2 stops).
    // With K=1, 0->1->3 is the only valid path to destination.
    cout << "Cheapest flight (K=1): " << solver.findCheapestPrice(4, flights, 0, 3, 1) << endl; // Output: 700
    
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Graph:** `0->1 (100)`, `1->2 (100)`, `1->3 (600)`, `2->3 (200)`.
**Goal:** `src = 0`, `dst = 3`, `k = 1`.
`dist` array = `[0, \infty, \infty, \infty]`
`Q` = `[(stops:0, node:0, cost:0)]`

**Step 1:**
- Pop `(0, 0, 0)`. `stops (0) <= 1`.
- Neighbors of `0`: `1` (cost 100).
- `0 + 100 < dist[1](\infty)`. Update `dist[1] = 100`.
- Push `(1, 1, 100)`. `Q = [(1, 1, 100)]`.

**Step 2:**
- Pop `(1, 1, 100)`. `stops (1) <= 1`.
- Neighbors of `1`: `2` (cost 100), `3` (cost 600).
- For `2`: `100 + 100 = 200 < dist[2](\infty)`. Update `dist[2] = 200`. Push `(2, 2, 200)`.
- For `3`: `100 + 600 = 700 < dist[3](\infty)`. Update `dist[3] = 700`. Push `(2, 3, 700)`.
- `Q = [(2, 2, 200), (2, 3, 700)]`.
- `dist = [0, 100, 200, 700]`.

**Step 3:**
- Pop `(2, 2, 200)`. `stops (2) > k (1)`. `continue` (skip neighbors).
- Pop `(2, 3, 700)`. `stops (2) > k (1)`. `continue` (skip neighbors).

**End:**
- Queue empty. `dist[3] = 700`. Return 700.
*(Notice the cheaper path `0->1->2->3` costing 400 was blocked because reaching `2` took 2 edges/1 stop, making outgoing edges exceed $K$).*

---

## ⚠️ Common Interview Mistakes

1. **Using Priority Queue**: A `priority_queue` sorted by cost will explore paths with the smallest total cost first, even if they have many stops. This breaks the level-order guarantee, causing extreme complication and often Wrong Answers. Stick to a simple `std::queue`.
2. **Missing `stops > k` Condition**: The limit $K$ means we can take AT MOST $K$ intermediate stops. This equates to $K+1$ edges. If the popped node already took $K+1$ edges (stops > $K$), we CANNOT extend any edges from it!
3. **Updating `dist` Incorrectly**: Since we use BFS, multiple paths might reach node $v$ at the same level. Always push to the queue ONLY if the new path strictly improves `dist[v]`.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(K \times E)$ or $O(V + E)$ in the worst-case BFS without a dense cycle limit. We explore each level, bounded by $K$ levels and $E$ edges.
- **Space Complexity:** $O(V + E)$ for the adjacency list. $O(V)$ for the queue and `dist` array. Total: $O(V + E)$.

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Can this be solved with Bellman-Ford?
**Answer:** Yes! Bellman-Ford naturally computes shortest paths step-by-step (edge-by-edge). If you run the outer relaxation loop exactly $K+1$ times, you will get the shortest paths using at most $K+1$ edges. You just need to ensure you use a temporary `dist` array each iteration so you don't use multi-edge jumps within a single iteration.

### Q2: What if there are negative edge weights?
**Answer:** The BFS approach still works safely because we limit depth strictly to $K+1$ levels. It will naturally prevent infinite looping in negative cycles, as execution terminates at depth $K$.

### Q3: Why don't we need a `visited` array here?
**Answer:** We are implicitly preventing loops by the condition `cost + weight < dist[v]`. A loop would only be traversed again if it somehow reduced the total path cost. Because edge weights are non-negative, loops only add cost, so `dist` relaxation inherently prevents revisiting cycles.

### Q4: If $K$ is very large (e.g., $K = V$), is BFS still better than Dijkstra?
**Answer:** If $K \ge V-1$, the constraint is essentially removed. In that case, standard Dijkstra with a Priority Queue is $O(E \log V)$, which is much faster than the worst-case $O(V \times E)$ of Bellman-Ford or this modified BFS.

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 743: Network Delay Time](https://leetcode.com/problems/network-delay-time/)** — Standard Dijkstra (no step limit).
2. **[Leetcode 1928: Minimum Cost to Reach Destination in Time](https://leetcode.com/problems/minimum-cost-to-reach-destination-in-time/)** — Instead of K stops limit, you have a max time limit. Similar state-tuple DP/Graph approach.

---

## 🔗 Cross-Topic Connections
- **Dynamic Programming (DP with States):** This BFS approach is mathematically equivalent to solving the DP: `dp[k][v] = min cost to reach v using k edges`.
- **Bellman-Ford Algorithm:** Bellman-Ford's core mechanism is tracking paths by edge counts.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Shortest path with at most $K$ stops ($K+1$ edges).
- **Core Trap:** Dijkstra doesn't work out-of-the-box because it prioritizes cost, ignoring step limits.
- **Solution:** Level-order BFS using a standard `queue`.
- **State Tuple:** `(stops, node, cost)`.
- **Pruning:** `if (stops > k) continue;`
- **Relaxation:** Only push to queue if `cost + weight < dist[v]`.
- **Time / Space:** $O(E \times K)$ Time | $O(V + E)$ Space.
