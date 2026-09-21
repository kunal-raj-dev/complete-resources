# Lecture 125: Bellman-Ford Algorithm: Negative Weight Cycles

> **One-Line Purpose:** Calculate single-source shortest paths on graphs with negative edge weights and reliably detect negative weight cycles in $O(V \times E)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #125  
> **Video ID:** `3rFHlbJ7qKc`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=3rFHlbJ7qKc)  
> **Duration:** 23:38  
> **Status:** AUDITED  

---

## 🔵 Algorithmic Invariant: $V-1$ Relaxations
A simple path in a graph with $V$ vertices contains at most $V - 1$ edges. Relaxing every edge in the graph $V - 1$ times guarantees that shortest paths of lengths $1, 2, \dots, V - 1$ edges are correctly computed.
**Negative Cycle Theorem:** If a further relaxation occurs on the $V$-th iteration, a **negative weight cycle** exists!

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <climits>

using namespace std;

struct Edge {
    int u, v, weight;
};

class BellmanFord {
public:
    static pair<bool, vector<int>> solve(int V, const vector<Edge>& edges, int src) {
        vector<int> dist(V, 1e9); // Use 1e9 to avoid 32-bit signed overflow
        dist[src] = 0;

        // 1. Relax all edges V - 1 times
        for (int i = 1; i <= V - 1; ++i) {
            bool anyRelaxed = false;
            for (const auto& e : edges) {
                if (dist[e.u] != 1e9 && dist[e.u] + e.weight < dist[e.v]) {
                    dist[e.v] = dist[e.u] + e.weight;
                    anyRelaxed = true;
                }
            }
            if (!anyRelaxed) break; // Early termination optimization
        }

        // 2. V-th iteration to detect negative weight cycle
        for (const auto& e : edges) {
            if (dist[e.u] != 1e9 && dist[e.u] + e.weight < dist[e.v]) {
                return {true, {}}; // Negative cycle detected!
            }
        }

        return {false, dist};
    }
};

