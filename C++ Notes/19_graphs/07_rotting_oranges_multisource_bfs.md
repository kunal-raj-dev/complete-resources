# Lecture 117: Rotting Oranges: Multi-Source BFS (LeetCode 994)

> **One-Line Purpose:** Determine minimum elapsed minutes until all fresh oranges rot by simultaneously propagating infection from all rotten sources via level-order BFS.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #117  
> **Video ID:** `RmXo5SWkhCs`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=RmXo5SWkhCs)  
> **Duration:** 26:22  
> **Status:** AUDITED  

---

## 🔵 Multi-Source BFS Principle
Unlike single-source BFS, all initially rotten oranges ($grid[r][c] = 2$) are enqueued at time $t = 0$. The queue expands in coordinated concentric time layers.

---

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <queue>
#include <iostream>

using namespace std;

class SolutionRottingOranges {
public:
    int orangesRotting(vector<vector<int>>& grid) {
        int rows = grid.size();
        int cols = grid[0].size();
        queue<pair<int, int>> q;
        int freshCount = 0;

        // 1. Enqueue all rotten oranges and count fresh ones
        for (int r = 0; r < rows; ++r) {
            for (int c = 0; c < cols; ++c) {
                if (grid[r][c] == 2) {
                    q.push({r, c});
                } else if (grid[r][c] == 1) {
                    freshCount++;
                }
            }
        }

        if (freshCount == 0) return 0; // Already zero fresh oranges

        int minutes = 0;
        int dRow[] = {-1, 1, 0, 0};
        int dCol[] = {0, 0, -1, 1};

        // 2. Layer-by-layer infection spread
        while (!q.empty() && freshCount > 0) {
            int layerSize = q.size();
            minutes++;

            for (int i = 0; i < layerSize; ++i) {
                auto [r, c] = q.front();
                q.pop();

                for (int d = 0; d < 4; ++d) {
                    int nr = r + dRow[d];
                    int nc = c + dCol[d];

                    if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] == 1) {
                        grid[nr][nc] = 2; // Infect
                        freshCount--;
                        q.push({nr, nc});
                    }
                }
            }
        }

        return freshCount == 0 ? minutes : -1;
    }
};

