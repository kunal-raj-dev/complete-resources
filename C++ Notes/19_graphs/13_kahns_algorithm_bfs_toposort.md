# Lecture 123: Topological Sorting using Kahn's Algorithm (BFS)

> **One-Line Purpose:** Implement in-degree-driven BFS topological sorting and detect directed cycles in $O(V + E)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #123  
> **Video ID:** `BnQpaTZg6Sc`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=BnQpaTZg6Sc)  
> **Duration:** 18:47  
> **Status:** AUDITED  

---

## 🔵 Kahn's Algorithm Invariant
A node with `inDegree == 0` has zero unfulfilled dependencies and is safe to process immediately. Removing it decrements its neighbors' in-degrees. If the final ordering count $< V$, a cycle exists!
