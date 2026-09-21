# Lecture 115: Detect Cycle in Undirected Graph using BFS

> **One-Line Purpose:** Detect cross-edges indicating undirected cycles via BFS queue tuples `(node, parent)`.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #115  
> **Video ID:** `MIjOkApZ39g`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=MIjOkApZ39g)  
> **Duration:** 18:23  
> **Status:** AUDITED  

---

## 🔵 Implementation

```cpp
#include <vector>
#include <queue>
using namespace std;

bool isCycleBFS(int src, const vector<vector<int>>& adj, vector<bool>& visited) {
    queue<pair<int, int>> q; // <node, parent>
    visited[src] = true;
    q.push({src, -1});

    while (!q.empty()) {
        auto [node, parent] = q.front();
        q.pop();

        for (int neighbor : adj[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.push({neighbor, node});
            } else if (neighbor != parent) {
                return true;
            }
        }
    }
    return false;
}
```
