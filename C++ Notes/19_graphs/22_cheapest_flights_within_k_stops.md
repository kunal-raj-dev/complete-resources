# Lecture 132: Cheapest Flights Within K Stops (LeetCode 787)

> **One-Line Purpose:** Find shortest path bounded by at most $K$ intermediate stops using modified BFS with level tracking.

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

## 🔵 Complete Implementation

```cpp
#include <vector>
#include <queue>
#include <climits>
using namespace std;

class SolutionCheapestFlights {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        vector<vector<pair<int, int>>> adj(n);
        for (auto& f : flights) adj[f[0]].push_back({f[1], f[2]});

        vector<int> dist(n, INT_MAX);
        dist[src] = 0;

        // Queue: <stops, <node, cost>>
        queue<pair<int, pair<int, int>>> q;
        q.push({0, {src, 0}});

        while (!q.empty()) {
            auto [stops, p] = q.front();
            auto [u, cost] = p;
            q.pop();

            if (stops > k) continue;

            for (auto& edge : adj[u]) {
                int v = edge.first, price = edge.second;
                if (cost + price < dist[v]) {
                    dist[v] = cost + price;
                    q.push({stops + 1, {v, dist[v]}});
                }
            }
        }

        return (dist[dst] == INT_MAX) ? -1 : dist[dst];
    }
};
```
