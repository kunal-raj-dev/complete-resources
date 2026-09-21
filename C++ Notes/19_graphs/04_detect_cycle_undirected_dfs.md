# Lecture 114: Detect Cycle in Undirected Graph using DFS

> **One-Line Purpose:** Identify back-edges in an undirected graph by comparing visited neighbor states against the immediate parent node.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #114  
> **Video ID:** `OZClCpPQDR4`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=OZClCpPQDR4)  
> **Duration:** 19:45  
> **Status:** AUDITED  

---

## 🔵 Implementation

```cpp
#include <vector>
using namespace std;

bool isCycleDFS(int node, int parent, const vector<vector<int>>& adj, vector<bool>& visited) {
    visited[node] = true;

    for (int neighbor : adj[node]) {
        if (!visited[neighbor]) {
            if (isCycleDFS(neighbor, node, adj, visited)) return true;
        } else if (neighbor != parent) {
            // Neighbor visited and not parent => back-edge => cycle!
            return true;
        }
    }
    return false;
}

bool hasCycle(int V, const vector<vector<int>>& adj) {
    vector<bool> visited(V, false);
    for (int i = 0; i < V; i++) {
        if (!visited[i]) {
            if (isCycleDFS(i, -1, adj, visited)) return true;
        }
    }
    return false;
}
```
