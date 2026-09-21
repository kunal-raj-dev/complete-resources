# Lecture 90: Kth Level of a Binary Tree

> **One-Line Purpose:** Retrieve or print all nodes at depth $K$ from the root using DFS recursive depth tracking or BFS queue level batching in $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #90  
> **Video ID:** `ze4JO_ODl3w`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=ze4JO_ODl3w)  
> **Duration:** 07:59  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Understanding Tree Level indexing conventions (1-indexed where root is level 1, vs 0-indexed depth).
- Recursive DFS depth decrement pattern (`k - 1`).
- BFS Level-order queue batching comparison.
- Handling boundary conditions where $K > \text{height}$ or $K \le 0$.

---

## 🧠 Core Intuition — Why This Works
In a binary tree, to collect nodes at level $K$:
- If $K = 1$, the current node itself is at level $K$. Add `root->val` to results and do NOT recurse deeper.
- If $K > 1$, its children are at distance $K - 1$. Recurse on `root->left` and `root->right` with parameter $K - 1$.

```text
Tree:
        1         <-- Level 1 (k=1)
      /   \
     2     3       <-- Level 2 (k=2)
    / \   / \
   4   5 6   7     <-- Level 3 (k=3)
```
*Analogy:* Imagine standing on top of a building (the root). You want to take photos of everyone on the 3rd floor down. Instead of walking around randomly, you send a message to the 2nd floor: "tell the floor below you to take photos". Each floor decreases the counter until the counter is 1, meaning "this is the target floor."

## 🎯 Pattern Recognition — When to Use This
- **Trigger cues:** "nodes at depth D", "k distance from root", "level-wise output".
- **Which approach to pick:** 
  - Use **DFS** if you want to write less code and don't care about memory efficiency for very wide trees (but risk stack overflow on very deep trees).
  - Use **BFS** if you want to stop exactly at level $K$ without traversing deeper parts unnecessarily, or if the tree is exceptionally deep.

## 📐 Algorithm Walk-Through
**DFS Approach:**
1. **Base Case 1:** If the current node is `nullptr` or $K < 1$, return.
2. **Base Case 2:** If $K == 1$, we have reached the target depth. Add `root->val` to our result vector and return (no need to go deeper).
3. **Recursive Step:** Call the function on `root->left` passing $K-1$, then on `root->right` passing $K-1$.

**BFS Approach:**
1. Initialize a queue and push the `root`. Set `currentLevel = 1`.
2. While the queue is not empty, check if `currentLevel == k`. If yes, empty the queue into a result list and return.
3. Otherwise, for every node currently in the queue, pop it and push its non-null children.
4. Increment `currentLevel` and repeat.

## 💻 Complete C++ Implementation: Both DFS and BFS

```cpp
#include <iostream>
#include <vector>
#include <queue>

using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class KthLevelSolver {
public:
    // Approach 1: Recursive DFS - O(N) Time, O(H) Stack Space
    static void getKthLevelDFS(TreeNode* root, int k, vector<int>& res) {
        if (!root || k < 1) return;

        if (k == 1) {
            res.push_back(root->val);
            return;
        }

        getKthLevelDFS(root->left, k - 1, res);
        getKthLevelDFS(root->right, k - 1, res);
    }

    // Approach 2: Iterative BFS - O(N) Time, O(W) Queue Space
    static vector<int> getKthLevelBFS(TreeNode* root, int k) {
        if (!root || k < 1) return {};

        queue<TreeNode*> q;
        q.push(root);
        int currentLevel = 1;

        while (!q.empty()) {
            int size = q.size();
            if (currentLevel == k) {
                vector<int> res;
                for (int i = 0; i < size; ++i) {
                    TreeNode* node = q.front();
                    q.pop();
                    res.push_back(node->val);
                }
                return res;
            }

            for (int i = 0; i < size; ++i) {
                TreeNode* node = q.front();
                q.pop();
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
            currentLevel++;
        }

        return {}; // k exceeds tree height
    }
};

int main() {
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);
    root->right->left = new TreeNode(6);
    root->right->right = new TreeNode(7);

    vector<int> resDFS;
    KthLevelSolver::getKthLevelDFS(root, 3, resDFS);
    cout << "Kth Level (k=3) via DFS: ";
    for (int x : resDFS) cout << x << " "; // Output: 4 5 6 7
    cout << endl;

    vector<int> resBFS = KthLevelSolver::getKthLevelBFS(root, 3);
    cout << "Kth Level (k=3) via BFS: ";
    for (int x : resBFS) cout << x << " "; // Output: 4 5 6 7
    cout << endl;
    return 0;
}
```

