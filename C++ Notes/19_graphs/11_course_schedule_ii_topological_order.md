# Lecture 121: Course Schedule II: Topological Ordering (LeetCode 210)

> **One-Line Purpose:** Return the complete order in which courses must be taken using BFS in-degree reduction (Kahn's algorithm), or an empty array if impossible due to circular dependencies.

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

## 🎯 Learning Objectives
- Extend cycle detection logic to output a valid sequential traversal path.
- Formulate a Topological Sort that can gracefully handle multiple valid orderings.
- Understand how BFS structure implicitly respects prerequisites.
- Apply early exit / empty state logic for un-resolvable dependencies.

---

## 🧠 Core Intuition — Why This Works

Course Schedule I answers the question: "Can I graduate?"
Course Schedule II answers the question: "What is the exact semester-by-semester plan?"

**Intuition:** 
Think of taking tasks off a "ready" pile.
If a course has an `inDegree` of 0, it means "All prerequisites have been met (or there were none)." It goes onto the ready pile (queue).
When you pull a task from the ready pile, you execute it (add it to your `order` array). By finishing this task, you might have fulfilled the prerequisite for other tasks. So you cross off this task from their list of dependencies (reduce their `inDegree`). If their dependency count drops to 0, they are now ready, so onto the pile they go!

If you finish emptying the pile but your schedule doesn't have all `N` courses, you were stopped by a cycle (deadlock).

**ASCII Visualization:**
```text
(0) -----> (1)
  \         |
   \        v
    \----> (2) -----> (3)
```
1. `inDegree`: `0=0`, `1=1`, `2=2`, `3=1`. 
2. `Ready Queue`: `[0]`.
3. Process `0`: `order=[0]`. `1`'s degree drops to 0. `2`'s drops to 1. `Queue=[1]`.
4. Process `1`: `order=[0, 1]`. `2`'s degree drops to 0. `Queue=[2]`.
5. Process `2`: `order=[0, 1, 2]`. `3`'s degree drops to 0. `Queue=[3]`.
6. Process `3`: `order=[0, 1, 2, 3]`. Done!

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Return the order..."** or **"Find a sequence..."** for dependencies.
- **"Lexicographically smallest topological sort"**: If multiple valid orders exist, and the problem asks for the smallest, swap the `queue` in Kahn's algorithm for a `priority_queue` (min-heap).
- **"Compilation sequence"**: Build tools (like `make` or `bazel`) determining what files to compile first.

---

## 📐 Algorithm Walk-Through

1. **Adjacency List & In-Degree**: Build the graph `adj` and fill the `inDegree` array from `prerequisites`. (Remember: `[course, pre]` means edge `pre -> course`).
2. **Initialize Queue**: Enqueue all nodes where `inDegree[i] == 0`.
3. **Initialize Result Vector**: Create `vector<int> order`.
4. **BFS Traversal**:
   - Loop while queue is not empty:
     - Pop node `u`.
     - Push `u` into `order`.
     - Iterate neighbors `v` of `u`:
       - `inDegree[v]--`.
       - If `inDegree[v] == 0`, enqueue `v`.
5. **Validation Check**:
   - Once queue is empty, check if `order.size() == numCourses`.
   - If yes, return `order`.
   - If no, return `{}` (empty array) because a cycle blocked processing.

---

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <queue>
#include <iostream>

using namespace std;

class SolutionCourseScheduleII {
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> adj(numCourses);
        vector<int> inDegree(numCourses, 0);

        for (const auto& edge : prerequisites) {
            adj[edge[1]].push_back(edge[0]);
            inDegree[edge[0]]++;
        }

        queue<int> q;
        for (int i = 0; i < numCourses; ++i) {
            if (inDegree[i] == 0) q.push(i);
        }

        vector<int> order;
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            order.push_back(u);

            for (int v : adj[u]) {
                inDegree[v]--;
                if (inDegree[v] == 0) {
                    q.push(v);
                }
            }
        }

        if (order.size() == (size_t)numCourses) {
            return order;
        }
        return {}; // Cycle detected, ordering impossible
    }
};

