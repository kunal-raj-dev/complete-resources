# Topic 19: Graphs & Network Algorithms — Master Index

> **Domain:** Graph Traversals, DAG Topologies, Shortest Path Algorithms, Minimum Spanning Trees, DSU, and Connectivity

---

## 📋 Topic Overview

This module covers Graph Algorithms from foundational adjacency matrices/lists and BFS/DFS traversals to advanced algorithms: cycle detection, topological sorting (DFS and Kahn's), single-source shortest paths (Dijkstra, Bellman-Ford), minimum spanning trees (Prim's, Kruskal's), Disjoint Set Union ($O(\alpha(N))$), Tarjan's bridge and articulation points, Kosaraju's strongly connected components, and Floyd-Warshall all-pairs shortest paths.

---

## 📑 Lecture Index

| # | Lecture Title | Focus Areas | Notes Link | Status |
|---|---|---|---|---|
| **111** | Introduction to Graphs | Adjacency Matrix vs Adjacency List memory models | [01_graph_representations_matrix_and_list.md](./01_graph_representations_matrix_and_list.md) | **AUDITED** |
| **112** | BFS Traversal | Queue level-order traversal, disconnected graph safety | [02_breadth_first_search_bfs.md](./02_breadth_first_search_bfs.md) | **AUDITED** |
| **113** | DFS Traversal | Recursive call stack graph traversal | [03_depth_first_search_dfs.md](./03_depth_first_search_dfs.md) | **AUDITED** |
| **114** | Cycle Detection Undirected (DFS) | `parent` tracking, back-edge identification | [04_detect_cycle_undirected_dfs.md](./04_detect_cycle_undirected_dfs.md) | **AUDITED** |
| **115** | Cycle Detection Undirected (BFS) | Queue pair `(node, parent)` cross-edge detection | [05_detect_cycle_undirected_bfs.md](./05_detect_cycle_undirected_bfs.md) | **AUDITED** |
| **116** | Number of Islands | 2D matrix connected component flood fill | [06_number_of_islands_grid_bfs_dfs.md](./06_number_of_islands_grid_bfs_dfs.md) | **AUDITED** |
| **117** | Rotting Oranges | Multi-source BFS wavefront simulation | [07_rotting_oranges_multisource_bfs.md](./07_rotting_oranges_multisource_bfs.md) | **AUDITED** |
| **118** | Cycle Detection Directed (DFS) | `inStack` / path-visited state backtracking | [08_detect_cycle_directed_dfs.md](./08_detect_cycle_directed_dfs.md) | **AUDITED** |
| **119** | Topological Sort (DFS) | Postorder stack finish ordering for DAGs | [09_topological_sorting_dfs.md](./09_topological_sorting_dfs.md) | **AUDITED** |
| **120** | Course Schedule | Directed cycle detection for prerequisite feasibility | [10_course_schedule_cycle_detection.md](./10_course_schedule_cycle_detection.md) | **AUDITED** |
| **121** | Course Schedule II | Kahn's algorithm prerequisite sequence output | [11_course_schedule_ii_topological_order.md](./11_course_schedule_ii_topological_order.md) | **AUDITED** |
| **122** | Flood Fill Algorithm | 4-directional matrix pixel re-coloring | [12_flood_fill_algorithm.md](./12_flood_fill_algorithm.md) | **AUDITED** |
| **123** | Kahn's Algorithm (BFS) | In-degree queue processing, cycle detection | [13_kahns_algorithm_bfs_toposort.md](./13_kahns_algorithm_bfs_toposort.md) | **AUDITED** |
| **124** | Dijkstra's Algorithm | Min-heap greedy relaxation, non-negative weights | [14_dijkstras_algorithm_shortest_path.md](./14_dijkstras_algorithm_shortest_path.md) | **AUDITED** |
| **125** | Bellman-Ford Algorithm | Negative edge weights, negative cycle detection | [15_bellman_ford_algorithm.md](./15_bellman_ford_algorithm.md) | **AUDITED** |
| **126** | Series Roadmap Update | Advanced Graph curriculum overview | [16_dsa_series_advanced_topics_roadmap.md](./16_dsa_series_advanced_topics_roadmap.md) | **AUDITED** |
| **127** | Prim's Algorithm (MST) | Cut property, min-heap boundary expansion | [17_prims_algorithm_mst.md](./17_prims_algorithm_mst.md) | **AUDITED** |
| **128** | Disjoint Set Union (DSU) | Path compression, union by rank/size ($O(\alpha(N))$) | [18_disjoint_set_union_dsu.md](./18_disjoint_set_union_dsu.md) | **AUDITED** |
| **129** | Kruskal's Algorithm (MST) | Edge sorting, DSU cycle avoidance | [19_kruskals_algorithm_mst.md](./19_kruskals_algorithm_mst.md) | **AUDITED** |
| **130** | Number of Provinces | Connected components via DFS/DSU | [20_number_of_provinces.md](./20_number_of_provinces.md) | **AUDITED** |
| **131** | Min Cost Connect Points | Complete graph Manhattan MST | [21_min_cost_to_connect_all_points.md](./21_min_cost_to_connect_all_points.md) | **AUDITED** |
| **132** | Cheapest Flights Within K Stops | Bounded BFS distance relaxation | [22_cheapest_flights_within_k_stops.md](./22_cheapest_flights_within_k_stops.md) | **AUDITED** |
| **133** | Bridges in Graph (Tarjan) | DFS discovery `tin` and `low` time, critical edges | [23_bridges_in_graph_tarjans_algorithm.md](./23_bridges_in_graph_tarjans_algorithm.md) | **AUDITED** |
| **134** | Articulation Points (Tarjan) | Cut vertices condition (`low[v] >= tin[u]`) | [24_articulation_points_tarjans_algorithm.md](./24_articulation_points_tarjans_algorithm.md) | **AUDITED** |
| **135** | Kosaraju's Algorithm (SCC) | Transposed graph DFS, strongly connected components | [25_strongly_connected_components_kosaraju.md](./25_strongly_connected_components_kosaraju.md) | **AUDITED** |
| **136** | Floyd-Warshall Algorithm | Dynamic programming all-pairs shortest paths ($O(V^3)$) | [26_floyd_warshall_algorithm.md](./26_floyd_warshall_algorithm.md) | **AUDITED** |

---

## 🎯 Topic Revision & Interview Preparation
- **Topic Quick Revision:** [topic_revision.md](./topic_revision.md)
- **Topic Interview Question Bank:** [topic_interview_questions.md](./topic_interview_questions.md)
