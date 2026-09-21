# Lecture 127: Prim's Algorithm: Minimum Spanning Tree (MST)

> **One-Line Purpose:** Construct an MST on a connected weighted graph in $O(E \log V)$ time by greedily expanding the visited cut boundary via a Min-Heap.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #127  
> **Video ID:** `Sflh1z6cIMk`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=Sflh1z6cIMk)  
> **Duration:** 26:07  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

```cpp
#include <vector>
#include <queue>
using namespace std;

int spanningTreePrim(int V, const vector<vector<pair<int, int>>>& adj) {
    // Min-heap: <weight, node>
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    vector<bool> inMST(V, false);

    pq.push({0, 0});
    int totalMSTWeight = 0;

    while (!pq.empty()) {
        auto [wt, u] = pq.top();
        pq.pop();

        if (inMST[u]) continue;

        inMST[u] = true;
        totalMSTWeight += wt;

        for (auto const& edge : adj[u]) {
            int v = edge.first;
            int edgeWt = edge.second;
            if (!inMST[v]) {
                pq.push({edgeWt, v});
            }
        }
    }
    return totalMSTWeight;
}
```