int main() {
    SolutionCourseScheduleII solver;
    vector<vector<int>> pre = {{1, 0}, {2, 0}, {3, 1}, {3, 2}};
    vector<int> res = solver.findOrder(4, pre);
    cout << "Valid Course Order: ";
    for (int c : res) cout << c << " ";
    cout << endl;
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Example:** `numCourses = 4`, `prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]`

1. **Build Step**:
   - `0 -> 1` (`inDegree[1] = 1`)
   - `0 -> 2` (`inDegree[2] = 1`)
   - `1 -> 3` (`inDegree[3] = 1`)
   - `2 -> 3` (`inDegree[3] = 2`)
   - `inDegree`: `[0, 1, 1, 2]`

2. **Initialize Queue**:
   - `inDegree[0] == 0`. `q = [0]`.

3. **Processing**:
   - Pop `0`. `order = [0]`.
     - Neighbors of `0`: `[1, 2]`.
     - Decrement `inDegree[1]` -> 0. Push `1`. `q = [1]`.
     - Decrement `inDegree[2]` -> 0. Push `2`. `q = [1, 2]`.
   - Pop `1`. `order = [0, 1]`.
     - Neighbors of `1`: `[3]`.
     - Decrement `inDegree[3]` -> 1. (Do not push). `q = [2]`.
   - Pop `2`. `order = [0, 1, 2]`.
     - Neighbors of `2`: `[3]`.
     - Decrement `inDegree[3]` -> 0. Push `3`. `q = [3]`.
   - Pop `3`. `order = [0, 1, 2, 3]`.
     - Neighbors of `3`: None. `q = []`.

4. **Validation**:
   - `order.size() (4) == numCourses (4)`. Valid! Returns `[0, 1, 2, 3]`.
   *(Note: `[0, 2, 1, 3]` is also perfectly valid).*

---

## ⚠️ Common Interview Mistakes

1. **Not Handling the Output Edge Case (Cycles)**: Returning an incomplete vector when a cycle exists instead of explicitly returning an empty vector `{}` as the problem requires. 
2. **Reverse Dependencies**: In `prerequisites`, `[A, B]` means `B -> A`. Setting up `A -> B` flips the topological order backward.
3. **Memory Leaks / Copy Overhead**: Passing `adj` by value instead of using it globally or creating it locally within the function correctly. The vector of vectors can be large.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(V + E)$ where $V = \text{numCourses}, E = \text{prerequisites.size()}$. We visit each vertex and edge at most once.
- **Space Complexity:** $O(V + E)$ to store the graph in adjacency list format, plus $O(V)$ for queue and in-degree arrays.

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Can I use DFS to solve this? Which is preferred?
**Answer:** Yes, using post-order DFS (pushing to a stack when returning, then reversing the stack). Kahn's BFS is often preferred because it builds the result array linearly from left-to-right (no reversal needed), handles disconnected subgraphs automatically at the `queue` initialization, and prevents recursion stack-overflow on $10^5$ depth graphs.

### Q2: What if we want to find ALL valid topological orders?
**Answer:** Kahn's algorithm can be modified using Backtracking. If at any step the queue has `K` elements, any of those `K` can be picked next. You would use a recursive function that loops through all current 0-in-degree elements, picks one, updates in-degrees, recurses, and then backtracks (un-picks it, restores in-degrees). This takes $O(V!)$ time worst-case.

### Q3: What if the problem states: "If there are multiple valid orders, return the one that is lexicographically smallest"?
**Answer:** Simply replace the standard `queue<int>` with a `priority_queue<int, vector<int>, greater<int>>` (Min-Heap). This guarantees that whenever multiple courses are ready to be taken, you always pick the one with the smallest ID first. The complexity becomes $O(V + E \log V)$.

### Q4: In an interview, what edge cases should I explicitly test before saying I'm done?
**Answer:** 
- A graph that is totally disconnected (0 edges).
- A graph that is one giant cycle (e.g., $0 \to 1 \to 2 \to 0$).
- A graph with multiple unconnected DAGs.
- `numCourses = 1`.

### Q5: How is Topological Sort used in React or Excel?
**Answer:** In React (hooks dependencies or state updates) and Excel (cell formula calculations), changes trigger cascades. A topological sort ensures that if Cell A depends on B, and B depends on C, C recalculates first, then B, then A. If a cycle exists, Excel throws a "Circular Reference Warning."

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 207: Course Schedule I](https://leetcode.com/problems/course-schedule/)** — (Base version, boolean return).
2. **[Leetcode 269: Alien Dictionary (Premium)](https://leetcode.com/problems/alien-dictionary/)** — (Graph building from strings + Topological Sort).
3. **[Leetcode 310: Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/)** — (Uses a similar degree-reduction BFS, peeling leaves iteratively).

---

## 🔗 Cross-Topic Connections
- **Priority Queues (Heaps):** Used alongside Topo Sort when specific ordering tie-breakers (like smallest ID) are needed.
- **Backtracking:** Used to generate *all* permutations of valid topological sorts.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Return the actual valid ordering of dependent tasks.
- **Kahn's Topo Sort:** `inDegree` array + BFS Queue.
- **Key Step:** Only push node to queue when `inDegree[node] == 0`.
- **Validation:** Compare size of result array to `V`. If less, cycle exists -> return empty `{}`.
- **Tie-Breaker Variation:** If lexicographical order needed, swap `queue` for `min-heap`.
- **Time/Space:** Both are $O(V + E)$.
