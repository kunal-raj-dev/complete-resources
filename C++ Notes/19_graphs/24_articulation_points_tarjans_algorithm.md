# Lecture 134: Articulation Points in Graph: Tarjan's Algorithm

> **One-Line Purpose:** Identify cut vertices whose removal disconnects the graph using DFS discovery times and low-link conditions.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #134  
> **Video ID:** `cn7pov3BEmg`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=cn7pov3BEmg)  
> **Duration:** 36:53  
> **Status:** AUDITED  

---

## 🔵 Articulation Point Invariant
Node $u$ is an **Articulation Point** if:
1. $u$ is not the DFS root and $\text{low}[v] \ge \text{tin}[u]$ for some child $v$.
2. $u$ is the DFS root and has $> 1$ independent DFS children.

```cpp
#include <vector>
#include <algorithm>
using namespace std;

void dfsAP(int u, int p, const vector<vector<int>>& adj, vector<int>& tin, vector<int>& low, vector<bool>& vis, vector<bool>& isAP, int& timer) {
    vis[u] = true;
    tin[u] = low[u] = timer++;
    int children = 0;

    for (int v : adj[u]) {
        if (v == p) continue;
        if (!vis[v]) {
            children++;
            dfsAP(v, u, adj, tin, low, vis, isAP, timer);
            low[u] = min(low[u], low[v]);

            if (p != -1 && low[v] >= tin[u]) isAP[u] = true;
        } else {
            low[u] = min(low[u], tin[v]);
        }
    }
    if (p == -1 && children > 1) isAP[u] = true;
}
```
