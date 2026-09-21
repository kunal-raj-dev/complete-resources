# Lecture 129: Kruskal's Algorithm: Minimum Spanning Tree (MST)

> **One-Line Purpose:** Construct an MST by sorting all edges by weight and unioning disjoint components via DSU in $O(E \log E)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #129  
> **Video ID:** `inoM6jwj1CA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=inoM6jwj1CA)  
> **Duration:** 29:07  
> **Status:** AUDITED  

---

## 🔵 Implementation

```cpp
#include <vector>
#include <algorithm>
#include <numeric>
using namespace std;

struct Edge {
    int u, v, weight;
    bool operator<(const Edge& other) const {
        return weight < other.weight;
    }
};

int findPar(int node, vector<int>& parent) {
    if (parent[node] == node) return node;
    return parent[node] = findPar(parent[node], parent);
}

int kruskalMST(int V, vector<Edge>& edges) {
    sort(edges.begin(), edges.end()); // O(E log E)

    vector<int> parent(V);
    iota(parent.begin(), parent.end(), 0);

    int mstWeight = 0, edgesCount = 0;
    for (const auto& e : edges) {
        int p1 = findPar(e.u, parent);
        int p2 = findPar(e.v, parent);

        if (p1 != p2) {
            parent[p1] = p2;
            mstWeight += e.weight;
            if (++edgesCount == V - 1) break;
        }
    }
    return mstWeight;
}
```
