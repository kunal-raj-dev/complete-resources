# Lecture 112: Breadth-First Search (BFS) Traversal

> **One-Line Purpose:** Implement level-by-level graph exploration using a FIFO queue to compute shortest paths on unweighted graphs in $O(V + E)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #112  
> **Video ID:** `scQITTLgFJo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=scQITTLgFJo)  
> **Duration:** 18:31  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- The FIFO Queue invariant driving concentric wave-front expansion.
- The critical role of the `visited` array to prevent infinite cycles.
- Handling disconnected graph components via multi-component driver loops.
- Proof of BFS finding shortest paths in unweighted graphs.

---

## 🔵 Algorithmic Intuition & Core Principles

BFS explores all neighbors at distance $d$ before moving to distance $d+1$:
```
Queue State Progression:
Initial:   [0]            (Level 0)
Pop 0:     [1, 2]         (Level 1)
Pop 1:     [2, 3]         (Level 2)
Pop 2:     [3, 4]
Pop 3:     [4]
Pop 4:     []             (All reachable visited)
```

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <queue>

using namespace std;

class BFSGraph {
private:
    int V;
    vector<vector<int>> adj;

public:
    BFSGraph(int vertices) : V(vertices), adj(vertices) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u); // Undirected
    }

    // Single Component BFS from starting source
    void bfsComponent(int src, vector<bool>& visited, vector<int>& traversal) {
        queue<int> q;
        visited[src] = true;
        q.push(src);

        while (!q.empty()) {
            int u = q.front();
            q.pop();
            traversal.push_back(u);

            for (int neighbor : adj[u]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true; // Mark BEFORE pushing to prevent duplicate queue entries
                    q.push(neighbor);
                }
            }
        }
    }

    // Full graph BFS handling disconnected components
    vector<int> bfsTraversal() {
        vector<bool> visited(V, false);
        vector<int> traversal;

        for (int i = 0; i < V; ++i) {
            if (!visited[i]) {
                bfsComponent(i, visited, traversal);
            }
        }
        return traversal;
    }
};

int main() {
    BFSGraph g(5);
    g.addEdge(0, 1);
    g.addEdge(0, 2);
    g.addEdge(1, 3);
    g.addEdge(2, 4);

    vector<int> res = g.bfsTraversal();
    cout << "BFS Order: ";
    for (int node : res) cout << node << " ";
    cout << endl;
    return 0;
}
```

---

## 🔍 Step-by-Step Dry Run
Given Graph: `0-1, 0-2, 1-3, 2-4`:
1. Start at 0: `visited[0] = true`, `q = [0]`
2. Pop 0: Output `[0]`. Neighbors `1, 2`. Mark `visited[1]=visited[2]=true`. `q = [1, 2]`
3. Pop 1: Output `[0, 1]`. Neighbor `3`. Mark `visited[3]=true`. `q = [2, 3]`
4. Pop 2: Output `[0, 1, 2]`. Neighbor `4`. Mark `visited[4]=true`. `q = [3, 4]`
5. Pop 3: Output `[0, 1, 2, 3]`. Neighbors already visited. `q = [4]`
6. Pop 4: Output `[0, 1, 2, 3, 4]`. Queue empty. Done.

---

## ⚠️ Common Pitfalls & Corner Cases
1. **Marking Visited on Pop instead of Push:** If you mark `visited[u] = true` after popping from the queue, a node can be pushed multiple times by adjacent neighbors, exploding the queue size to $O(E)$ and degrading performance.
2. **Disconnected Graphs:** Never assume vertex 0 connects to the entire graph. Always loop through $0 \dots V-1$.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(V + E)$ where every vertex is enqueued/dequeued once, and every edge is traversed twice (undirected).
- **Space Complexity:** $O(V)$ auxiliary space for `visited` array and queue buffer.

---

## 🧠 Core Intuition — Why This Works

### Real-World Analogy: Ripples in a Pond
Drop a stone in still water. The ripple expands outward in perfect concentric circles — every point at distance $d$ is wetted before any point at distance $d+1$. BFS is *exactly* this: the queue is the ripple front, advancing one level (one edge-hop) at a time.

```
        Graph:                BFS Wave Expansion:
        
        0                     t=0:  [0]        ← source
       / \                    t=1:  [1][2]     ← 1-hop neighbors
      1   2                   t=2:  [3][4]     ← 2-hop neighbors
      |   |
      3   4
      
  Queue snapshot:
  After push 0:   [0]
  After pop 0:    [1, 2]   visited={0,1,2}
  After pop 1:    [2, 3]   visited={0,1,2,3}
  After pop 2:    [3, 4]   visited={0,1,2,3,4}
  After pop 3:    [4]
  After pop 4:    [] DONE
```

### The Key Insight: Why BFS Guarantees Shortest Paths
**Claim:** When BFS first visits vertex $v$, it has found the shortest path (minimum number of edges) from source $s$ to $v$.

