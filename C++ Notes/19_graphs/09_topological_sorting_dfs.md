# Lecture 119: Topological Sorting using DFS

> **One-Line Purpose:** Determine a valid linear sequence of vertices in a Directed Acyclic Graph (DAG) such that edge $u \to v \implies u$ precedes $v$.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #119  
> **Video ID:** `0WIINUY12Yg`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=0WIINUY12Yg)  
> **Duration:** 15:58  
> **Status:** AUDITED  

---

## 🔵 Complete Implementation

```cpp
#include <vector>
#include <stack>
using namespace std;

void topoDFS(int node, const vector<vector<int>>& adj, vector<bool>& visited, stack<int>& st) {
    visited[node] = true;
    for (int neighbor : adj[node]) {
        if (!visited[neighbor]) {
            topoDFS(neighbor, adj, visited, st);
        }
    }
    // Push to stack after visiting all dependencies
    st.push(node);
}

vector<int> topoSort(int V, const vector<vector<int>>& adj) {
    vector<bool> visited(V, false);
    stack<int> st;

    for (int i = 0; i < V; i++) {
        if (!visited[i]) topoDFS(i, adj, visited, st);
    }

    vector<int> order;
    while (!st.empty()) {
        order.push_back(st.top());
        st.pop();
    }
    return order;
}
```
