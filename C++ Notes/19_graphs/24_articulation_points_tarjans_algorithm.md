# Lecture 134: Articulation Point in Graph using Tarjan's Algorithm

> **One-Line Purpose:** Locate all "cut vertices" (nodes whose removal disconnects the graph) using DFS discovery and lowest reachable timestamps in $O(V + E)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #134  
> **Video ID:** `cn7pov3BEmg`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=cn7pov3BEmg)  
> **Duration:** 36:53  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Define an Articulation Point (AP) / Cut Vertex.
- Understand why APs require a slight mathematical tweak ($\ge$) from the Bridges ($>$) condition.
- Master the special edge-case for the DFS Root node.
- Realize why tracking multiple AP flags per node in a boolean array is necessary to prevent duplicates.

---

## 🧠 Core Intuition — Why This Works

An articulation point is a node that holds two different parts of a graph together. If you remove it, the graph breaks into multiple disconnected components.
To find them, we use the same `tin` (discovery time) and `low` (lowest reachable discovery time via 1 back-edge) as we did for Bridges.

**The Condition:** `low[v] >= tin[u]`
If we are at node `u`, and we send DFS down to a neighbor `v`. If `v`'s `low` value is strictly greater than `tin[u]`, it's a bridge. 
But what if `low[v] == tin[u]`? This means `v` can reach back exactly to `u`, but NO HIGHER. If `v` can't reach above `u`, then taking `u` away will completely sever `v` from everything above `u`! Thus, `u` is an Articulation Point.

**The Root Node Exception:**
The very first node we start DFS from (the root) has no ancestors. So `low[v] >= tin[root]` will ALWAYS be true! This would falsely flag the root as an AP every time.
- **Root Condition:** The root is an AP *if and only if* it has **more than 1 independent child** in the DFS tree. If it only has 1 child, removing the root just removes an endpoint, leaving the rest of the chain intact. If it has 2 children, removing the root splits those two branches.

---

## 🎯 Pattern Recognition — When to Use This
Trigger cues: "if you see X in a problem, think Y"
- **"Cut Vertex" / "Articulation Point"**: Direct keywords.
- **"Single point of failure"**: (e.g., "Which router's failure will split the network?").
- **"Vulnerable node"**: Any node that disconnects components.

---

## 📐 Algorithm Walk-Through

1. **Setup**: `tin`, `low` initialized to -1. `isArticulation` boolean array initialized to false (a node can be flagged multiple times by different children, so a boolean array deduplicates).
2. **DFS(`u`, `parent`)**:
   - `visited[u] = true`, `tin[u] = low[u] = ++timer`.
   - `children = 0` (used ONLY for the root).
   - Loop neighbors `v`:
     - If `v == parent`, continue.
     - If `visited[v]`: (Back-edge) `low[u] = min(low[u], tin[v])`.
     - If `!visited[v]`: (Tree-edge)
       - `children++`.
       - Recurse `dfs(v, u)`.
       - `low[u] = min(low[u], low[v])`.
       - **Check Non-Root:** If `parent != -1` AND `low[v] >= tin[u]`, mark `isArticulation[u] = true`.
3. **Check Root**:
   - After the loop, if `parent == -1` AND `children > 1`, mark `isArticulation[u] = true`.

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

class TarjanArticulationPoints {
private:
    int timer;
    void dfs(int u, int parent, const vector<vector<int>>& adj, vector<int>& tin,
             vector<int>& low, vector<bool>& visited, vector<bool>& isArticulation) {
        visited[u] = true;
        tin[u] = low[u] = ++timer;
        int children = 0;

        for (int v : adj[u]) {
            if (v == parent) continue; // Skip trivial reverse edge

            if (visited[v]) {
                // Back-edge: Update low using tin[v]
                low[u] = min(low[u], tin[v]);
            } else {
                // Tree-edge: standard DFS
                children++;
                dfs(v, u, adj, tin, low, visited, isArticulation);
                
                // Update low of u based on child's low
                low[u] = min(low[u], low[v]);

                // Case 1: Non-root condition for Articulation Point
                if (parent != -1 && low[v] >= tin[u]) {
                    isArticulation[u] = true;
                }
            }
        }

        // Case 2: Root condition for Articulation Point
        // If the root of DFS tree has more than one disconnected child branch
        if (parent == -1 && children > 1) {
            isArticulation[u] = true;
        }
    }

public:
    vector<int> getArticulationPoints(int V, const vector<vector<int>>& adj) {
        vector<int> tin(V, -1), low(V, -1);
        vector<bool> visited(V, false);
        vector<bool> isArticulation(V, false);
        timer = 0;

        for (int i = 0; i < V; ++i) {
            if (!visited[i]) {
                dfs(i, -1, adj, tin, low, visited, isArticulation);
            }
        }

        vector<int> result;
        for (int i = 0; i < V; ++i) {
            if (isArticulation[i]) result.push_back(i);
        }
        return result;
    }
};

