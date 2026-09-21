# Lecture 124: Dijkstra's Algorithm: Single-Source Shortest Path

> **One-Line Purpose:** Compute shortest paths from a source vertex on non-negative weighted graphs using a greedy Min-Heap in $O((V + E) \log V)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #124  
> **Video ID:** `8gYBHjtjWBI`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=8gYBHjtjWBI)  
> **Duration:** 35:20  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

```cpp
#include <vector>
#include <queue>
#include <climits>
using namespace std;

vector<int> dijkstra(int V, const vector<vector<pair<int, int>>>& adj, int src) {
    vector<int> dist(V, INT_MAX);
    // Min-heap: <distance, node>
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;

    dist[src] = 0;
    pq.push({0, src});

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();

        if (d > dist[u]) continue; // Stale queue entry

        for (auto const& edge : adj[u]) {
            int v = edge.first;
            int weight = edge.second;

            // Relaxation Step
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```
- **Time Complexity:** $O((V + E) \log V)$.
- **Space Complexity:** $O(V)$ distances + heap.