int main() {
    vector<vector<int>> grid = {
        {2, 1, 1},
        {1, 1, 0},
        {0, 1, 1}
    };
    SolutionRottingOranges solver;
    cout << "Minutes to rot: " << solver.orangesRotting(grid) << endl; // Output: 4
    return 0;
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(M \times N)$
- **Space Complexity:** $O(M \times N)$ for the queue.

---

## 🧠 Core Intuition — Why This Works

### Real-World Analogy: Epidemic Spreading from Multiple Hotspots
Imagine a disease outbreak starting simultaneously in multiple cities. The infection spreads to neighboring cities each day. You want to know when the last uninfected city gets infected (or if some are geographically isolated and unreachable).

Multi-source BFS models this exactly: all initial "hotspots" (rotten oranges, or infected cities) are treated as a single simultaneous wave-front at $t = 0$.

```
Grid:            t=0:         t=1:         t=2:         t=3:         t=4:
2 1 1            2 1 1        2 2 1        2 2 2        2 2 2        2 2 2
1 1 0   →        2 1 0   →    2 2 0   →    2 2 0   →    2 2 0   →    2 2 0
0 1 1            0 1 1        0 1 1        0 2 1        0 2 2        0 2 2

Initial rotten: {(0,0)}
t=1: Infect (0,1) and (1,0)
t=2: Infect (0,2) from (0,1); infect (1,1) from (1,0)
t=3: Infect (2,1) from (1,1)
t=4: Infect (2,2) from (2,1)
Answer: 4 minutes ✓
```

### Key Insight: Why Multi-Source BFS is NOT "Run BFS from each rotten orange separately"
If we ran BFS from each rotten orange independently, we'd get the wrong answer:
- Single-source BFS from `(0,0)` would give "5 minutes to reach `(2,2)`"
- But with multiple sources, `(1,0)` starts rotting simultaneously, cutting the time to 4.

Multi-source BFS captures the simultaneous spreading by initializing the queue with **all** sources before starting the BFS loop. This is equivalent to adding a virtual super-source $S$ connected to all rotten oranges with 0-weight edges, then running single-source BFS from $S$.

---

## 🎯 Pattern Recognition — When to Use Multi-Source BFS

| Problem Cue | Multi-Source BFS Application |
|---|---|
| "Minimum time/steps from ANY of multiple sources" | Enqueue all sources at $t=0$ |
| "Spread/infection/fire from multiple origins" | All origins go into queue first |
| "Distance to nearest X from every cell" | Enqueue all X positions |
| "Walls and Gates" (nearest gate) | Enqueue all gate positions |
| "01 Matrix" (nearest 0 for each cell) | Enqueue all 0 positions |

### Single-Source vs Multi-Source BFS
| Property | Single-Source BFS | Multi-Source BFS |
|---|---|---|
| Initial queue | One source node | All source nodes simultaneously |
| Distance semantics | Distance from that one source | Distance from nearest source |
| Virtual equivalent | Direct BFS | Single-source BFS from virtual super-node |
| Time complexity | $O(V + E)$ | $O(V + E)$ — same |

---

## 📐 Algorithm Walk-Through

**Why use `layerSize` to track minutes?**

The key challenge is knowing when one "minute" ends and the next begins. The `layerSize` snapshot captures how many nodes are in the current wave-front:

```
After init:     Queue = [(0,0), (other_initial_rotten...)]
                layerSize = number of initially rotten oranges

Minute 1:       Process all layerSize nodes.
                Push their fresh neighbors (infected at minute 1).
                
Minute 2:       Process all nodes pushed during minute 1.
                Push their fresh neighbors (infected at minute 2).
                ...
```

Without the `layerSize` trick, we'd need to enqueue sentinel markers `(-1,-1)` between levels — less clean.

**Termination conditions:**
- `freshCount == 0`: All fresh oranges rotted → return `minutes`.
- Queue empty but `freshCount > 0`: Some oranges are isolated (surrounded by `0`s) → return `-1`.

---

## ⚠️ Common Interview Mistakes

### 1. Forgetting the Early Return When freshCount == 0
```cpp
// ❌ Without this guard:
// If there are no fresh oranges at all, the while loop never runs.
// minutes stays 0, freshCount stays 0, returns 0. Actually OK BUT:
// The code is cleaner and avoids edge-case reasoning with the guard:
if (freshCount == 0) return 0;
```

### 2. Incrementing Minutes for Empty Layers
```cpp
// ❌ WRONG — increments minutes even when queue has initial rotten but no fresh neighbors
while (!q.empty()) {
    minutes++; // Increments BEFORE processing!
    int layerSize = q.size();
    for (int i = 0; i < layerSize; ++i) { ... }
}
// For input [[2]], returns minutes=1 instead of 0
```
The guard `freshCount == 0` before the loop prevents this. Also, the `while` condition `!q.empty() && freshCount > 0` ensures we don't process extra layers when all fresh are already rotted.

### 3. Not Using Layer-by-Layer Processing (Wrong Time Count)
```cpp
// ❌ WRONG — counts individual node pops as "minutes"
int minutes = 0;
while (!q.empty()) {
    auto [r, c] = q.front(); q.pop();
    minutes++; // Wrong! Each POP is not one minute
    // ...
}
```
Minutes correspond to **BFS levels**, not individual node pops. Use `layerSize` to batch-process each level.

### 4. Not Checking `grid[nr][nc] == 1` (Revisiting Rotten Oranges)
```cpp
// ❌ WRONG — would push already-rotten oranges again
if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] != 0) { ... }
// Should check == 1 specifically, not != 0
```

### 5. Returning `minutes - 1` (Off-by-One)
The `minutes` counter is incremented at the start of each layer processing, before any infections are made. Alternatively, increment after processing. Be consistent — the provided implementation increments at the start of each layer.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Why is BFS the right algorithm here, not DFS?

**Answer:** BFS is correct because we need to find the **minimum time** for all oranges to rot. BFS explores in concentric layers, where each layer corresponds to one unit of time. The first time BFS reaches a fresh orange from any rotten orange, it gives the minimum time to rot that orange (since BFS guarantees shortest path in unweighted graphs).

DFS would explore deep paths first and cannot guarantee minimum time. Consider:
```
2 - 1 - 1 - 1
        |
        2
```
DFS might compute time to rot the last `1` as 3 (going left from the right rotten orange), missing the shorter path of 1 (going up from the bottom rotten orange). BFS simultaneously explores from both rotten oranges and naturally picks the minimum.

### Q2: [Extension] How do you handle the case where some fresh oranges can never be reached?

**Answer:** After the BFS loop completes, check `freshCount`:
- If `freshCount == 0`: All fresh oranges were reachable and have rotted → return `minutes`.
- If `freshCount > 0`: Some fresh oranges are surrounded by empty cells (`0`) with no path to any rotten orange → return `-1`.

The check `return freshCount == 0 ? minutes : -1;` handles this exactly. No special "reachability" pre-computation is needed — BFS naturally doesn't visit isolated cells.

### Q3: [Variant] What if the grid also contains walls that neither oranges nor rot can pass through? How does the algorithm change?

**Answer:** The current implementation already handles this! Cell value `0` means "empty" — BFS only infects cells with value `1` (fresh orange). Walls could be represented as a new value, say `3`, and the BFS condition `grid[nr][nc] == 1` would skip them automatically.

No structural change needed — just add the wall value to your grid representation and ensure the BFS only spreads to fresh oranges.

### Q4: [Complexity] Is the time complexity truly $O(M \times N)$? Justify it.

**Answer:** Yes. Each cell `(r, c)` is enqueued at most **once**:
- Rotten oranges are enqueued at initialization (once).
- Fresh oranges are enqueued when they become rotten (and their value is immediately changed to `2`, preventing re-enqueueing).
- Empty cells (`0`) are never enqueued.

Total enqueues ≤ $M \times N$. Each dequeue processes 4 neighbors in $O(1)$. Initialization scan: $O(M \times N)$. Total: $O(M \times N)$.

### Q5: [Bug Prediction] What is the output of this code for grid `[[2,1,1],[0,1,1],[1,0,1]]`?
```cpp
// Same algorithm but minutes is incremented AFTER the while loop
int minutes = 0;
while (!q.empty() && freshCount > 0) {
    int layerSize = q.size();
    for (int i = 0; i < layerSize; ++i) {
        // ... process and push neighbors
    }
    minutes++; // Incremented after processing each layer
}
return freshCount == 0 ? minutes : -1;
```
**Answer:** The output would be `4` (correct for this grid). Moving `minutes++` to after the layer processing loop (vs. before) gives the same result as long as you don't increment for the "initial" layer. The key: increment once per layer processed, whether before or after the inner for loop. Both placements work correctly with the given while-loop structure.

### Q6: [Multi-Source BFS Design] How would you adapt this to: "Find the minimum distance from each cell to the nearest gate, given a grid with walls, gates, and rooms"?

**Answer:** This is LeetCode 286 "Walls and Gates":
1. Initialize: Enqueue all gate positions `(INF=0 cells)` into the queue simultaneously.
2. BFS: For each gate, spread to adjacent rooms, assigning distance = current BFS level.
3. Since BFS expands layer by layer, the first time a room is visited = its distance to the nearest gate.

```cpp
void wallsAndGates(vector<vector<int>>& rooms) {
    int rows = rooms.size(), cols = rooms[0].size();
    queue<pair<int,int>> q;
    const int INF = 2147483647;
    for (int r = 0; r < rows; ++r)
        for (int c = 0; c < cols; ++c)
            if (rooms[r][c] == 0) q.push({r, c}); // Enqueue all gates
    
    int dr[] = {-1,1,0,0}, dc[] = {0,0,-1,1};
    while (!q.empty()) {
        auto [r, c] = q.front(); q.pop();
        for (int d = 0; d < 4; ++d) {
            int nr = r+dr[d], nc = c+dc[d];
            if (nr>=0 && nr<rows && nc>=0 && nc<cols && rooms[nr][nc]==INF) {
                rooms[nr][nc] = rooms[r][c] + 1; // Distance from nearest gate
                q.push({nr, nc});
            }
        }
    }
}
```
Same multi-source BFS pattern as Rotting Oranges.

### Q7: [System Design] How would you scale "Rotting Oranges" to a city-scale disease simulation with millions of grid cells?

**Answer:** For a $10^6 \times 10^6$ grid:
1. **Sparse representation:** Most cells are `0` (empty). Store only non-empty cells in a hash map: `unordered_map<int, int> grid` where key = `r * cols + c`.
2. **Distributed BFS:** Partition the grid into blocks. Each machine handles a block. Border cells require inter-machine communication.
3. **Level-synchronous BFS:** Use barrier synchronization between levels — all machines process the current level before any proceeds to the next.
4. **Memory:** Queue holds only the "frontier" cells (currently rotten, about to spread). For a spreading epidemic, frontier size is $O(\sqrt{\text{area}})$ at any given time.

---

## 🏆 Related LeetCode Problems

| # | Problem | Approach Hint |
|---|---|---|
| 542 | 01 Matrix | Multi-source BFS from all 0s; find distance to nearest 0 |
| 286 | Walls and Gates | Multi-source BFS from all gates simultaneously |
| 1765 | Map of Highest Peak | Multi-source BFS from all water cells |
| 200 | Number of Islands | Single-source BFS per component |
| 1162 | As Far from Land as Possible | Multi-source BFS from all land cells |

---

## 🔗 Cross-Topic Connections

- **BFS (File 02):** Multi-source BFS is BFS with multiple initial nodes. The level-counting technique (layerSize) is BFS with level tracking.
- **Number of Islands (File 06):** Same grid DFS/BFS framework, but counting components instead of timing.
- **Flood Fill (File 12):** Single-source grid spreading — Rotting Oranges is the multi-source timed variant.
- **Shortest Path in Weighted Graphs (Dijkstra):** Multi-source Dijkstra works similarly — enqueue all sources with distance 0.
- **BFS Level Order:** The `layerSize` technique is identical to binary tree level-order traversal.

---

## ⚡ 2-Minute Revision Flash Card

- **Multi-source BFS:** Enqueue ALL rotten oranges at $t=0$, THEN start the while loop.
- **Count fresh oranges** upfront; decrement when infected. Return `-1` if any remain after BFS.
- **Layer tracking:** Snapshot `layerSize = q.size()` at the start of each minute, process exactly that many nodes.
- **Infection condition:** Only spread to `grid[nr][nc] == 1`; mark as `2` immediately on enqueue.
- **Time & Space:** $O(M \times N)$ — each cell is enqueued at most once.
