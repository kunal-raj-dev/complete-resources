# Lecture 111: Introduction to Graphs: Representations & Memory Models

> **One-Line Purpose:** Master foundational graph theory definitions (nodes, directed/undirected edges, weighted topologies, degrees) and implement both Adjacency Matrix ($O(V^2)$ space) and Adjacency List ($O(V + 2E)$ space) in modern C++.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #111  
> **Video ID:** `RpgyCJBbl5E`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=RpgyCJBbl5E)  
> **Duration:** 26:08  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
By the end of this lecture, you should understand:
- Mathematical definition of a Graph $G = (V, E)$.
- Distinction between Directed (Digraphs) and Undirected Graphs.
- In-degree, Out-degree, and the Handshaking Lemma ($\sum \deg(v) = 2|E|$).
- Memory footprints and trade-offs of Adjacency Matrix vs. Adjacency List.
- Production-grade C++ encapsulation using `std::vector<std::vector<pair<int, int>>>`.

---

## 🔵 Algorithmic Intuition & Core Principles

A Graph models pairwise relationships between discrete entities:
```
Undirected Graph (V=4, E=4):
    0 ------ 1
    |      / |
    |    /   |
    |  /     |
    2 ------ 3
```

### Representation Comparison

| Property | Adjacency Matrix (`int adj[V][V]`) | Adjacency List (`vector<vector<Edge>>`) |
|---|---|---|
| **Space Complexity** | $\Theta(V^2)$ regardless of $E$ | $\Theta(V + E)$ (Directed) / $\Theta(V + 2E)$ (Undirected) |
| **Edge Lookup ($u \leftrightarrow v$)** | $O(1)$ direct array indexing | $O(\deg(u))$ scan through neighbors |
| **Iterate All Neighbors of $u$** | $O(V)$ scans whole row | $O(\deg(u))$ strictly visits actual edges |
| **Add Vertex** | $O(V^2)$ reallocation cost | $O(1)$ amortized `push_back()` |
| **Best Used For** | Dense Graphs ($E \approx V^2$) | Sparse Graphs ($E \ll V^2$, 99% of interviews) |

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <utility>

using namespace std;

// Weighted Edge Representation
struct Edge {
    int to;
    int weight;
    Edge(int target, int w) : to(target), weight(w) {}
};

class Graph {
private:
    int V;
    bool isDirected;
    vector<vector<Edge>> adjList;
    vector<vector<int>> adjMatrix;

public:
    Graph(int vertices, bool directed = false) : V(vertices), isDirected(directed) {
        adjList.resize(V);
        adjMatrix.assign(V, vector<int>(V, 0));
    }

    // Add Edge to both representations
    void addEdge(int u, int v, int weight = 1) {
        if (u < 0 || u >= V || v < 0 || v >= V) return;

        // 1. Adjacency Matrix
        adjMatrix[u][v] = weight;
        if (!isDirected) adjMatrix[v][u] = weight;

        // 2. Adjacency List
        adjList[u].push_back(Edge(v, weight));
        if (!isDirected) adjList[v].push_back(Edge(u, weight));
    }

    void printAdjList() const {
        cout << "--- Adjacency List ---" << endl;
        for (int i = 0; i < V; ++i) {
            cout << "Vertex " << i << ":";
            for (const auto& edge : adjList[i]) {
                cout << " -> (" << edge.to << ", w=" << edge.weight << ")";
            }
            cout << "\n";
        }
    }

    bool hasEdge(int u, int v) const {
        return adjMatrix[u][v] != 0;
    }
};

int main() {
    Graph g(4, false);
    g.addEdge(0, 1, 10);
    g.addEdge(0, 2, 15);
    g.addEdge(1, 3, 20);
    g.addEdge(2, 3, 25);

    g.printAdjList();
    cout << "Edge 0-1 exists? " << (g.hasEdge(0, 1) ? "YES" : "NO") << endl;
    return 0;
}
```

---

## 🔍 Step-by-Step Trace & Memory Walkthrough
For $V = 4$, Edges: $(0,1,10), (0,2,15), (1,3,20), (2,3,25)$:
```
adjList[0] = [{1, 10}, {2, 15}]
adjList[1] = [{0, 10}, {3, 20}]
adjList[2] = [{0, 15}, {3, 25}]
adjList[3] = [{1, 20}, {2, 25}]
```
Total stored elements in vector buffers: $2 \times E = 8$ edges + 4 head pointers. Total memory is strictly $O(V + E)$ compared to $4 \times 4 = 16$ matrix cells.

---

## ⚠️ Common Pitfalls & Corner Cases
1. **Self Loops and Parallel Edges:** An adjacency matrix overwrites parallel edges unless a multiset/counter is maintained. Adjacency list naturally stores multigraph edges.
2. **0-indexed vs 1-indexed Vertices:** Competitive programming questions often give vertices $1 \dots N$. Always resize adjacency vectors to $N+1$ or subtract 1 from inputs to prevent out-of-bounds segfaults.
3. **Integer Memory Limit:** An adjacency matrix for $V = 10^5$ vertices requires $(10^5)^2 \times 4\text{ bytes} \approx 40\text{ GB}$, triggering an instant Memory Limit Exceeded (MLE). Always use Adjacency List for $V > 5000$.

---

## 🔥 FAANG Technical Interview Follow-Ups
- **Q: How does graph density affect choice of representation?**  
  *A:* Dense graphs ($E = \Theta(V^2)$) benefit from Adjacency Matrix because checking edge existence is $O(1)$ and space is asymptotically identical to list ($V^2$). Sparse graphs ($E = O(V)$) require Adjacency List to avoid $O(V^2)$ memory and $O(V)$ neighbor-scan penalties.
- **Q: What is the Handshaking Lemma and why does it matter?**  
  *A:* Every undirected edge contributes 2 to the sum of vertex degrees: $\sum_{v \in V} \deg(v) = 2|E|$. This implies the number of vertices with odd degree must be even.

---

## ⏱️ Complexity Analysis
- **Time Complexity:**
  - Add Edge: $O(1)$
  - Check Edge: Matrix $O(1)$, List $O(\deg(u))$
  - Enumerate Neighbors: Matrix $O(V)$, List $O(\deg(u))$
- **Space Complexity:**
  - Matrix: $\Theta(V^2)$
  - List: $\Theta(V + E)$
