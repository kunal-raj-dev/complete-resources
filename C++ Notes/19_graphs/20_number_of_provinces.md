# Lecture 130: Number of Provinces (LeetCode 547)

> **One-Line Purpose:** Determine connected components in an adjacency matrix using DFS or Disjoint Set Union.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #130  
> **Video ID:** `J1yCPIP-K8s`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=J1yCPIP-K8s)  
> **Duration:** 12:35  
> **Status:** AUDITED  

---

## 🔵 Implementation

```cpp
#include <vector>
using namespace std;

class SolutionProvinces {
private:
    void dfs(int node, const vector<vector<int>>& isConnected, vector<bool>& vis) {
        vis[node] = true;
        for (int j = 0; j < isConnected.size(); j++) {
            if (isConnected[node][j] && !vis[j]) {
                dfs(j, isConnected, vis);
            }
        }
    }

public:
    int findCircleNum(vector<vector<int>>& isConnected) {
        int n = isConnected.size();
        vector<bool> vis(n, false);
        int provinces = 0;

        for (int i = 0; i < n; i++) {
            if (!vis[i]) {
                provinces++;
                dfs(i, isConnected, vis);
            }
        }
        return provinces;
    }
};
```
