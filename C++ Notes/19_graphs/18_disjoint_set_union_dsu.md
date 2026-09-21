# Lecture 128: Disjoint Set Union (DSU): Path Compression & Rank/Size

> **One-Line Purpose:** Implement Union-Find data structures with Path Compression and Union by Rank/Size running in nearly constant amortized $O(\alpha(N))$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna Course)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #128  
> **Video ID:** `nnrjWxWMo3E`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=nnrjWxWMo3E)  
> **Duration:** 34:04  
> **Status:** AUDITED  

---

## 🔵 Production C++ DSU Class

```cpp
#include <vector>
#include <numeric>
using namespace std;

class DisjointSet {
private:
    vector<int> parent;
    vector<int> rank;
    vector<int> size;

public:
    DisjointSet(int n) {
        parent.resize(n);
        iota(parent.begin(), parent.end(), 0);
        rank.assign(n, 0);
        size.assign(n, 1);
    }

    // Find with Path Compression: O(alpha(N))
    int findUPar(int node) {
        if (node == parent[node]) return node;
        return parent[node] = findUPar(parent[node]);
    }

    // Union by Size
    bool unionBySize(int u, int v) {
        int ulp_u = findUPar(u);
        int ulp_v = findUPar(v);
        if (ulp_u == ulp_v) return false; // Already in same set (cycle!)

        if (size[ulp_u] < size[ulp_v]) {
            parent[ulp_u] = ulp_v;
            size[ulp_v] += size[ulp_u];
        } else {
            parent[ulp_v] = ulp_u;
            size[ulp_u] += size[ulp_v];
        }
        return true;
    }
};
```
