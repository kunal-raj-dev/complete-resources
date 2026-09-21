# Lecture 120: Course Schedule: Directed Cycle Verification (LeetCode 207)

> **One-Line Purpose:** Determine prerequisite course feasibility by testing for directed cycles using Kahn's algorithm or DFS in-stack tracking.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #120  
> **Video ID:** `37cJ38HadM4`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=37cJ38HadM4)  
> **Duration:** 17:54  
> **Status:** AUDITED  

---

## 🔵 Complete Kahn's BFS Implementation

```cpp
#include <vector>
#include <queue>
using namespace std;

class SolutionCourseSchedule {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> adj(numCourses);
        vector<int> inDegree(numCourses, 0);

        for (auto& pre : prerequisites) {
            adj[pre[1]].push_back(pre[0]);
            inDegree[pre[0]]++;
        }

        queue<int> q;
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) q.push(i);
        }

        int completed = 0;
        while (!q.empty()) {
            int curr = q.front();
            q.pop();
            completed++;

            for (int neighbor : adj[curr]) {
                inDegree[neighbor]--;
                if (inDegree[neighbor] == 0) q.push(neighbor);
            }
        }

        return completed == numCourses;
    }
};
```