int main() {
    int V = 5;
    vector<Edge> edges = {
        {0, 1, -1}, {0, 2, 4},
        {1, 2, 3}, {1, 3, 2}, {1, 4, 2},
        {3, 2, 5}, {3, 1, 1}, {4, 3, -3}
    };

    auto [hasCycle, dist] = BellmanFord::solve(V, edges, 0);
    if (hasCycle) {
        cout << "Graph contains a negative weight cycle!" << endl;
    } else {
        cout << "Distances from source 0: ";
        for (int d : dist) cout << d << " ";
        cout << endl;
    }
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(V \times E)$ worst-case.
- **Space Complexity:** $O(V)$ auxiliary space.

---

## 🧠 Core Intuition — Why This Works

**Real-World Analogy:** Think of Bellman-Ford like sending a wave of news across a telephone tree. In round 1, only direct contacts of the source get updated. In round 2, their neighbors get updated. After $V-1$ rounds, even the most distant node (connected by a chain of $V-1$ edges) has received the correct shortest-path news. The key insight is: **no simple path can have more than $V-1$ edges** (it would need to revisit a vertex, forming a cycle).

**ASCII Visualization — Relaxation Waves:**
```
Graph:  0 --(-1)--> 1 --(-3)--> 4
        |                       |
       (4)                     (+2)
        |                       |
        v                       v
        2 <--(3)-- 1            3

Round 0: dist = [0, INF, INF, INF, INF]
Round 1: Relax all edges from src=0
         dist = [0, -1,   4, INF, INF]   (0→1 gives -1, 0→2 gives 4)
Round 2: Relax from newly reachable nodes
         dist = [0, -1,   2,   1,   1]   (1→2: -1+3=2, 1→3: -1+2=1, 1→4: -1+2=1)
Round 3: Relax from 4→3 with weight -3
         dist = [0, -1,   2,  -2,   1]   (4→3: 1+(-3)=-2)
Round 4: No further relaxations possible → terminate early
```

**Key Insight:** After iteration $i$, all shortest paths using **at most $i$ edges** are correct. By iteration $V-1$, all paths are finalized. If the $V$-th iteration still relaxes an edge, it means a negative cycle is forcing distances to decrease indefinitely.

---

## 🎯 Pattern Recognition — When to Use This

**Keyword triggers from problem statements:**
- "Find shortest path" + "graph may have negative edge weights"
- "Detect negative weight cycle"
- "Currency arbitrage detection" (negative cycle in log-transformed exchange rates)
- "K stops / constraints on number of hops" → modified Bellman-Ford (LeetCode 787)
- Graph is sparse; otherwise prefer Floyd-Warshall for all-pairs

**Distinguish from similar problems:**
| Situation | Algorithm |
|---|---|
| Positive weights only | Dijkstra $O((V+E)\log V)$ |
| Negative weights, single source | **Bellman-Ford** $O(VE)$ |
| All-pairs, dense graph | Floyd-Warshall $O(V^3)$ |
| K-constrained hops + negative possible | Modified Bellman-Ford |

---

## 🔍 Dry Run Trace

**Input:** 4 vertices, edges: `{0→1, w=1}, {1→2, w=-3}, {2→3, w=2}, {3→1, w=-1}` (has negative cycle 1→2→3→1 with total weight -3-1+2=-2)

```
Initial:  dist = [0, INF, INF, INF]

Iteration 1:
  Relax (0,1,1):  dist[1] = min(INF, 0+1) = 1
  Relax (1,2,-3): dist[2] = min(INF, 1-3) = -2
  Relax (2,3,2):  dist[3] = min(INF, -2+2) = 0
  Relax (3,1,-1): dist[1] = min(1,  0-1)  = -1  ← already relaxing into cycle!

Iteration 2:
  Relax (1,2,-3): dist[2] = min(-2, -1-3) = -4  ← keeps getting smaller!
  ...

Iteration V=4 (detection pass):
  dist[1] relaxed again → NEGATIVE CYCLE DETECTED ✓
```

---

## ⚠️ Common Interview Mistakes

1. **Missing the `dist[u] != INF` guard:** Without it, `INF + negative_weight` wraps around to a valid-looking number. Always check reachability before relaxing.
   ```cpp
   // BUGGY — can cause overflow:
   if (dist[e.u] + e.weight < dist[e.v]) ...
   // CORRECT:
   if (dist[e.u] != 1e9 && dist[e.u] + e.weight < dist[e.v]) ...
   ```

2. **Running only V-1 iterations and forgetting the Nth pass:** The negative cycle detection REQUIRES one extra pass. Many candidates stop at V-1 and never detect the cycle.

3. **Using `INT_MAX` instead of `1e9`:** `INT_MAX + any_positive = undefined behavior` (integer overflow). Use `1e9` or `INT_MAX/2`.

4. **Directed vs. Undirected confusion:** In undirected graphs, an edge `(u,v,w)` with `w < 0` forms an immediate negative cycle `u→v→u`. Bellman-Ford is typically applied to directed graphs for this reason.

5. **Not processing edges in consistent order:** The order of edge relaxation doesn't affect correctness (only performance with early termination), but many candidates overthink this.

6. **SPFA confusion:** SPFA (Bellman-Ford with a queue) has the same worst-case as Bellman-Ford but is faster in practice. It can be tricked into $O(VE)$ worst case with adversarial inputs — **do not use SPFA in competitive programming** if the judge has anti-SPFA test cases.

---

## 🔥 Interview Q&A — Google/Amazon/Meta Level

### Q1: [Conceptual] Why exactly V-1 iterations and not V or V+1?
**Answer:** A simple path (no repeated vertices) in a graph with $V$ vertices can have at most $V-1$ edges. After iteration $i$ of Bellman-Ford, all shortest paths using **at most $i$ edges** are correctly computed. Therefore after $V-1$ iterations, even the longest possible simple path (of $V-1$ edges) is correctly computed. Doing more iterations is unnecessary IF no negative cycle exists. The $V$-th iteration is used purely as a detection mechanism: if any edge still relaxes, a shortest path would need $V$ or more edges, which means it must revisit a vertex, implying a negative cycle.

### Q2: [Conceptual] How does Bellman-Ford detect negative weight cycles?
**Answer:** After $V-1$ iterations, if any edge $(u, v, w)$ satisfies `dist[u] + w < dist[v]`, it means we found a path of $V$ edges that is shorter than any path of $\leq V-1$ edges. This is only possible if there's a negative cycle reachable from the source. The proof: in a graph without negative cycles, $V-1$ iterations always find the optimal solution. If the $V$-th relaxation changes a value, the "optimal path" has length $> V-1$ edges, implying a cycle, which must be negative (otherwise we'd never prefer it).

### Q3: [Comparison] Dijkstra vs Bellman-Ford — when does Dijkstra's greedy fail?
**Answer:** Dijkstra uses the invariant: once a node is popped from the min-heap, its distance is finalized. This assumes that all edge weights are non-negative, because no future edge can make the path cheaper. With negative weights, this assumption breaks: after finalizing node $u$, we might find edge $(v, u, -100)$ that, combined with a path to $v$, gives a cheaper path to $u$. Bellman-Ford doesn't finalize any distance prematurely — it re-examines all edges in every iteration. The cost: $O(VE)$ vs $O((V+E)\log V)$.