## 🔍 Dry Run Trace
Let's trace `getKthLevelDFS(root, 3, res)` for the tree in the intuition section:
- `getKthLevelDFS(Node(1), 3)`
  - $K \neq 1$, recurse left: `getKthLevelDFS(Node(2), 2)`
    - $K \neq 1$, recurse left: `getKthLevelDFS(Node(4), 1)`
      - $K == 1$. Add `4` to `res`. Return.
    - recurse right: `getKthLevelDFS(Node(5), 1)`
      - $K == 1$. Add `5` to `res`. Return.
  - recurse right: `getKthLevelDFS(Node(3), 2)`
    - recurse left: `getKthLevelDFS(Node(6), 1)` $\rightarrow$ Adds `6`.
    - recurse right: `getKthLevelDFS(Node(7), 1)` $\rightarrow$ Adds `7`.
- Result: `[4, 5, 6, 7]`

## ⚠️ Common Pitfalls & Corner Cases
1. **$K > \text{height}$:** The recursive function terminates naturally when reaching null pointers; ensure returning an empty list rather than throwing null pointer exceptions.
2. **Left-to-Right Ordering:** Recursing `root->left` before `root->right` preserves standard left-to-right node ordering.
3. **Index Base:** Always clarify with the interviewer if the root is considered level 0 or level 1. If it's level 0, the target comparison changes to `k == 0` and the initial BFS level is `0`.

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$ worst-case to traverse to level $K$. In the best case (BFS where K is small), it visits only the nodes up to level K.
- **Space Complexity:** $O(H)$ recursion stack depth in DFS, or $O(W)$ width in BFS (where $W \le N/2$ in a balanced binary tree).

## 🔥 Interview Q&A
### Q1: Can we find the Kth level from the bottom?
Yes. You first need to find the height $H$ of the tree in $O(N)$ time. Then, the $K$th level from the bottom is simply the $(H - K + 1)$th level from the top (assuming 1-indexed levels). Then apply the same algorithm. Total time remains $O(N)$.

### Q2: Why might BFS be preferable to DFS for this specific problem?
If $K$ is very small but the tree is extremely deep (e.g., $K=2$ but height is $10^5$), BFS will stop as soon as it processes the 2nd level. DFS, while also pruned when $K=1$, still processes the left subtree before the right subtree, meaning it's theoretically equivalent in optimal pruning, but BFS is often more intuitive for "level" related early-stopping and guarantees no stack overflow. BFS guarantees memory usage is only proportional to the width of the levels up to $K$, which might be much smaller than the height of the tree.

### Q3: What if we wanted nodes at distance K from a *target* node, not the root?
This becomes the "All Nodes Distance K in Binary Tree" problem. You would need to either: 1) Convert the tree to an undirected graph using parent pointers and do a BFS from the target, or 2) Recursively find the distance from the root to the target, and for ancestors, look into their other subtrees at distance `K - dist`.

### Q4: How would you handle printing a massive tree's $K$th level where the result doesn't fit in memory?
Instead of storing in a `vector<int>`, you could stream the results directly (e.g., `cout << root->val` or writing to a file or network socket) during the `k == 1` base case in the DFS, achieving $O(1)$ auxiliary space beyond the recursion stack.

### Q5: Is it possible to solve this in $O(1)$ space (ignoring the output array)?
Yes, using a modified Morris Traversal. You can track the current depth by observing changes in the threads, but it is highly complex and impractical for interviews. Standard DFS ($O(H)$) is generally considered the optimal accepted space complexity.

## 🏆 Related Problems
- **Leetcode 199. Binary Tree Right Side View:** Uses the same depth tracking, but you only keep the last node at each level.
- **Leetcode 863. All Nodes Distance K in Binary Tree:** A generalized, much harder version of this problem starting from any target node.
- **Leetcode 102. Binary Tree Level Order Traversal:** Collects *all* levels, not just the $K$th one.

## 🔗 Cross-Topic Connections
- **Graph BFS:** A binary tree is just a directed acyclic graph where each node has max out-degree of 2. Finding nodes at level $K$ is identical to finding vertices at distance $K$ from the source in an unweighted graph.
- **Recursion & Backtracking:** The DFS approach perfectly models passing state down the recursion tree (the remaining distance $K$).

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Get all nodes exactly $K$ edges/levels away from root.
- **DFS Approach:** Pass $K$ down. If `K == 1`, add node and return. Else recurse left and right with $K-1$.
- **BFS Approach:** Queue-based level order. Loop until `currentLevel == K`, then dump the queue.
- **Time Complexity:** $O(N)$ (but stops early at target depth).
- **Space:** $O(H)$ for DFS stack, $O(W)$ for BFS queue.
- **Trap:** Clarify 0-indexed vs 1-indexed levels.
