# Lecture 104: Construct BST from Preorder Traversal (LeetCode 1008)

> **One-Line Purpose:** Construct a BST from preorder values in linear $O(N)$ time by maintaining upper bounds.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #104  
> **Video ID:** `-n5Ur1wE5Jc`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=-n5Ur1wE5Jc)  
> **Duration:** 19:10  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Reconstruct a unique BST using only its preorder traversal (Root, Left, Right).
- Avoid the naive $O(N^2)$ insertion method.
- Avoid the $O(N \log N)$ sorting method (sorting preorder gives inorder, then building from both).
- Master the $O(N)$ technique of passing an "upper bound" down the recursion tree.

## 🧠 Core Intuition — Why This Works
A preorder traversal gives us the `root` first. In a BST, everything to the left of the root must be smaller than it, and everything to the right must be larger.
Instead of searching the array for where the left elements stop and right elements begin (which takes $O(N)$ per node, leading to $O(N^2)$), we just process the array sequentially.
We keep an **upper bound**. For the left child, the upper bound is its parent's value. For the right child, the upper bound is whatever the parent's upper bound was. If the next number in the array is greater than the current bound, it doesn't belong in this subtree, and we return `nullptr`, naturally closing that branch.

**Visualization:**
```text
Preorder: [8, 5, 1, 7, 10, 12]
Bound: +∞

Root 8: Next is 5. 5 < 8, so it's the left child.
  Root 5 (bound 8): Next is 1. 1 < 5, so left child.
    Root 1 (bound 5): Next is 7. 7 > 5! So 1 has no more children. Return.
  Back to 5. Next is 7. 7 < 8, so right child of 5.
    Root 7 (bound 8): Next is 10. 10 > 8! So 7 has no more children. Return.
Back to 8. Next is 10. 10 < +∞, so right child of 8.
  Root 10 (bound +∞): Next is 12. 12 < +∞, right child of 10.
```

## 🎯 Pattern Recognition — When to Use This
**Trigger cues:**
- "Construct BST from preorder/postorder array"
- "Rebuild tree"
→ **Action:** Use a recursive bound-checking approach with a global/reference index.

## 📐 Algorithm Walk-Through
1. Initialize an index `idx = 0` (passed by reference or as a class member).
2. Create `build(preorder, bound)`:
   - **Base Case 1:** If `idx == preorder.size()`, return `nullptr`.
   - **Base Case 2:** If `preorder[idx] > bound`, the current element doesn't belong here. Return `nullptr`.
   - **Construct:** Create a new node with `preorder[idx]`. Increment `idx`.
   - **Recurse Left:** Call `build(preorder, node->val)`. The new strict upper bound is the current node's value.
   - **Recurse Right:** Call `build(preorder, bound)`. The upper bound remains whatever the parent's bound was.
3. Call `build(preorder, INT_MAX)`.

## 💻 Complete C++ Implementation

```cpp
#include <vector>
#include <climits>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionBstFromPreorder {
private:
    int idx = 0;

    TreeNode* build(const vector<int>& preorder, int bound) {
        if (idx >= preorder.size() || preorder[idx] > bound) {
            return nullptr;
        }

        TreeNode* root = new TreeNode(preorder[idx++]);
        root->left = build(preorder, root->val);
        root->right = build(preorder, bound);

        return root;
    }

public:
    TreeNode* bstFromPreorder(vector<int>& preorder) {
        idx = 0;
        return build(preorder, INT_MAX);
    }
};
```

