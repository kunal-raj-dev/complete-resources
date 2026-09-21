# Lecture 133: Bridges in Graph: Tarjan's Algorithm (LeetCode 1192)

> **One-Line Purpose:** Detect critical connection bridges whose removal increases connected components using DFS discovery times and low-link values in $O(V + E)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #133  
> **Video ID:** `6h1SucBNxgc`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=6h1SucBNxgc)  
> **Duration:** 32:36  
> **Status:** AUDITED  

---

## 🔵 Invariant & C++ Implementation
A tree edge `u -> v` is a **Bridge** if and only if:
$$\text{low}[v] > \text{tin}[u]$$
meaning node $v$ has zero back-edges to $u$ or any ancestor of $u$.

```cpp
#include <vector>
#include <algorithm>
using namespace std;

class SolutionTarjanBridges {
private:
    int timer = 1;

    void dfs(int u, int parent, const vector<vector<int>>& adj, vector<int>& tin, vector<int>& low, vector<bool>& vis, vector<vector<int>>& bridges) {
        vis[u] = true;
        tin[u] = low[u] = timer++;

        for (int v : adj[u]) {
            if (v == parent) continue;

            if (!vis[v]) {
                dfs(v, u, adj, tin, low, vis, bridges);
                low[u] = min(low[u], low[v]);

                // Bridge Condition
                if (low[v] > tin[u]) {
                    bridges.push_back({u, v});
                }
            } else {
                // Back-edge
                low[u] = min(low[u], tin[v]);
            }
        }
    }

public:
    vector<vector<int>> criticalConnections(int n, vector<vector<int>>& connections) {
        vector<vector<int>> adj(n);
        for (auto& c : connections) {
            adj[c[0]].push_back(c[1]);
            adj[c[1]].push_back(c[0]);
        }

        vector<int> tin(n), low(n);
        vector<bool> vis(n, false);
        vector<vector<int>> bridges;
        timer = 1;

        dfs(0, -1, adj, tin, low, vis, bridges);
        return bridges;
    }
};
```
- **Time Complexity:** $O(V + E)$.
- **Space Complexity:** $O(V)$.