int main() {
    int V = 5;
    vector<vector<int>> adj(V);
    auto addEdge = [&](int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    };

    // Triangle 0-1-2. Line from 1 to 3 to 4.
    // 0 -- 1 -- 3 -- 4
    //  \  /
    //   2
    addEdge(0, 1);
    addEdge(1, 2);
    addEdge(2, 0);
    addEdge(1, 3);
    addEdge(3, 4);

    TarjanArticulationPoints solver;
    vector<int> ap = solver.getArticulationPoints(V, adj);
    
    cout << "Articulation Points: ";
    for (int p : ap) cout << p << " "; // Output: 1, 3
    cout << endl;
    
    return 0;
}
```

---

## 🔍 Dry Run Trace

**Graph:** `0-1`, `1-2`, `2-0`, `1-3`, `3-4`. (Same as code).
`timer = 0`. `tin` & `low` = `[-1,-1,-1,-1,-1]`.

1. **DFS(0, p=-1)**: `tin[0]=1, low[0]=1`. Kids: 1.
2. -> **DFS(1, p=0)**: `tin[1]=2, low[1]=2`. Kids: 2, 3.
3. --> **DFS(2, p=1)**: `tin[2]=3, low[2]=3`. Kids: 0.
   - Neighbor 0: visited! Back-edge! `low[2] = min(3, tin[0]=1) = 1`.
   - Return to 1.
4. Back at 1: `low[1] = min(2, low[2]=1) = 1`.
   - Check AP: `p != -1`. `low[2]=1 >= tin[1]=2`? FALSE.
5. --> **DFS(3, p=1)**: `tin[3]=4, low[3]=4`. Kids: 4.
6. ---> **DFS(4, p=3)**: `tin[4]=5, low[4]=5`. Kids: 0.
   - Return to 3.
7. Back at 3: `low[3] = min(4, low[4]=5) = 4`.
   - Check AP: `p != -1`. `low[4]=5 >= tin[3]=4`? **TRUE!** `isAP[3] = true`.
   - Return to 1.
8. Back at 1: `low[1] = min(1, low[3]=4) = 1`.
   - Check AP: `p != -1`. `low[3]=4 >= tin[1]=2`? **TRUE!** `isAP[1] = true`.
   - Return to 0.
9. Back at 0: `low[0] = min(1, low[1]=1) = 1`.
   - Check root condition: `p == -1`. `children` of 0 is `1` (because we only explored branch `1`).
   - `1 > 1`? FALSE. `isAP[0]` remains false.

**Result:** `1, 3`. (If you remove 1, 0&2 separate from 3&4. If you remove 3, 4 separates from the rest).

---

## ⚠️ Common Interview Mistakes

1. **`low[u] = min(low[u], low[v])` on Back-edges**: We mentioned this in Bridges, but it is **FATAL** here. If you use `low[v]` instead of `tin[v]` on a back-edge, you might accidentally inherit a lower time from a *parallel* path, incorrectly bypassing the `low[v] >= tin[u]` check. You MUST use `tin[v]` on back-edges.
2. **Forgetting the Root Condition**: The DFS root node will ALWAYS satisfy `low[v] >= tin[u]`. You must strictly check `parent == -1 && children > 1` instead of the standard formula.
3. **Not Using a Boolean Array**: A single node can be flagged as an AP by *multiple* different child branches. If you just push to a `vector<int> result` directly, you will get duplicate answers. Always use a `vector<bool> isArticulation` array, then collect true values at the end.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(V + E)$ single-pass DFS.
- **Space Complexity:** $O(V + E)$ for adjacency list, and $O(V)$ for arrays and call stack.

---

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Can a graph have no articulation points?
**Answer:** Yes. A simple cycle (e.g., a triangle) has no articulation points. Removing any one node just leaves a line (which is still connected). Such graphs are called **Biconnected Graphs**.

### Q2: What's the relationship between Bridges and Articulation Points?
**Answer:** They are closely related but distinct. 
- If an edge `(u, v)` is a bridge, then either `u` or `v` (usually both) will be an Articulation Point (unless they are leaf nodes of the entire graph).
- However, an Articulation Point does NOT necessarily imply a bridge. E.g., two triangles joined at a single vertex. That vertex is an AP, but there are no bridges in the graph!

### Q3: Why does `children` only increment on unvisited nodes?
**Answer:** `children` counts the number of independent DFS *subtrees*. A back-edge to an already visited node is just an edge within the *same* subtree. We only care if the root has to spawn *multiple independent DFS branches* to reach everything.

### Q4: If I have a disconnected graph, how does the Root Condition work?
**Answer:** The outer loop (`for (i=0 to V-1) if (!visited) dfs()`) will trigger multiple times. EACH time it triggers, it establishes a new DFS root (`parent = -1`). The root condition `children > 1` applies individually to every component's root.

---

## 🏆 Related Problems (Leetcode)
1. **[Leetcode 1192: Critical Connections in a Network](https://leetcode.com/problems/critical-connections-in-a-network/)** — Technically about bridges, but understanding APs is required to fully grasp the concepts.
2. **[HackerRank / SPOJ variants]**: Direct "Find Cut Vertices" questions are common on competitive platforms, though slightly less common on LeetCode as standalone problems compared to bridges.

---

## 🔗 Cross-Topic Connections
- **Bridges (Tarjan's):** The exact same setup, just $>$ instead of $\ge$.
- **Biconnected Components (BCC):** Graphs divided into maximal subgraphs that have NO articulation points. Used heavily in fault-tolerant network design.

---

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Find nodes that disconnect the graph if removed.
- **Rule 1 (Non-Root):** `parent != -1` AND `low[v] >= tin[u]`.
- **Rule 2 (Root):** `parent == -1` AND `children > 1` (independent DFS branches).
- **Back-Edge logic:** `low[u] = min(low[u], tin[v])`. (Must use `tin[v]`!).
- **Deduplication:** Use `isAP[u] = true` boolean array, NOT a direct push to results.
- **Time/Space:** $O(V + E)$ Time | $O(V + E)$ Space.