## 🔍 Dry Run Trace
**Array:** `[8, 5, 1, 7, 10]`
- `build(bound=∞)`: `pre[0]=8`. Node(8). `idx=1`.
  - Left: `build(bound=8)`. `pre[1]=5`. Node(5). `idx=2`.
    - Left: `build(bound=5)`. `pre[2]=1`. Node(1). `idx=3`.
      - Left: `build(bound=1)`. `pre[3]=7 > 1`. Return `null`.
      - Right: `build(bound=5)`. `pre[3]=7 > 5`. Return `null`.
    - Right: `build(bound=8)`. `pre[3]=7`. Node(7). `idx=4`.
      - Left: `build(bound=7)`. `pre[4]=10 > 7`. Return `null`.
      - Right: `build(bound=8)`. `pre[4]=10 > 8`. Return `null`.
  - Right: `build(bound=∞)`. `pre[4]=10`. Node(10). `idx=5`.
    - Left: `build(bound=10)`. `idx=5` (end). Return `null`.
    - Right: `build(bound=∞)`. `idx=5` (end). Return `null`.
- Return Tree rooted at 8.

## ⚠️ Common Interview Mistakes
- **Using both a min and max bound:** For constructing from preorder, you ONLY need the upper bound (max). Because we are parsing sequentially, the lower bound is implicitly handled by the fact that if a number was smaller than the lower bound, it would have been absorbed by a left-child call earlier in the recursion stack.
- **Forgetting to increment the index:** `idx` must be a global variable or passed by reference. If passed by value, the right subtree won't know how many elements the left subtree consumed!

## 📊 Complexity Analysis
- **Time Complexity:** $O(N)$ because every element in the array is visited exactly once and creates one node.
- **Space Complexity:** $O(H)$ for the recursive call stack, where $H$ is the height of the tree. In the worst case (a skewed tree, meaning a sorted preorder array), it is $O(N)$.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: [Alternative] How would you solve this if you were given a Postorder array instead?
**Answer:** A postorder array is Left, Right, Root. The root is always at the *end* of the array. We would read the array backwards (decrementing `idx` from `size-1` to `0`). We would build the Right subtree first (passing a lower bound), then the Left subtree (passing an upper bound). 

### Q2: [Inefficient Approaches] What is the $O(N \log N)$ approach and why is it worse?
**Answer:** We know that sorting a BST's preorder traversal gives its inorder traversal. Once we have preorder and inorder arrays, we can construct the unique binary tree using the standard $O(N)$ algorithm (with a hashmap). However, the sorting step takes $O(N \log N)$ time, making it strictly worse than our $O(N)$ bound approach.

### Q3: [Why not $O(N^2)$?] What does the naive $O(N^2)$ approach look like?
**Answer:** For each root, iterating through the remaining array to find the first element larger than the root. That index splits the array into left and right subtrees. In a skewed tree, finding that split takes $O(N)$, resulting in $O(N^2)$ total time.

### Q4: [Concept] Can we construct a unique normal Binary Tree (not BST) from just a preorder traversal?
**Answer:** No. Preorder `[1, 2]` could represent a root `1` with a left child `2` OR a root `1` with a right child `2`. We need both Preorder and Inorder to construct a generic binary tree. The BST property (values dictating left/right placement) gives us the extra information needed to do it with just one traversal.

## 🏆 Related Problems (Leetcode)
- **Leetcode 106:** Construct Binary Tree from Inorder and Postorder
- **Leetcode 105:** Construct Binary Tree from Preorder and Inorder
- **Leetcode 449:** Serialize and Deserialize BST (this logic is the deserialization part)

## 🔗 Cross-Topic Connections
- **Recursion & State:** Passing the bound down and letting the `idx` increment globally is a classic example of shared state vs isolated state in recursion.

## ⚡ 2-Minute Revision Flash Card
- **Pattern:** Upper-Bound checking for BST Preorder construction.
- **Algorithm:** Global `idx`. If `val > bound`, return null. Else, make node, increment `idx`.
- **Recurse:** `left = build(root->val)`, `right = build(bound)`.
- **Time/Space:** $O(N)$ Time, $O(H)$ Space.
- **Why no lower bound?** Sequential processing guarantees we don't encounter invalid smaller values for the right subtree; they'd have been consumed already.
