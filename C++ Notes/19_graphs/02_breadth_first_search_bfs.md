# Lecture 112: Breadth-First Search (BFS) Traversal in Graphs

> **One-Line Purpose:** Traverse graph topologies level by level using a FIFO queue and visited boolean flags, handling disconnected components.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #112  
> **Video ID:** `scQITTLgFJo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=scQITTLgFJo)  
> **Duration:** 18:31  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

```cpp
#include <vector>
#include <queue>
using namespace std;

vector<int> bfsOfGraph(int V, vector<vector<int>>& adj) {
    vector<int> bfs;
    vector<bool> visited(V, false);

    for (int i = 0; i < V; i++) {
        if (!visited[i]) {
            queue<int> q;
            q.push(i);
            visited[i] = true;

            while (!q.empty()) {
                int node = q.front();
                q.pop();
                bfs.push_back(node);

                for (int neighbor : adj[node]) {
                    if (!visited[neighbor]) {
                        visited[neighbor] = true;
                        q.push(neighbor);
                    }
                }
            }
        }
    }
    return bfs;
}
```
- **Time Complexity:** $O(V + 2E)$ for undirected graphs ($O(V + E)$ for directed).
- **Space Complexity:** $O(V)$ queue and visited array.