**Proof sketch (by induction on distance $d$):**
- **Base case:** $d = 0$: Source $s$ is at distance 0. Trivially shortest.
- **Inductive step:** Assume all nodes at distance $d$ are discovered with correct shortest path. When we process a level-$d$ node $u$, we push all of $u$'s unvisited neighbors. Those neighbors have distance exactly $d+1$ (since they haven't been seen yet — if they were reachable in fewer hops they'd already be visited). ∎

DFS **cannot** guarantee this because it may go deep down a long path before exploring a shorter one.

---

## 🎯 Pattern Recognition — When to Use BFS

| Problem Cue | Why BFS Fits |
|---|---|
| "Minimum steps / moves / jumps" | BFS level = number of steps from source |
| "Shortest path in unweighted graph" | First visit = shortest distance guaranteed |
| "Level-order traversal" | Natural layer-by-layer expansion |
| "Multi-source spreading" (e.g., fire/rot spreads) | Enqueue all sources at $t=0$ |
| "Minimum transformations" (Word Ladder) | Each word is a node; BFS finds min transforms |
| "Nearest X from every cell" | Multi-source BFS from all X positions |

### Distinguishing BFS vs DFS
| Property | BFS | DFS |
|---|---|---|
| Data structure | Queue (FIFO) | Stack / Recursion (LIFO) |
| Path property | Shortest (unweighted) | Not necessarily shortest |
| Space | $O(W)$ where $W$ = max width | $O(D)$ where $D$ = max depth |
| Best for | Shortest path, level problems | Connectivity, cycle detection, topo sort |
| Traversal shape | Wide/shallow | Narrow/deep |

---

## ⚠️ Common Interview Mistakes

### 1. Marking Visited AFTER Pop (Critical Bug)
```cpp
// ❌ WRONG — causes duplicate queue entries
void bfsBuggy(int src) {
    queue<int> q;
    q.push(src);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        visited[u] = true;  // TOO LATE!
        for (int v : adj[u])
            if (!visited[v]) q.push(v); // v may be pushed multiple times!
    }
}
```
**Impact:** In a dense graph with $E = O(V^2)$, the queue can hold $O(E)$ entries instead of $O(V)$, causing TLE or MLE.

### 2. Forgetting Disconnected Components
```cpp
// ❌ WRONG — only visits one component
bfsComponent(0, visited, result);

// ✅ CORRECT — visits all components
for (int i = 0; i < V; ++i)
    if (!visited[i]) bfsComponent(i, visited, result);
```

### 3. Off-by-One in Level/Time Counting
When counting the number of BFS levels (e.g., minimum steps), increment `time/level` **after** processing each full layer, not for each individual node pop. Use a `layerSize` snapshot.

### 4. Not Handling the Empty Graph
Always guard: `if (graph.empty()) return;`

### 5. Using BFS on Weighted Graphs for Shortest Path
BFS finds shortest path by **edge count**, not by **edge weight**. For weighted graphs, use Dijkstra's algorithm instead.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Why does BFS guarantee shortest path in unweighted graphs but DFS does not?

**Answer:** BFS explores nodes in non-decreasing order of their distance from the source. By the time BFS first reaches a node $v$ at depth $d$, it has already fully processed all nodes at depths $0, 1, \ldots, d-1$. Therefore, no shorter path to $v$ exists — any path of length $< d$ would have been discovered earlier.

DFS, by contrast, follows one branch as deep as possible before backtracking. It might reach a node $v$ via a path of length 10 before ever trying the path of length 2. There is no mechanism in plain DFS to guarantee minimum-hop discovery.

Formally: BFS maintains the invariant that `dist[v]` is non-decreasing as nodes are popped from the queue. DFS makes no such guarantee.

### Q2: [Bug Prediction] What is the output of this code? Is it correct?
```cpp
void bfs(int src) {
    queue<int> q;
    q.push(src);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        visited[u] = true;
        cout << u << " ";
        for (int v : adj[u])
            if (!visited[v]) q.push(v);
    }
}
// Graph: 0-1, 0-2, 1-2 (triangle)
// Call: bfs(0)
```
**Answer:** The traversal output will be `0 1 2 2` (node 2 appears twice!). Since visited is marked on pop, both node 1 and node 0 push node 2 onto the queue before node 2 is marked visited. This is a classic interview trap. The fix: mark `visited[v] = true` **before** `q.push(v)`.

### Q3: [Conceptual] What is Multi-Source BFS and when do you use it?

**Answer:** Multi-Source BFS initializes the queue with **multiple source nodes simultaneously** at time $t=0$, allowing simultaneous wave-front expansion from all sources. This is used when you need the minimum distance from **any** source to each node, rather than from one fixed source.

**Classic problems:**
- **Rotting Oranges (LC 994):** All initially rotten oranges are enqueued at $t=0$; BFS propagates infection simultaneously.
- **01 Matrix (LC 542):** All zeros are enqueued; BFS computes distance from nearest zero for each cell.
- **Walls and Gates:** All gates are enqueued; BFS fills rooms with distance to nearest gate.

The key insight: Multi-source BFS is equivalent to adding a virtual super-source $S$ connected to all real sources with 0-weight edges, then running single-source BFS from $S$.

