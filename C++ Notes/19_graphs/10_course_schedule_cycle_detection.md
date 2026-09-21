# Lecture 120: Course Schedule I (LeetCode 207)

> **One-Line Purpose:** Determine if all courses can be finished by detecting cycles in the prerequisite dependency DAG using Kahn's algorithm or DFS.

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

## 🎯 Learning Objectives
- Map real-world dependency problems ("do A before B") to directed graphs.
- Understand how directed cycles prevent task completion (deadlock).
- Master cycle detection using In-Degrees (Kahn's Algorithm BFS).
- Learn to confidently track processing count to verify completion.

---

## 🧠 Core Intuition — Why This Works

If Course A requires Course B, and Course B requires Course C, we process C, then B, then A. 
But what if Course A requires Course B, AND Course B requires Course A? 
This is a cycle. You can start neither.

**Kahn's Algorithm Intuition:**
We track the "In-Degree" of every node (how many prerequisites it has). 
1. If a course has `In-Degree = 0`, it has no prerequisites. We can take it immediately.
2. After taking it, we effectively remove it from the graph. For all the courses that depended on it, we reduce their `In-Degree` by 1.
3. If their `In-Degree` becomes 0, we can now take them too!
4. If we finish this process and still have courses left that never reached `In-Degree = 0`, they must be stuck in a cycle.

**ASCII Visualization:**
```text
(0) ---> (1) ---> (2)      Cycle:
           ^       |       (3) ---> (4)
           |       v        ^        |
           +-------+        +--------+
```
For `(3) -> (4) -> (3)`, both start with In-Degree 1. Since neither is 0, they are never added to our processing queue. Thus, `completed_count` falls short of the total courses.

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Course schedule", "Prerequisites"**: Direct application of Topological Sort / Kahn's.
- **"Task Scheduling"**: Jobs that must be executed in a specific order.
- **"Is it possible to finish..."**: Keyword for checking if a valid topological sort exists (i.e., checking if the graph is a DAG).
- **"Deadlock detection"**: In operating systems, detecting circular wait.

---

## 📐 Algorithm Walk-Through

1. **Build Adjacency List & In-Degree Array**: 
   - Iterate through `prerequisites`. For `[course, pre]`, add an edge `pre -> course`.
   - Increment `inDegree[course]`.
2. **Initialize Queue**: 
   - Push all courses with `inDegree == 0` into a queue.
3. **BFS Traversal**:
   - Maintain a `completed = 0` counter.
   - While queue is not empty:
     - Pop a node `u`. Increment `completed`.
     - For every neighbor `v` of `u`:
       - Decrement `inDegree[v]`.
       - If `inDegree[v] == 0`, push `v` into the queue.
4. **Final Check**: 
   - If `completed == numCourses`, return `true` (no cycle).
   - If `completed < numCourses`, return `false` (cycle detected).

---

## 💻 Complete C++ Implementation (Kahn's BFS Method)

```cpp
#include <vector>
#include <queue>
#include <iostream>

using namespace std;

class SolutionCourseSchedule {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> adj(numCourses);
        vector<int> inDegree(numCourses, 0);

        // prerequisites: [course, prerequisite] => edge: pre -> course
        for (const auto& pair : prerequisites) {
            int course = pair[0];
            int pre = pair[1];
            adj[pre].push_back(course);
            inDegree[course]++;
        }

        queue<int> q;
        for (int i = 0; i < numCourses; ++i) {
            if (inDegree[i] == 0) q.push(i);
        }

        int completed = 0;
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            completed++;

            for (int neighbor : adj[u]) {
                inDegree[neighbor]--;
                if (inDegree[neighbor] == 0) {
                    q.push(neighbor);
                }
            }
        }

        return completed == numCourses;
    }
};

int main() {
    SolutionCourseSchedule solver;
    vector<vector<int>> pre = {{1, 0}, {0, 1}}; // Cycle 0 <-> 1
    cout << "Can finish: " << (solver.canFinish(2, pre) ? "YES" : "NO") << endl; // NO
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Example:** `numCourses = 4`, `prerequisites = [[1,0], [2,1], [3,2], [1,3]]`
Graph: `0 -> 1 -> 2 -> 3 -> 1` (Cycle between 1, 2, 3)

1. **Build Step**:
   - `0 -> 1` (`inDegree[1] = 1`)
   - `1 -> 2` (`inDegree[2] = 1`)
   - `2 -> 3` (`inDegree[3] = 1`)
   - `3 -> 1` (`inDegree[1] = 2`)
   - `inDegree` array: `[0, 2, 1, 1]`

2. **Initialize Queue**:
   - Only `0` has `inDegree == 0`.
   - `q = [0]`

3. **BFS Execution**:
   - Pop `0`. `completed = 1`.
   - Neighbors of `0`: `[1]`.
   - Decrement `inDegree[1]` -> becomes `1`. (Not 0, so don't push).
   - `q` is now empty.

4. **Final Check**:
   - Loop ends. `completed = 1`.
   - `1 != 4` (numCourses). Return `false`.
   - Logic holds! The cycle `1-2-3` blocked completion.

---

## ⚠️ Common Interview Mistakes

1. **Reversing the Directed Edge**: A prerequisite `[a, b]` (take `b` to take `a`) means the edge MUST be `b -> a`. Making it `a -> b` fundamentally breaks the in-degree logic.
2. **Handling Disconnected Graphs**: You don't need a `for` loop to restart BFS from unvisited nodes because Kahn's inherently handles disconnected components. It pushes ALL initial `0`-in-degree nodes into the queue at the start.
3. **Space Complexity Blowout**: Using a heavy structure like `unordered_map<int, vector<int>>` for `adj` instead of a simple `vector<vector<int>>`. Courses are labeled `0` to `n-1`, so a vector of vectors is faster and cheaper.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(V + E)$ where $V = \text{numCourses}, E = \text{prerequisites.size()}$. Building the graph takes $O(E)$. BFS visits each node once and traverses each edge once.
- **Space Complexity:** $O(V + E)$ for the adjacency list. $O(V)$ for the `inDegree` array and $O(V)$ for the queue. Total space: $O(V + E)$.

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Can this be solved using DFS? 
**Answer:** Yes. You would maintain a `visited` array (size `V`) using three states: `0 = unvisited`, `1 = visiting (in current recursion stack)`, `2 = visited completely`. If during DFS you encounter a node in state `1`, you have found a cycle. 

### Q2: Why is Kahn's algorithm (BFS) often preferred over DFS for this problem?
**Answer:** Kahn's is non-recursive, preventing stack overflow on massive graphs. Furthermore, if you need to return the topological order itself, Kahn's builds it naturally from front to back, whereas DFS requires pushing to a stack and reversing.

### Q3: What if there are multiple courses with no prerequisites?
**Answer:** Kahn's algorithm pushes all of them to the queue initially. The order in which they are processed doesn't matter for cycle detection. They are valid independent starting points.

### Q4: How would you parallelize this if courses take different times to complete?
**Answer:** This transforms the problem into finding the longest path (critical path) in a DAG. You would maintain an array `time_to_complete[u]`. When relaxing edges: `earliest_start[v] = max(earliest_start[v], earliest_start[u] + duration[u])`. You still process in topological order using Kahn's.

### Q5: What if `numCourses` is huge (e.g., $10^9$) but dependencies are sparse?
**Answer:** You can't allocate a `vector` of size $10^9$. You would switch to `unordered_map<int, vector<int>>` for the adjacency list and `unordered_map<int, int>` for in-degrees. This optimizes space to $O(E)$.

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 210: Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)** — Similar, but return the ordering instead of a boolean.
2. **[Leetcode 802: Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/)** — Nodes that don't lead to a cycle. Can be solved by reversing graph and running Kahn's.
3. **[Leetcode 1462: Course Schedule IV](https://leetcode.com/problems/course-schedule-iv/)** — Is A a prerequisite of B (transitive closure). Topo Sort + BFS/DFS per node.

---

## 🔗 Cross-Topic Connections
- **Graphs (Cycle Detection):** This is the definitive directed graph cycle detection algorithm.
- **Dynamic Programming (Critical Path):** Job scheduling with maximum durations heavily relies on topological sorting as the baseline state-processing order.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Determine if a DAG is cycle-free.
- **Kahn's Method:** 
  1. Calculate `inDegree` for all nodes.
  2. Queue nodes with `inDegree == 0`.
  3. BFS: Pop node, decrement neighbors' `inDegree`. If 0, queue them.
  4. Increment `completed` counter per pop.
- **Condition:** Cycle exists if `completed < numCourses`.
- **Edge Direction:** If A depends on B, edge is `B -> A`.
- **Time / Space:** $O(V + E)$ Time | $O(V + E)$ Space.
