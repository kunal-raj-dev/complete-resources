# Lecture 111: Introduction to Graphs: Representations & Memory Models

> **One-Line Purpose:** Master fundamental graph theory definitions, directed/undirected topologies, and implement Adjacency Matrix ($O(V^2)$) and Adjacency List ($O(V + 2E)$) representations.

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

## 🔵 Adjacency List C++ Implementation

```cpp
#include <iostream>
#include <vector>
using namespace std;

class Graph {
private:
    int V;
    vector<vector<pair<int, int>>> adj; // pair: <neighbor, weight>
    bool isDirected;

public:
    Graph(int vertices, bool directed = false) : V(vertices), isDirected(directed) {
        adj.resize(V);
    }

    void addEdge(int u, int v, int weight = 1) {
        adj[u].push_back({v, weight});
        if (!isDirected) {
            adj[v].push_back({u, weight});
        }
    }

    void printGraph() const {
        for (int i = 0; i < V; i++) {
            cout << i << " -> ";
            for (auto const& edge : adj[i]) {
                cout << "(" << edge.first << ", w:" << edge.second << ") ";
            }
            cout << endl;
        }
    }
};
```