### Q4: [Complexity] BFS on a graph represented as an adjacency matrix vs adjacency list — what changes?

**Answer:**
- **Adjacency List:** $O(V + E)$ time. For each node, we only iterate over its actual neighbors.
- **Adjacency Matrix:** $O(V^2)$ time. For each node popped, we scan all $V$ columns to find neighbors, even if the node has degree 1.

For sparse graphs ($E \ll V^2$), the adjacency list is far superior. For dense graphs ($E \approx V^2$), both are asymptotically equivalent. Space is $O(V + E)$ for list vs $O(V^2)$ for matrix.

### Q5: [Extension] How would you modify BFS to find the actual shortest path (not just the distance)?

**Answer:** Maintain a `parent[]` array where `parent[v] = u` means $u$ was the node that discovered $v$ in BFS. After BFS completes, backtrack from the target to the source:

```cpp
vector<int> shortestPath(int src, int dst) {
    vector<int> parent(V, -1);
    vector<bool> visited(V, false);
    queue<int> q;
    visited[src] = true;
    q.push(src);
    
    while (!q.empty()) {
        int u = q.front(); q.pop();
        if (u == dst) break;
        for (int v : adj[u]) {
            if (!visited[v]) {
                visited[v] = true;
                parent[v] = u;
                q.push(v);
            }
        }
    }
    
    // Reconstruct path
    vector<int> path;
    for (int v = dst; v != -1; v = parent[v])
        path.push_back(v);
    reverse(path.begin(), path.end());
    return path;
}
```

### Q6: [Memory] Compare memory usage of BFS vs DFS for a balanced binary tree with $N$ nodes.

**Answer:**
- **BFS** queue holds at most one full level. The widest level of a balanced binary tree is the leaf level: $\lceil N/2 \rceil$ nodes. So BFS space = $O(N)$.
- **DFS** call stack holds the current root-to-leaf path. Depth of a balanced tree = $O(\log N)$. So DFS space = $O(\log N)$.

**Winner for memory:** DFS on balanced trees. However, for a skewed (linear) tree:
- BFS queue: $O(1)$ (only one node per level)
- DFS stack: $O(N)$ (depth = N)

So the right choice depends on the graph's structure.

### Q7: [System Design] How would you use BFS in a social network to implement "people you may know" (friends-of-friends)?

**Answer:** Model the social graph where nodes = users, edges = friendships. Run BFS from the user $u$ up to depth 2:
- **Level 1:** Direct friends of $u$ (already known)
- **Level 2:** Friends of friends — these are the "people you may know" candidates

Filter out users already at Level 1 (direct friends). Rank candidates by number of mutual friends (= how many Level-1 nodes they're connected to). This is exactly a 2-hop BFS with frequency counting. LinkedIn and Facebook use variants of this approach with graph sampling and approximate algorithms for scale.

### Q8: [Directed Graphs] Does BFS work on directed graphs? What property does it preserve?

**Answer:** Yes, BFS works on directed graphs. It still computes the shortest directed path (minimum number of hops following edge directions) from source $s$ to any reachable vertex. The visited array prevents revisiting. However, BFS on a directed graph only explores vertices **reachable** from the source — nodes that only have incoming edges from non-reachable nodes will never be visited. This is correct behavior: those nodes are simply not reachable from the source.

---

## 🏆 Related LeetCode Problems

| # | Problem | Approach Hint |
|---|---|---|
| 200 | Number of Islands | Multi-component BFS/DFS on grid |
| 994 | Rotting Oranges | Multi-source BFS; count levels |
| 542 | 01 Matrix | Multi-source BFS from all 0s simultaneously |
| 127 | Word Ladder | BFS on implicit graph (each word is a node) |
| 1926 | Nearest Exit from Entrance in Maze | Single-source BFS on grid |

---

## 🔗 Cross-Topic Connections

- **Dijkstra's Algorithm:** BFS on weighted graphs — replace the queue with a priority queue (min-heap). BFS is a special case of Dijkstra where all edge weights = 1.
- **Topological Sort (Kahn's):** Uses BFS but with in-degree filtering; only enqueues nodes with in-degree 0.
- **Bipartite Check:** BFS with 2-coloring — if any neighbor has the same color, the graph is not bipartite.
- **0-1 BFS:** Uses a deque instead of a queue — push to front for 0-weight edges, push to back for 1-weight edges. More efficient than Dijkstra for 0-1 weight graphs.
- **Multi-Source BFS → Distance Transform:** The basis for computing distance maps in computer vision and robotics path planning.

---

## ⚡ 2-Minute Revision Flash Card

- **BFS uses a FIFO queue** — always mark visited **before enqueue**, never after pop.
- **Guarantees shortest path** (by edge count) on unweighted graphs via level-by-level expansion.
- **Always loop over all vertices** as sources to handle disconnected graphs.
- **Multi-source BFS:** Enqueue all sources at $t=0$; perfect for "spread from multiple origins" problems.
- **Time & Space:** $O(V + E)$ time; $O(V)$ queue space — but queue width can be $O(V)$ in worst case (star graph).
