# Lecture 135: Strongly Connected Components: Kosaraju's Algorithm

> **One-Line Purpose:** Extract all Strongly Connected Components (SCC) in directed graphs in $O(V + E)$ time using edge transposition and finish-time orderings.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #135  
> **Video ID:** `lqY8TE0P1S8`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=lqY8TE0P1S8)  
> **Duration:** 26:26  
> **Status:** AUDITED  

---

## 🔵 Kosaraju's 3 Steps & Implementation
1. **Pass 1:** Order nodes by finish time using DFS and a stack.
2. **Step 2:** Transpose the graph (reverse all directed edges $u \to v$ to $v \to u$).
3. **Pass 3:** Pop stack and run DFS on transposed graph to identify each SCC component.

```cpp
#include <vector>
#include <stack>
using namespace std;

void dfs1(int u, const vector<vector<int>>& adj, vector<bool>& vis, stack<int>& st) {
    vis[u] = true;
    for (int v : adj[u]) if (!vis[v]) dfs1(v, adj, vis, st);
    st.push(u);
}

void dfs2(int u, const vector<vector<int>>& adjT, vector<bool>& vis) {
    vis[u] = true;
    for (int v : adjT[u]) if (!vis[v]) dfs2(v, adjT, vis);
}

int kosarajuSCC(int V, const vector<vector<int>>& adj) {
    stack<int> st;
    vector<bool> vis(V, false);

    for (int i = 0; i < V; i++) if (!vis[i]) dfs1(i, adj, vis, st);

    // Transpose graph
    vector<vector<int>> adjT(V);
    for (int u = 0; u < V; u++) {
        for (int v : adj[u]) adjT[v].push_back(u);
    }

    fill(vis.begin(), vis.end(), false);
    int sccCount = 0;

    while (!st.empty()) {
        int u = st.top();
        st.pop();
        if (!vis[u]) {
            sccCount++;
            dfs2(u, adjT, vis);
        }
    }
    return sccCount;
}
```
