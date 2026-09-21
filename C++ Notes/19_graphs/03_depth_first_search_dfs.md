# Lecture 113: Depth-First Search (DFS) Traversal in Graphs

> **One-Line Purpose:** Traverse graph components to terminal depths using recursive call stack activation records and backtracking.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #113  
> **Video ID:** `3czYbhac160`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=3czYbhac160)  
> **Duration:** 14:03  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

```cpp
#include <vector>
using namespace std;

void dfs(int node, const vector<vector<int>>& adj, vector<bool>& visited, vector<int>& res) {
    visited[node] = true;
    res.push_back(node);

    for (int neighbor : adj[node]) {
        if (!visited[neighbor]) {
            dfs(neighbor, adj, visited, res);
        }
    }
}

vector<int> dfsOfGraph(int V, const vector<vector<int>>& adj) {
    vector<int> res;
    vector<bool> visited(V, false);

    for (int i = 0; i < V; i++) {
        if (!visited[i]) {
            dfs(i, adj, visited, res);
        }
    }
    return res;
}
```
- **Time Complexity:** $O(V + E)$.
- **Space Complexity:** $O(V)$ recursion call stack.
