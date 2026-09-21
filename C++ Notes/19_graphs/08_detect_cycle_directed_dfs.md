# Lecture 118: Detect Cycle in Directed Graph using DFS

> **One-Line Purpose:** Identify directed cycles by tracking both global visited nodes and active recursion call stack paths.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #118  
> **Video ID:** `AcppN5XFt24`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=AcppN5XFt24)  
> **Duration:** 15:59  
> **Status:** AUDITED  

---

## 🔵 Complete Implementation

```cpp
#include <vector>
using namespace std;

bool dfsCycleDirected(int node, const vector<vector<int>>& adj, vector<bool>& visited, vector<bool>& inStack) {
    visited[node] = true;
    inStack[node] = true;

    for (int neighbor : adj[node]) {
        if (!visited[neighbor]) {
            if (dfsCycleDirected(neighbor, adj, visited, inStack)) return true;
        } else if (inStack[neighbor]) {
            // Node is currently active in recursion stack => Directed Cycle!
            return true;
        }
    }

    inStack[node] = false; // Backtrack
    return false;
}
```