### Q4: [Debugging] What if we copy dist[] before each iteration and only update from the copy?
**Answer:** This gives the "correct" Bellman-Ford where after iteration $i$, we have shortest paths using **exactly $i$ edges** (not "at most $i$"). This is useful for problems like "Cheapest Flights Within K Stops" where we need exactly $K$ edges. Without copying (the standard implementation), a single relaxation in iteration $i$ can cascade within the same iteration, making some paths appear "found" in fewer iterations. Both versions are correct for the general shortest-path problem but behave differently on K-hop constrained problems.

### Q5: [Extension] What is SPFA and when does it fail?
**Answer:** SPFA (Shortest Path Faster Algorithm) is Bellman-Ford with a queue optimization: instead of relaxing ALL edges every iteration, only enqueue a vertex when its distance improves. Average case is $O(kE)$ where $k << V$, making it much faster in practice. However, adversarial graphs can force $O(VE)$ worst case, and some competitive programming judges include anti-SPFA tests. SPFA also detects negative cycles: if a vertex is enqueued more than $V$ times, a negative cycle exists.

### Q6: [System Design] How would you use Bellman-Ford for currency arbitrage detection?
**Answer:** Model currencies as vertices and exchange rates as directed edges with weight $-\log(\text{rate})$. A currency arbitrage opportunity exists when you can convert A→B→C→A and end up with more money than you started, i.e., $r_{AB} \times r_{BC} \times r_{CA} > 1$. Taking logarithms: $\log(r_{AB}) + \log(r_{BC}) + \log(r_{CA}) > 0$, which with negation becomes $(-\log(r_{AB})) + (-\log(r_{BC})) + (-\log(r_{CA})) < 0$. This is exactly a **negative cycle** in the transformed graph! Run Bellman-Ford: if a negative cycle is detected, arbitrage exists.

### Q7: [Output Prediction] What does this code output?
```cpp
// Graph: 3 vertices, edges: (0,1,1), (1,2,-2), (2,1,1)
// src = 0
vector<Edge> edges = {{0,1,1},{1,2,-2},{2,1,1}};
auto [hasCycle, dist] = BellmanFord::solve(3, edges, 0);
cout << hasCycle << " " << dist[1] << endl;
```
**Answer:** Outputs `1` (negative cycle detected). The cycle is 1→2→1 with total weight (-2+1) = -1, which is negative. The Nth-pass detection catches this. Note: `dist` is empty `{}` when a cycle is returned by the implementation above.

### Q8: [Proof] Prove the correctness of Bellman-Ford by induction.
**Answer:** **Claim:** After iteration $i$, `dist[v]` equals the shortest path from `src` to `v` using at most $i$ edges.  
**Base case:** $i=0$: `dist[src]=0`, all others $\infty$. Correct — shortest path using 0 edges.  
**Inductive step:** Assume true after iteration $i-1$. In iteration $i$, for every edge $(u,v,w)$, we try `dist[v] = min(dist[v], dist[u]+w)`. By induction, `dist[u]` is the shortest path using $\leq i-1$ edges. So `dist[u]+w` is the shortest path using $\leq i$ edges that goes through this specific edge. Since we try ALL edges, we find the minimum over all such paths. QED.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Approach |
|---|---|---|
| 787 | Cheapest Flights Within K Stops | Bellman-Ford with edge-level copy (K+1 iterations) |
| 743 | Network Delay Time | Bellman-Ford or Dijkstra (all positive weights) |
| 1334 | Find the City With the Smallest Number of Neighbors | Floyd-Warshall or Bellman-Ford per vertex |
| 1514 | Path with Maximum Probability | Modified Bellman-Ford (maximize, not minimize) |
| 1368 | Minimum Cost to Make at Least One Valid Path | 0-1 BFS (variant) |

---

## 🔗 Cross-Topic Connections

- **Dijkstra's Algorithm:** Bellman-Ford's faster sibling for non-negative weights. Dijkstra is BFS + greedy; Bellman-Ford is pure DP.
- **Floyd-Warshall:** All-pairs version. Run Bellman-Ford from every vertex = $O(V^2 E)$; Floyd-Warshall does it in $O(V^3)$.
- **Dynamic Programming:** Bellman-Ford IS DP: `dp[i][v]` = shortest path to `v` using at most `i` edges.
- **Topological Sort:** On DAGs, you can find shortest paths in $O(V+E)$ using toposort + relaxation — no negative cycle possible!
- **DSU:** Both detect cycles; DSU detects structural cycles, Bellman-Ford detects negative-weight cycles.

---

## ⚡ 2-Minute Revision Flash Card

- **When to use:** Negative edge weights OR need to detect negative cycles
- **Core loop:** $V-1$ iterations × all edges = relax greedily
- **Negative cycle detection:** Run ONE more iteration; if any edge relaxes → cycle exists
- **Guard:** Always check `dist[u] != INF` before relaxing to prevent overflow
- **vs Dijkstra:** Dijkstra is faster ($O((V+E)\log V)$) but fails with negative weights; Bellman-Ford is $O(VE)$ but handles them
