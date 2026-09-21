# Lecture 95: Maximum Width of Binary Tree (LeetCode 662)

> **One-Line Purpose:** Calculate maximum horizontal tree width using 0-based heap indices with level-offset normalization to avoid 64-bit integer overflow.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #95  
> **Video ID:** `rhz-csskg_A`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=rhz-csskg_A)  
> **Duration:** 21:09  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Use complete binary tree indexing properties (Heap Indices) to calculate distances between nodes.
- Understand that the width of a level is `(index_of_last_node - index_of_first_node) + 1`.
- Handle extreme integer overflow by normalizing indices at the start of each level.

## 🧠 Core Intuition — Why This Works
A tree's "width" at a level includes all nodes and the `null` gaps between them. 
If we use array indexing (like in a Binary Heap), the root is at index `0`. Its left child is at `2*i + 1` and right child is at `2*i + 2`.
This indexing naturally preserves gaps! If a node is missing, its index is skipped, but the indices of the nodes that *do* exist remain perfectly accurate relative to each other.
The width of any level is simply the index of the rightmost node minus the index of the leftmost node, plus one.

**Visualization:**
```text
Tree:
        1          [Idx: 0]
      /   \
     3     2       [Idx: 1, 2]
    /       \
   5         9     [Idx: 3, 6]

Level 3 width = (6 - 3) + 1 = 4. 
(Indices 4 and 5 are the missing children of node 2).
```

## 🎯 Pattern Recognition — When to Use This
**Trigger cues:**
- "Width of a tree including null nodes"
- "Positions of nodes in a complete binary tree"
→ **Action:** Use BFS with a Queue storing pairs of `<TreeNode*, Index>`.

## 📐 Algorithm Walk-Through
1. Initialize `maxWidth = 0`. Use a queue storing `pair<TreeNode*, unsigned long long>`.
2. Push `{root, 0}` to the queue.
3. While the queue is not empty:
   - Get the `size` of the queue (number of nodes on current level).
   - Get `minIdx = q.front().second`. We will subtract this from all indices on this level to prevent integer overflow.
   - For `i = 0` to `size - 1`:
     - Pop `[node, curIdx]`.
     - Normalize it: `normIdx = curIdx - minIdx`.
     - If `i == 0`, record this as `first`.
     - If `i == size - 1`, record this as `last`.
     - Push children with normalized indices: Left $\rightarrow$ `2 * normIdx + 1`, Right $\rightarrow$ `2 * normIdx + 2`.
   - Update `maxWidth = max(maxWidth, last - first + 1)`.
4. Return `maxWidth`.

## 🔵 Complete C++ Overflow-Safe Implementation

```cpp
#include <queue>
#include <algorithm>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionWidth {
public:
    int widthOfBinaryTree(TreeNode* root) {
        if (!root) return 0;
        unsigned long long maxWidth = 0;

        queue<pair<TreeNode*, unsigned long long>> q;
        q.push({root, 0});

        while (!q.empty()) {
            int size = q.size();
            unsigned long long minIdx = q.front().second; // Offset for current level
            unsigned long long first = 0, last = 0;

            for (int i = 0; i < size; i++) {
                auto [node, curIdx] = q.front();
                q.pop();

                // Normalize index by subtracting minimum index of this level
                unsigned long long normIdx = curIdx - minIdx;
                if (i == 0) first = normIdx;
                if (i == size - 1) last = normIdx;

                if (node->left) q.push({node->left, 2 * normIdx + 1});
                if (node->right) q.push({node->right, 2 * normIdx + 2});
            }

            maxWidth = max(maxWidth, last - first + 1);
        }

        return (int)maxWidth;
    }
};
```

## 🔍 Dry Run Trace
**Tree:** `[1, 3, 2, 5, null, null, 9]`
- **Level 1:** Queue has `[{1, 0}]`.
  - `size = 1`, `minIdx = 0`.
  - Pop `{1, 0}`. `normIdx = 0 - 0 = 0`. `first=0, last=0`.
  - Push Left 3 at `2*0+1 = 1`. Push Right 2 at `2*0+2 = 2`.
  - `maxWidth = max(0, 0-0+1) = 1`.
- **Level 2:** Queue has `[{3, 1}, {2, 2}]`.
  - `size = 2`, `minIdx = 1`.
  - Pop `{3, 1}`. `normIdx = 1 - 1 = 0`. `first=0`.
    - Push Left 5 at `2*0+1 = 1`. Right is null.
  - Pop `{2, 2}`. `normIdx = 2 - 1 = 1`. `last=1`.
    - Left is null. Push Right 9 at `2*1+2 = 4`.
  - `maxWidth = max(1, 1-0+1) = 2`.
- **Level 3:** Queue has `[{5, 1}, {9, 4}]`.
  - `size = 2`, `minIdx = 1`.
  - Pop `{5, 1}`. `normIdx = 1 - 1 = 0`. `first=0`. (No children).
  - Pop `{9, 4}`. `normIdx = 4 - 1 = 3`. `last=3`. (No children).
  - `maxWidth = max(2, 3-0+1) = 4`.
- **Result:** `4`.

## ⚠️ Common Interview Mistakes
- **Ignoring Integer Overflow:** If a tree is highly skewed (e.g., all right children) and deep, the index `2*i + 2` grows exponentially. By depth 32, it will exceed the limits of a 32-bit integer, and by depth 64, it exceeds a 64-bit integer. 
- **Failing to Normalize:** Normalizing indices (subtracting the level's minimum index from all nodes on that level) solves the overflow problem completely because the maximum width on any level cannot exceed the maximum number of nodes, avoiding exponential growth down skewed paths.

## 📊 Complexity Analysis
- **Time Complexity:** $O(N)$ since every node is pushed and popped from the queue exactly once.
- **Space Complexity:** $O(W)$ where $W$ is the maximum width of the tree. In the worst case (a perfect binary tree), the bottom level has $N/2$ nodes, making space $O(N)$.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: [Overflow] Why did you use `unsigned long long` if you are normalizing the indices?
**Answer:** Even with normalization, if a level spans a huge width (e.g., millions of null nodes between two actual nodes), the indices could theoretically exceed a 32-bit `int` boundary just on that single level before the next normalization happens. Using `unsigned long long` provides absolute safety against standard test cases.

### Q2: [Alternative Traversal] Could we solve this using DFS?
**Answer:** Yes! Instead of a BFS queue, we can do DFS and maintain an array `first_index_of_level[]` indexed by depth. When visiting `(node, depth, idx)`, if `depth == first_index_of_level.size()`, we push `idx`. Then, we update the max width with `idx - first_index_of_level[depth] + 1`. This also requires index normalization.

### Q3: [Variant] How would you find the width without counting the `null` gaps between nodes?
**Answer:** That's just finding the maximum number of actual nodes on any level. BFS makes this trivial: just take the maximum value of `q.size()` across all iterations of the outer loop.

## 🏆 Related Problems (Leetcode)
- **Leetcode 102:** Binary Tree Level Order Traversal (Standard BFS)
- **Leetcode 654:** Maximum Binary Tree

## 🔗 Cross-Topic Connections
- **Heaps & Priority Queues:** The formula `2*i+1` and `2*i+2` is the foundation of array-based Binary Heaps.

## ⚡ 2-Minute Revision Flash Card
- **Pattern:** BFS Level-Order Traversal with Heap Indices.
- **Index Formula:** Left child = `2 * index + 1`, Right child = `2 * index + 2`.
- **Width Formula:** `last_index_in_level - first_index_in_level + 1`.
- **Overflow Fix:** Normalize indices per level by subtracting `q.front().second` from all nodes on that level.
