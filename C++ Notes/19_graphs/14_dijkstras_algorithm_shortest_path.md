# Lecture 124: Dijkstra's Algorithm: Single-Source Shortest Path

> **One-Line Purpose:** Compute the minimal path costs from a starting source vertex to all other vertices in non-negative weighted graphs using greedy Min-Heap relaxation in $O((V + E) \log V)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #124  
> **Video ID:** `8gYBHjtjWBI`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=8gYBHjtjWBI)  
> **Duration:** 35:20  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Single-Source Shortest Path (SSSP) problem definition.
- Edge Relaxation Condition: `dist[u] + weight < dist[v]`.
- Why Dijkstra fails on negative weight edges (greedy premise violated).
- Optimizing vertex selection from $O(V^2)$ (unvisited array scan) to $O((V + E) \log V)$ via Min-Priority Queue.

---

## 🧠 Core Intuition
At its core, Dijkstra's algorithm operates like a breadth-first search (BFS) on steroids. While BFS expands outward level-by-level (assuming uniform edge weights), Dijkstra expands "contour by contour" based on accumulated path cost. Imagine dropping a stone in a pond: the ripples expand concentrically. The Min-Priority Queue perfectly simulates this concentric expansion. By always selecting the node with the smallest tentative distance, we guarantee that no shorter path to it could possibly be discovered later—because any alternative route would have to pass through a node further away, and since all edge weights are $\ge 0$, that route would strictly increase the distance. This greedy choice property is what definitively seals a node's shortest path the moment it is extracted from the queue.

**Greedy Relaxation Invariant:**
Maintain a tentative distance array initialized to $\infty$, with `dist[src] = 0`.
At each iteration, select the unvisited vertex $u$ with the smallest tentative distance. Because all edge weights are non-negative, no future path can possibly relax $u$ with a shorter distance.

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <climits>

using namespace std;

// Pair format: <distance, vertex>
typedef pair<int, int> pii;

class DijkstraSolver {
private:
    int V;
    vector<vector<pair<int, int>>> adj; // <neighbor, weight>

public:
    DijkstraSolver(int vertices) : V(vertices), adj(vertices) {}

    void addEdge(int u, int v, int weight) {
        adj[u].push_back({v, weight});
        adj[v].push_back({u, weight}); // Undirected
    }

    vector<int> shortestPath(int src) {
        vector<int> dist(V, INT_MAX);
        priority_queue<pii, vector<pii>, greater<pii>> pq; // Min-Heap

        dist[src] = 0;
        pq.push({0, src});

        while (!pq.empty()) {
            auto [currentDist, u] = pq.top();
            pq.pop();

            // Ignore stale entries in priority queue
            if (currentDist > dist[u]) continue;

            for (const auto& edge : adj[u]) {
                int v = edge.first;
                int weight = edge.second;

                // Relaxation Step
                if (dist[u] + weight < dist[v]) {
                    dist[v] = dist[u] + weight;
                    pq.push({dist[v], v});
                }
            }
        }

        return dist;
    }
};

