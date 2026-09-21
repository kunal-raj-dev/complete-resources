# Lecture 125: Bellman-Ford Algorithm: Negative Weight Cycles

> **One-Line Purpose:** Find shortest paths on graphs with negative edge weights and detect negative cycles by relaxing all edges $V - 1$ times in $O(V \times E)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #125  
> **Video ID:** `3rFHlbJ7qKc`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=3rFHlbJ7qKc)  
> **Duration:** 23:38  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

```cpp
#include <vector>
#include <climits>
using namespace std;

struct Edge {
    int u, v, weight;
};

vector<int> bellmanFord(int V, const vector<Edge>& edges, int src, bool& hasNegativeCycle) {
    vector<int> dist(V, 1e8);
    dist[src] = 0;

    // Relax all edges V - 1 times
    for (int i = 1; i <= V - 1; i++) {
        for (const auto& e : edges) {
            if (dist[e.u] != 1e8 && dist[e.u] + e.weight < dist[e.v]) {
                dist[e.v] = dist[e.u] + e.weight;
            }
        }
    }

    // N-th relaxation to detect negative weight cycles
    hasNegativeCycle = false;
    for (const auto& e : edges) {
        if (dist[e.u] != 1e8 && dist[e.u] + e.weight < dist[e.v]) {
            hasNegativeCycle = true;
            break;
        }
    }

    return dist;
}
```
- **Time Complexity:** $O(V \times E)$.
- **Space Complexity:** $O(V)$.
