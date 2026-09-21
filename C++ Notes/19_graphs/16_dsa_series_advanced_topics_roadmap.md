# Lecture 126: DSA Series Advanced Topics Roadmap: MSTs, DSU & Connectivity

> **One-Line Purpose:** Architectural roadmap bridging foundational graph traversals to advanced network algorithms: Minimum Spanning Trees (Prim's & Kruskal's), Disjoint Set Union (DSU), Bridges & Articulation Points (Tarjan's), Strongly Connected Components (Kosaraju's), and All-Pairs Shortest Paths (Floyd-Warshall).

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #126  
> **Video ID:** `YlmU4gBgePA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=YlmU4gBgePA)  
> **Duration:** 06:24  
> **Status:** AUDITED  

---

## 🗺️ Advanced Graph Curriculum Architecture

```
                       Advanced Graph Algorithms
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
Minimum Spanning Trees     Disjoint Set Union       Network Connectivity
 (Prim's & Kruskal's)     (Rank & Path Compress)    (Bridges & Articulation)
         │                        │                        │
         ▼                        ▼                        ▼
Greedy Cut/Cycle Property     O(α(N)) DSU           Tarjan's Discovery Time
Spanning Forest               Cycle Detection       Kosaraju's 2-Pass SCC
```

---

## ⏱️ Advanced Graph Complexity Summary Matrix

| Algorithm | Domain / Problem | Time Complexity | Auxiliary Space |
|---|---|---|---|
| **Prim's Algorithm** | Minimum Spanning Tree (MST) | $O((V + E) \log V)$ | $O(V)$ |
| **Kruskal's Algorithm** | Minimum Spanning Tree (MST) | $O(E \log E)$ | $O(V)$ |
| **DSU (Path + Rank)** | Dynamic Disjoint Set Union | $O(\alpha(N)) \approx O(1)$ | $O(N)$ |
| **Tarjan's Bridges** | Critical Connections / Cut Edges | $O(V + E)$ | $O(V)$ |
| **Tarjan's Articulation**| Cut Vertices | $O(V + E)$ | $O(V)$ |
| **Kosaraju's Algorithm**| Strongly Connected Components | $O(V + E)$ | $O(V)$ |
| **Floyd-Warshall** | All-Pairs Shortest Path (APSP) | $O(V^3)$ | $O(V^2)$ |
