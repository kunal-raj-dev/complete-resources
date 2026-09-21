# Lecture 131: Min Cost to Connect All Points (LeetCode 1584)

> **One-Line Purpose:** Connect 2D coordinate points with minimum Manhattan distance using Prim's or Kruskal's MST algorithm.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #131  
> **Video ID:** `mEx8JJQJUs8`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=mEx8JJQJUs8)  
> **Duration:** 21:16  
> **Status:** AUDITED  

---

## 🔵 Implementation (Prim's Algorithm)

```cpp
#include <vector>
#include <queue>
#include <cmath>
using namespace std;

class SolutionMinCostPoints {
public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        int n = points.size();
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        vector<bool> inMST(n, false);

        pq.push({0, 0});
        int totalCost = 0, connected = 0;

        while (connected < n) {
            auto [cost, u] = pq.top();
            pq.pop();

            if (inMST[u]) continue;

            inMST[u] = true;
            totalCost += cost;
            connected++;

            for (int v = 0; v < n; v++) {
                if (!inMST[v]) {
                    int dist = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1]);
                    pq.push({dist, v});
                }
            }
        }
        return totalCost;
    }
};
```
