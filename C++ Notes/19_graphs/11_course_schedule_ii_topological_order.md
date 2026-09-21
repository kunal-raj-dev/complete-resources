# Lecture 121: Course Schedule II: Topological Ordering (LeetCode 210)

> **One-Line Purpose:** Generate the complete prerequisite sequence of courses using Kahn's algorithm in $O(V + E)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #121  
> **Video ID:** `rZsgWxodGmM`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=rZsgWxodGmM)  
> **Duration:** 19:33  
> **Status:** AUDITED  

---

## 🔵 Complete Implementation

```cpp
#include <vector>
#include <queue>
using namespace std;

class SolutionCourseScheduleII {
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> adj(numCourses);
        vector<int> inDegree(numCourses, 0);

        for (auto& p : prerequisites) {
            adj[p[1]].push_back(p[0]);
            inDegree[p[0]]++;
        }

        queue<int> q;
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) q.push(i);
        }

        vector<int> order;
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            order.push_back(u);

            for (int v : adj[u]) {
                if (--inDegree[v] == 0) {
                    q.push(v);
                }
            }
        }

        return (order.size() == numCourses) ? order : vector<int>();
    }
};
```
