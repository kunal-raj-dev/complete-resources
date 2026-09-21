# Lecture 88: Diameter of Binary Tree (LeetCode 543)

> **One-Line Purpose:** Calculate the longest path between any two nodes in a tree using bottom-up height computation to achieve strictly $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #88  
> **Video ID:** `aPyDPImR5UM`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=aPyDPImR5UM)  
> **Duration:** 19:29  
> **Status:** AUDITED  

---

## 🧠 Core Intuition — Why This Works

The **diameter** is the longest path between any two nodes. The path doesn't have to pass through the root — it can pass through any node.

**Real-world analogy:** Imagine a city road network shaped like a tree. The diameter is the longest possible direct route between any two intersections. The "longest route" might pass through the center of the city (root), or it might be an entirely local route within a neighborhood (subtree).

```
Example where diameter passes through root:
         1           ← longest path: 4→2→1→3 (3 edges)
        / \
       2   3
      /
     4

Example where diameter does NOT pass through root:
         1           ← longest path: 4→2→5 (2 edges, NOT through root 1)
        /
       2
      / \
     4   5
```

**Key Insight:** At any node $u$, the longest path THROUGH $u$ is:
$$\text{pathThrough}(u) = \text{leftHeight}(u) + \text{rightHeight}(u)$$

The global diameter is the maximum of this value across ALL nodes. So we need to compute this efficiently for every node.

**Naive approach ($O(N^2)$):** For each node, call `height(left) + height(right)`. But `height()` itself is $O(N)$, so total is $O(N^2)$.

**Optimal approach ($O(N)$):** Compute height in a postorder fashion. As we return the height from each recursive call, simultaneously update the global diameter. Each node is visited exactly once.

```
Postorder walk for diameter:

Node 4: lh=0, rh=0, path=0, height=1
Node 5: lh=0, rh=0, path=0, height=1
Node 2: lh=1, rh=1, path=2 ← UPDATE maxDiameter=2, height=2
Node 3: lh=0, rh=0, path=0, height=1
Node 1: lh=2, rh=1, path=3 ← UPDATE maxDiameter=3, height=3

Final diameter = 3 ✓
```

---

## 🎯 Pattern Recognition — When to Use This

- "Longest path between any two nodes" → Diameter
- "Diameter" combined with "Binary Tree" → Bottom-up postorder with global max
- If they say "path through root" → simpler (just left height + right height at root)
- If they say "any two nodes" → must check at EVERY node, not just root

**Distinguish:** Diameter (path between nodes) vs. Height (root to deepest leaf). Diameter = height_left + height_right at the "bridge" node.

---

## 🔵 Bottom-Up Optimization
A naive recursive approach recomputes height at every node, taking $O(N^2)$.
By returning height from each post-order subtree call, the diameter passing through node $u$ is simply $\text{leftHeight} + \text{rightHeight}$, computing both in a single $O(N)$ pass.

---

## 💻 Complete C++ Implementation

```cpp
#include <algorithm>
#include <iostream>

using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionDiameter {
private:
    int maxDiameter = 0;

    int calculateHeight(TreeNode* root) {
        if (!root) return 0;

        int lh = calculateHeight(root->left);
        int rh = calculateHeight(root->right);

        // Longest path through root
        maxDiameter = max(maxDiameter, lh + rh);

        return 1 + max(lh, rh);
    }

public:
    int diameterOfBinaryTree(TreeNode* root) {
        maxDiameter = 0;
        calculateHeight(root);
        return maxDiameter;
    }
};

int main() {
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);

    SolutionDiameter solver;
    cout << "Diameter: " << solver.diameterOfBinaryTree(root) << endl; // Output: 3 (edges: 4-2-1-3 or 5-2-1-3)
    return 0;
}
```

---

## 🔍 Dry Run Trace

```
Tree:      1
          / \
         2   3
        / \
       4   5

calculateHeight(4): lh=0, rh=0, maxD=max(0,0+0)=0, return 1
calculateHeight(5): lh=0, rh=0, maxD=max(0,0+0)=0, return 1
calculateHeight(2): lh=1, rh=1, maxD=max(0,1+1)=2, return 2
calculateHeight(3): lh=0, rh=0, maxD=max(2,0+0)=2, return 1
calculateHeight(1): lh=2, rh=1, maxD=max(2,2+1)=3, return 3

Answer: 3 (path: 4→2→1→3 or 5→2→1→3)
```

---

## ⚠️ Common Interview Mistakes

1. **Only checking at root:** `return height(root->left) + height(root->right)` — this misses diameters entirely within a subtree. The global max must be updated at EVERY node.

2. **Forgetting `maxDiameter = 0` reset:** If you reuse the solver object, `maxDiameter` from the previous call persists. Always reset in the public method.

3. **Confusing diameter with height:** Diameter = `lh + rh` (edges between two deepest leaves through a node). Height = `1 + max(lh, rh)` (single longest path downward).