int main() {
    DijkstraSolver solver(5);
    solver.addEdge(0, 1, 4);
    solver.addEdge(0, 2, 8);
    solver.addEdge(1, 2, 2);
    solver.addEdge(1, 3, 5);
    solver.addEdge(2, 3, 5);
    solver.addEdge(2, 4, 9);
    solver.addEdge(3, 4, 4);

    vector<int> distances = solver.shortestPath(0);
    cout << "Shortest distances from source 0:\n";
    for (int i = 0; i < 5; ++i) {
        cout << "To " << i << " : " << distances[i] << "\n";
    }
    return 0;
}
```

---

## 📐 Dry Run Trace

### Example 1: Standard Step-by-Step
Source `0`: `dist = [0, inf, inf, inf, inf]`, `pq = [(0, 0)]`
1. Pop `(0, 0)`. Relax neighbors:
   - $0 \to 1$ (weight 4): `dist[1] = 4`, push `(4, 1)`
   - $0 \to 2$ (weight 8): `dist[2] = 8`, push `(8, 2)`
2. Pop `(4, 1)`. Relax neighbors:
   - $1 \to 2$ (weight 2): $4 + 2 = 6 < 8 \Rightarrow$ `dist[2] = 6`, push `(6, 2)`
   - $1 \to 3$ (weight 5): $4 + 5 = 9 \Rightarrow$ `dist[3] = 9`, push `(9, 3)`
3. Pop `(6, 2)`. Relax neighbors:
   - $2 \to 3$ (weight 5): $6 + 5 = 11 \ge 9$ (no change)
   - $2 \to 4$ (weight 9): $6 + 9 = 15 \Rightarrow$ `dist[4] = 15`, push `(15, 4)`
4. Pop `(8, 2)`. Stale entry! `currentDist (8) > dist[2] (6)`. Skip!
5. Pop `(9, 3)`. Relax neighbors:
   - $3 \to 4$ (weight 4): $9 + 4 = 13 < 15 \Rightarrow$ `dist[4] = 13`, push `(13, 4)`
6. Pop `(13, 4)`. No outgoing relaxations.
Final distances: `0:0, 1:4, 2:6, 3:9, 4:13`.

### Example 2: The FAANG Strict Inequality Trap
Let's trace a tricky graph setup designed to test your understanding of edge relaxation and heap mechanics.
**Graph**: `A -> B (w: 2)`, `A -> C (w: 5)`, `B -> C (w: 3)`, `C -> D (w: 1)`.
**Trace with Priority Queue `[cost, node]`**:
1. **Start at A**: `dist[A] = 0`, push `[0, A]`. PQ: `[0, A]`
2. **Pop A (0)**: Finalize A. Relax A's neighbors:
   - `B`: `dist[B] = 2`, push `[2, B]`. PQ: `[2, B]`
   - `C`: `dist[C] = 5`, push `[5, C]`. PQ: `[2, B], [5, C]`
3. **Pop B (2)**: Finalize B. Relax B's neighbors:
   - `C`: Current `dist[C]` is 5. Path via B is `2 + 3 = 5`. Since `5 < 5` is FALSE, we **do not** push `C` again. *(FAANG interviewers look closely for this optimization to check if you strictly use `<` vs `<=`).*
4. **Pop C (5)**: Finalize C. Relax C's neighbors:
   - `D`: `dist[D] = 5 + 1 = 6`, push `[6, D]`. PQ: `[6, D]`
5. **Pop D (6)**: Finalize D. No outgoing edges. PQ empty.
**Key Insight**: This trace proves why strict inequality (`<`) is crucial—it avoids redundant heap insertions on identical-distance paths.

---

## ⚠️ Common Interview Mistakes
1. **Defaulting to Max-Heap:** In C++, `priority_queue<pair<int, int>>` is a Max-Heap by default. You must explicitly declare `priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>>` to get the required Min-Heap behavior. Forgetting this is an instant red flag.
2. **Premature Termination on Push:** A very frequent bug is terminating the algorithm the moment the target node is pushed into the queue. The shortest path is only guaranteed when the target node is **popped** from the queue.
3. **Missing the Stale State Check:** Neglecting the `if (currentDist > dist[u]) continue;` check. Without it, you process obsolete, longer paths for nodes, degrading performance from $O((V+E) \log V)$ to $O(V \cdot E \log V)$ in dense graphs, often leading to TLE.
4. **Treating Reached as Visited:** Unlike BFS where reaching a node marks its shortest path as final, Dijkstra must allow `dist[v]` to be updated multiple times if a better path is found, before the node is eventually popped and finalized.
5. **Negative Weights:** Dijkstra does NOT work with negative weights because a path through a negative weight edge could reduce an already finalized vertex's distance. Use **Bellman-Ford**.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O((V + E) \log V)$ with binary heap.
- **Space Complexity:** $O(V + E)$ for adjacency list and heap.

## 🎯 Pattern Recognition — When to Use This
- **"Find the shortest/minimum cost path"**: If edge weights are positive/non-negative, this is a direct signal for Dijkstra.
- **"Minimizing maximum edge on a path" / "Maximizing minimum probability"**: Modified Dijkstra works perfectly for these bottleneck/max-min probability paths.
- **"Multiple sources to multiple destinations"**: If you can model a "super-source" connected to all starting points with weight 0, you can run SSSP to find the shortest path to any destination.

## 🔥 Interview Q&A — Google / Amazon Level

### Q1: Why doesn't Dijkstra's algorithm work with negative edge weights?
Dijkstra relies on a greedy invariant: once a vertex is popped from the priority queue, its shortest distance is finalized because any subsequent paths must be longer (since edge weights $\ge 0$). A negative edge violates this assumption, allowing a later path to potentially reduce the distance of an already finalized node.

### Q2: What is the time complexity difference between using a `priority_queue` (binary heap) and a `set` (BST)?
A binary heap gives $O((V + E) \log V)$ but doesn't support direct `decrease-key`. A `set` in C++ inherently supports erasing an old distance and inserting a new one, keeping the queue smaller (max size $V$), yielding $O(E \log V)$. However, the constant factor for `set` (pointer chasing in a Red-Black tree) is often higher than a vector-backed `priority_queue`, making `priority_queue` practically faster despite storing up to $E$ elements.

### Q3: How do you trace the actual shortest path, not just the distance?
Maintain a `parent` or `predecessor` array. When relaxing an edge: `if (dist[u] + weight < dist[v]) { dist[v] = ...; parent[v] = u; }`. To reconstruct the path, backtrack from the destination using `parent[dest]` until reaching the source.

### Q4: If the graph is an unweighted Directed Acyclic Graph (DAG), should you use Dijkstra?
No. For an unweighted graph, standard BFS computes SSSP in $O(V + E)$ time without a priority queue. For a weighted DAG, Topological Sorting followed by relaxation yields SSSP in $O(V + E)$ time, which is strictly faster than Dijkstra's $O((V + E) \log V)$.

### Q5: Can we terminate Dijkstra early if we only want the distance to a specific target node?
Yes. The moment the target node is popped from the priority queue, its shortest distance is finalized, and you can return immediately. Note: It must be when *popped*, not when *pushed* to the PQ.

### Q6: What if we use a Fibonacci Heap instead of a Binary Heap?
The theoretical time complexity improves to $O(V \log V + E)$ because `decrease-key` takes $O(1)$ amortized time. However, Fibonacci heaps are complex to implement and have large constant factors, making them rarely used in actual interview settings or standard libraries.

## 🏆 Related Problems (Leetcode)

- **[743. Network Delay Time](https://leetcode.com/problems/network-delay-time/)**: Classic SSSP to all nodes, finding the max time among all shortest paths.
- **[1514. Path with Maximum Probability](https://leetcode.com/problems/path-with-maximum-probability/)**: Dijkstra variant where you maximize the product of probabilities.
- **[1631. Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/)**: Dijkstra variant to minimize the maximum absolute difference on a path.
- **[787. Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/)**: Dijkstra with state (needs a slight modification to track steps, or use Bellman-Ford).

## 🔗 Cross-Topic Connections
- **Dynamic Programming / Memoization**: SSSP on a DAG can be seen as a DP problem evaluated in topological order.
- **A* Search**: A* is simply Dijkstra's algorithm with a heuristic function guiding the search towards the target.
- **Greedy Algorithms**: The fundamental premise of popping the closest unvisited node is a greedy choice.

## ⚡ 2-Minute Revision Flash Card

- **Concept**: Greedy SSSP using a Min-Heap.
- **Invariant**: Once a node is popped, its distance is final (requires non-negative weights).
- **Core Logic**: `if (dist[u] + w < dist[v]) { dist[v] = dist[u] + w; pq.push({dist[v], v}); }`
- **Complexity**: $O((V + E) \log V)$ time, $O(V + E)$ space.
- **Trap**: Must check for stale queue elements: `if (currDist > dist[u]) continue;`.
- **Negative Weights**: Fails. Use Bellman-Ford instead.
