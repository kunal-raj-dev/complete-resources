# Lecture 94: Binary Tree Paths (LeetCode 257)

> **One-Line Purpose:** Collect all root-to-leaf paths as formatted strings using depth-first search backtracking.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #94  
> **Video ID:** `AWJD__CfM6A`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=AWJD__CfM6A)  
> **Duration:** 10:01  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Use Depth-First Search (DFS) to explore all paths from root to leaves.
- Build and pass string states along recursive calls without global mutation.
- Identify leaf nodes correctly (nodes with both left and right children as `nullptr`).

## 🧠 Core Intuition — Why This Works
A tree path from root to a leaf node represents a single sequence of decisions (going left or right).
By using Depth-First Search (DFS), we can naturally build this path. As we visit a node, we append its value to the current path string. 
When we reach a leaf node (a node with no children), the current string is a complete path, and we add it to our results array.
If we pass the string *by value* to the recursive calls (or create a new string), the state is isolated to that specific branch. Returning to the parent automatically "backtracks" the string state, avoiding the need to manually erase the last added node.

**Visualization:**
```text
Tree:
      1
    /   \
   2     3
    \
     5

Paths:
1 -> 2 -> 5 (Leaf 5 reached, path saved)
1 -> 3 (Leaf 3 reached, path saved)
```

## 🎯 Pattern Recognition — When to Use This
**Trigger cues:**
- "Find all root-to-leaf paths"
- "Sum of root-to-leaf paths"
- "Combinations down a tree"
→ **Action:** Use Pre-order DFS traversal passing a "running state" (string, array, or sum) down the recursive calls.

## 📐 Algorithm Walk-Through
1. Initialize an empty vector of strings `paths` to store results.
2. Call a helper `dfs(root, current_path, paths)`.
3. **Base Case:** If `root` is null, just return.
4. **Action:** Append `root->val` to `current_path`.
5. **Leaf Check:** If both `root->left` and `root->right` are null:
   - We hit a leaf! Add `current_path` to `paths` and return.
6. **Recurse:** If not a leaf, append `"->"` to `current_path`.
   - Call `dfs(root->left, current_path, paths)`.
   - Call `dfs(root->right, current_path, paths)`.

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <string>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionPaths {
private:
    void dfs(TreeNode* root, string path, vector<string>& paths) {
        if (!root) return;

        path += to_string(root->val);

        // Leaf node reached
        if (!root->left && !root->right) {
            paths.push_back(path);
            return;
        }

        path += "->";
        dfs(root->left, path, paths);
        dfs(root->right, path, paths);
    }

public:
    vector<string> binaryTreePaths(TreeNode* root) {
        vector<string> paths;
        dfs(root, "", paths);
        return paths;
    }
};
```

## 🔍 Dry Run Trace
**Tree:** `[1, 2, 3, null, 5]`
- Call `dfs(1, "", paths)`
  - `path` becomes `"1"`
  - Not a leaf. `path` becomes `"1->"`.
  - Recurse Left: `dfs(2, "1->", paths)`
    - `path` becomes `"1->2"`.
    - Not a leaf. `path` becomes `"1->2->"`.
    - Recurse Left: `dfs(null, "1->2->", paths)` $\rightarrow$ returns.
    - Recurse Right: `dfs(5, "1->2->", paths)`
      - `path` becomes `"1->2->5"`.
      - Is a leaf! Add `"1->2->5"` to `paths`. Returns.
    - Returns to `dfs(1)`.
  - Recurse Right: `dfs(3, "1->", paths)`
    - `path` becomes `"1->3"`.
    - Is a leaf! Add `"1->3"` to `paths`. Returns.
- Final `paths`: `["1->2->5", "1->3"]`.

## ⚠️ Common Interview Mistakes
- **Passing the string by reference without backtracking:** If you do `void dfs(..., string& path)` (to save memory), you MUST manually erase the appended characters after the recursive calls return. Passing by value (`string path`) makes a copy for each stack frame, which is easier to write but uses more memory and time.
- **Adding "->" indiscriminately:** Adding the arrow at the end of every node instead of waiting to check if it's a leaf results in paths like `"1->2->5->"`.

## 📊 Complexity Analysis
- **Time Complexity:** $O(N)$ to visit every node. String copying at each step can make this $O(N^2)$ in the worst case (a skewed tree). In a balanced tree, it's $O(N \log N)$.
- **Space Complexity:** $O(H)$ for the recursion stack (where $H$ is the tree height). Also $O(N \log N)$ to $O(N^2)$ extra space for string copies if passing by value.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: [Optimization] How can we improve the performance of string concatenation?
**Answer:** Passing strings by value creates a lot of copies. We can pass a single `vector<int>` by reference, push the node's value, recurse, and then `pop_back()` (backtracking). When we hit a leaf, we join the vector elements into a string. This avoids intermediate string copies and is much faster.

### Q2: [Alternative Traversal] Could we use BFS (Level Order) to solve this?
**Answer:** Yes, but it requires maintaining parallel queues: one for the `TreeNode*` and one for the `string` representing the path to that node. While BFS works, DFS is generally preferred for path-building as the recursion stack naturally handles the state backtracking.

### Q3: [Variant] What if we only want paths that sum to a specific target?
**Answer:** This becomes LeetCode 113 (Path Sum II). Instead of unconditionally adding to `paths` when reaching a leaf, we would also check if `current_sum + root->val == targetSum`.

### Q4: [Edge Case] What if the tree is completely empty?
**Answer:** The initial `if (!root) return;` inside the DFS handles this. The `paths` vector remains empty, which is the correct output for an empty tree.

## 🏆 Related Problems (Leetcode)
- **Leetcode 112:** Path Sum (Check if a path exists with a sum)
- **Leetcode 113:** Path Sum II (Return all paths with a sum)
- **Leetcode 129:** Sum Root to Leaf Numbers (Treat paths as numbers and sum them)

## 🔗 Cross-Topic Connections
- **Backtracking:** This is a fundamental introduction to the concept of backtracking. Although passing by value masks it, passing by reference requires explicit "undo" operations, which is the core of backtracking algorithms.

## ⚡ 2-Minute Revision Flash Card
- **Pattern:** Depth-First Search for path-building.
- **Leaf Check:** `if (!node->left && !node->right)` is the condition for a leaf.
- **State Management:** Pass path state downward. By value = implicit backtracking (slower, easier). By reference = explicit backtracking (faster, harder).
- **Time/Space:** $O(N^2)$ worst case if string copying heavily. $O(H)$ stack space.