4. **Off-by-one with node-based vs edge-based height:** If using node-based height, diameter = lh + rh - 1 (subtract 1 because the root node is counted in both). The code above uses edge-based height (null=0, leaf=1), so `lh + rh` = number of edges in the path. ✓

5. **"What if interviewer asks: diameter of the LONGEST PATH with values?"** → Then you can't just track count; you'd need to track weighted paths (modify to return sum, not count).

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$ — each node visited exactly once via postorder DFS.
- **Space Complexity:** $O(H)$ recursion stack depth.
  - Best case (balanced): $O(\log N)$
  - Worst case (skewed): $O(N)$

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] What is the difference between the diameter of a binary tree and its height?
**Answer:** 
- **Height** of a tree = the longest path from root to any leaf = a single downward path. It's anchored at the root.
- **Diameter** = the longest path between any two nodes in the tree. The path can go up from one node, cross an ancestor, and go down to another. It equals `max(leftHeight + rightHeight)` evaluated at the optimal "bridge" node, which may not be the root.
- Relationship: `diameter ≤ 2 * height`. Equality holds when the two deepest leaves are in opposite subtrees of the root.

### Q2: [Deep Dive] Why does the recursive solution naturally handle the case where the diameter doesn't pass through the root?
**Answer:** Because we update `maxDiameter` at EVERY node during the postorder traversal — not just at the root. When `calculateHeight` visits node 2 in the example, it computes `lh+rh = 2` and updates `maxDiameter`. The root (node 1) may compute `lh+rh = 3`, which is larger and becomes the new max. The postorder nature guarantees that by the time we evaluate any node, its children have already been evaluated, so all sub-diameters have already been considered.

### Q3: [Output Prediction] What does this naïve solution return for a path-shaped tree 1→2→3→4→5?
```cpp
int naiveDiameter(TreeNode* root) {
    if (!root) return 0;
    int lh = height(root->left);
    int rh = height(root->right);
    int throughRoot = lh + rh;
    return max({throughRoot, naiveDiameter(root->left), naiveDiameter(root->right)});
}
```
**Answer:** It returns 4 (the correct answer for a 5-node path: 4 edges). And it does so correctly! But its time complexity is $O(N^2)$ because `height()` is called at every node. For the path 1→2→3→4→5: at node 1, `height(right)=4` costs O(4) calls; at node 2, `height(right)=3` costs O(3) calls; total = O(N²).

### Q4: [Extension] How would you extend this to find the actual path (not just the length)?
**Answer:** Track the two leaf nodes (or node values) that constitute the diameter. Modify `calculateHeight` to also return the deepest leaf node. When updating `maxDiameter`, also record `left.deepestLeaf` and `right.deepestLeaf`. After the traversal, reconstruct the path from left deepest leaf to right deepest leaf through the bridge node. This requires returning additional state (pair of leaf nodes), increasing code complexity but not changing time/space complexity.

### Q5: [Generalization] How does the diameter problem change for N-ary trees (each node can have multiple children)?
**Answer:** Instead of exactly 2 children, track the top-2 largest heights among all children. The diameter through node $u$ = sum of the two largest child heights. Algorithm: for each node, find the two maximum heights among all children subtrees. Update `maxDiameter` with their sum. Return `1 + maxChildHeight`. Time complexity remains $O(N)$.

### Q6: [Proof] Why is `lh + rh` at each node (in the edge-based height convention) equal to the number of edges in the path through that node?
**Answer:** `lh` = number of edges from node $u$ to the deepest leaf in the left subtree. `rh` = same for right subtree. The path goes: deepest-left-leaf → (lh edges) → node $u$ → (rh edges) → deepest-right-leaf. Total edges = `lh + rh`. This assumes `height(null) = 0` and `height(leaf) = 1` (in node-count terms, meaning the edge count from leaf to its null child = 0). The formula holds because edges are counted, not nodes.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Approach |
|---|---|---|
| 543 | Diameter of Binary Tree | Bottom-up postorder, global max |
| 124 | Binary Tree Maximum Path Sum | Same pattern but with values, allow negative subtraction |
| 687 | Longest Univalue Path | Diameter variant with value constraints |
| 1522 | Diameter of N-ary Tree | Top-2 child heights instead of left+right |

---

## 🔗 Cross-Topic Connections
- Diameter is solved using the **same postorder bottom-up pattern** as height
- **Binary Tree Maximum Path Sum (LC 124)** is "diameter with node values" — hardest tree problem in interviews
- The bridge-node concept extends to: **Lowest Common Ancestor**, **Distance between two nodes**
- Distance between nodes p and q = `depth(p) + depth(q) - 2 * depth(LCA(p,q))`

---

## ⚡ 2-Minute Revision Flash Card
- **Diameter** = longest path between any two nodes = `max(lh + rh)` over all nodes
- Path may or may NOT pass through root — check at EVERY node in postorder
- **O(N)** trick: compute height and update diameter simultaneously in one DFS pass
- **Naive O(N²)** error: calling `height()` separately at each node
- Key formula at each node: `maxDiameter = max(maxDiameter, lh + rh)`; return `1 + max(lh, rh)`
