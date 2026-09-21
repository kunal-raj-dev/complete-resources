# Lecture 92: Build Tree from Preorder & Inorder (LeetCode 105)

> **One-Line Purpose:** Reconstruct a unique binary tree from preorder root order and inorder boundary splitting with hash table index lookups.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #92  
> **Video ID:** `33b1M980cCA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=33b1M980cCA)  
> **Duration:** 20:59  
> **Status:** AUDITED  

---

## 🧠 Core Intuition — Why This Works

**Why can't one traversal alone reconstruct a tree?**
- Inorder alone: `[4,2,5,1,3]` — you know left/right boundaries but not which is the root!
- Preorder alone: `[1,2,4,5,3]` — you know the root but can't tell where the left subtree ends!
- Together: preorder gives you the root → find root in inorder → everything LEFT of root in inorder = left subtree; everything RIGHT = right subtree.

**The recursive decomposition:**
```
Preorder: [1, 2, 4, 5, 3]
            ↑ = root

Inorder:  [4, 2, 5, 1, 3]
                    ↑ = root at index 3
           [4,2,5] = left subtree (3 nodes)
                       [3] = right subtree (1 node)

Next root in preorder = preorder[1] = 2 (root of left subtree)
Left subtree inorder range: [4, 2, 5] → inorder[0..2]
Right subtree preorder: starts at preorder[1 + 3] = preorder[4] = 3
```

**Hash map optimization:** Finding the root's position in inorder is O(N) with linear scan → repeated for each node = O(N²). Precomputing an `unordered_map<val, index>` makes each lookup O(1) → total O(N).

---

## 🎯 Pattern Recognition — When to Use This

- "Reconstruct / build tree from traversals" → need INORDER + one of (preorder/postorder)
- "Preorder + Inorder" → preorder gives roots top-down; inorder gives subtree boundaries
- "Postorder + Inorder" → postorder gives roots bottom-up (from the end)
- "Preorder + Postorder alone" → NOT uniquely reconstructible (unless perfect binary tree)

---

## 🔵 Complete C++ Implementation

```cpp
#include <vector>
#include <unordered_map>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionBuildTree {
private:
    unordered_map<int, int> inMap;
    int preIdx = 0;

    TreeNode* construct(const vector<int>& preorder, int inStart, int inEnd) {
        if (inStart > inEnd) return nullptr;

        int rootVal = preorder[preIdx++];
        TreeNode* root = new TreeNode(rootVal);

        int rootPos = inMap[rootVal];

        root->left = construct(preorder, inStart, rootPos - 1);
        root->right = construct(preorder, rootPos + 1, inEnd);

        return root;
    }

public:
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        inMap.clear();
        preIdx = 0;
        for (int i = 0; i < inorder.size(); i++) {
            inMap[inorder[i]] = i;
        }
        return construct(preorder, 0, inorder.size() - 1);
    }
};
```
- **Time Complexity:** $O(N)$ with hash map lookups.
- **Space Complexity:** $O(N)$ map + recursion stack.

---

## 💻 Build from Postorder + Inorder

```cpp
// Symmetrically: postorder's LAST element = root; right subtree before left
class SolutionBuildFromPost {
private:
    unordered_map<int, int> inMap;
    int postIdx;

    TreeNode* construct(const vector<int>& postorder, int inStart, int inEnd) {
        if (inStart > inEnd) return nullptr;

        int rootVal = postorder[postIdx--];  // Take from END of postorder
        TreeNode* root = new TreeNode(rootVal);

        int rootPos = inMap[rootVal];

        // IMPORTANT: Build RIGHT subtree first (it comes before root in postorder from the end)
        root->right = construct(postorder, rootPos + 1, inEnd);
        root->left = construct(postorder, inStart, rootPos - 1);

        return root;
    }

public:
    TreeNode* buildTree(vector<int>& inorder, vector<int>& postorder) {
        postIdx = postorder.size() - 1;
        for (int i = 0; i < inorder.size(); i++) inMap[inorder[i]] = i;
        return construct(postorder, 0, inorder.size() - 1);
    }
};
```

---

## 🔍 Dry Run Trace

```
Preorder: [3, 9, 20, 15, 7]
Inorder:  [9, 3, 15, 20, 7]

construct(preorder, inStart=0, inEnd=4):
  rootVal = preorder[0] = 3, preIdx=1
  rootPos in inorder = 1
  left subtree: inorder[0..0] = [9]
  right subtree: inorder[2..4] = [15, 20, 7]

  left = construct(preorder, 0, 0):
    rootVal = preorder[1] = 9, preIdx=2
    rootPos = 0 (in inorder)
    left = construct(preorder, 0, -1) → null
    right = construct(preorder, 1, 0) → null
    return Node(9)

  right = construct(preorder, 2, 4):
    rootVal = preorder[2] = 20, preIdx=3
    rootPos = 3
    left = construct(preorder, 2, 2):
      rootVal = preorder[3] = 15, return Node(15)
    right = construct(preorder, 4, 4):
      rootVal = preorder[4] = 7, return Node(7)
    return Node(20) with left=15, right=7

Final tree:
       3
      / \
     9   20
        /  \
       15   7
```

---

## ⚠️ Common Interview Mistakes

1. **Building right subtree before left (for Preorder+Inorder):** Preorder gives left subtree next. Must build LEFT first to correctly advance `preIdx`. Getting this order wrong produces incorrect trees.

2. **Off-by-one in inorder boundaries:** `rootPos - 1` for left; `rootPos + 1` for right. The root itself is excluded from both sub-calls.

3. **Not using a hash map:** Linear search for root in inorder at each step = O(N²). Always precompute the map.

4. **Assuming unique values:** The algorithm requires all values to be distinct (for the hash map to work correctly). If values can repeat, the problem requires additional constraints.

5. **Forgetting to reset `preIdx` between calls:** If using a class member variable, reset `preIdx = 0` in the public method.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$ with hash map lookups.
- **Space Complexity:** $O(N)$ hash map + $O(H)$ recursion stack.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Why does Preorder + Inorder uniquely reconstruct a binary tree, but Preorder + Postorder does not?
**Answer:** Preorder tells us the root; Inorder tells us the LEFT/RIGHT boundary — everything before the root in inorder is in the left subtree, everything after is in the right subtree. This boundary is UNAMBIGUOUS.

Preorder + Postorder doesn't work because: given a root (from preorder) and postorder ending at root, you cannot determine how many elements belong to the left vs right subtree. For example, preorder `[1, 2]` and postorder `[2, 1]` could represent:
```
1          or       1
 \                 /
  2               2
```
Both have the same preorder and postorder! Exception: if you know it's a **perfect binary tree** (all leaves at same level), the split is uniquely determined.

### Q2: [Extension] How do you build the tree from Postorder + Inorder? What changes?
**Answer:** Symmetric to preorder + inorder:
1. The **last** element of postorder = root (postorder ends with root).
2. Find root in inorder → split into left/right subtrees.
3. Recursively build **right subtree FIRST** (because postorder reads right subtree before root when processed from the end).

```cpp
postIdx = postorder.size() - 1;  // Start from the end
// Build RIGHT before LEFT
root->right = construct(postorder, rootPos + 1, inEnd);
root->left  = construct(postorder, inStart, rootPos - 1);
```

### Q3: [Tricky] Why must we build the LEFT subtree before RIGHT in the Preorder+Inorder solution?
**Answer:** In preorder, after the root comes the **entire left subtree**, then the entire right subtree. The `preIdx` pointer must advance through the left subtree's nodes before reaching the right subtree's nodes. If we build right before left, `preIdx` would grab nodes meant for the left subtree for the right subtree construction, producing a wrong tree.

### Q4: [Output Prediction] What does this code do if preorder = `[1]` and inorder = `[1]`?
```cpp
construct(preorder, 0, 0):
  rootVal = preorder[0] = 1, preIdx=1
  rootPos = 0
  left = construct(preorder, 0, -1) → inStart > inEnd → nullptr
  right = construct(preorder, 1, 0) → inStart > inEnd → nullptr
  return Node(1)
```
**Answer:** Returns a single-node tree containing value 1. Correct — a single-element preorder and inorder can only represent a single node.

### Q5: [Design] How would you serialize and deserialize a binary tree using this approach?
**Answer:** Serialize: perform both preorder and inorder traversals, store both as arrays. Deserialize: use the build-tree-from-preorder-inorder algorithm. However, a more compact approach is to serialize with null markers: `"1,2,null,null,3,null,null"` using preorder. This requires only one traversal and can be deserialized from preorder alone using null markers.

### Q6: [Complexity] Why is the naive O(N²) approach a problem and when would it matter?
**Answer:** The naive approach uses `find()` on the inorder array at each recursive call — $O(N)$ per call, $O(N)$ calls total = $O(N^2)$. For $N = 10^5$ nodes, this is $10^{10}$ operations — completely infeasible. The hash map brings this to $O(1)$ per lookup, giving $O(N)$ total. The space tradeoff is $O(N)$ for the hash map vs $O(1)$ additional space, which is acceptable.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Approach |
|---|---|---|
| 105 | Construct Binary Tree from Preorder + Inorder | preIdx + hash map |
| 106 | Construct Binary Tree from Inorder + Postorder | postIdx (from end) + hash map |
| 889 | Construct Binary Tree from Preorder + Postorder | Only possible for perfect BTs with tie-breaking |
| 297 | Serialize and Deserialize Binary Tree | Preorder with null markers |

---

## 🔗 Cross-Topic Connections
- **Preorder traversal** gives the "root-first" sequence needed for reconstruction
- **Inorder traversal** divides the universe into left/right subtrees
- **BST from Preorder (Lecture 104):** No inorder needed because BST property determines boundaries
- **Tree Serialization (LC 297):** Uses preorder with null markers — single traversal suffices

---

## ⚡ 2-Minute Revision Flash Card
- **Preorder root → find in inorder → split left/right boundaries**
- **Build LEFT before RIGHT** (preorder visits left subtree first after root)
- **Hash map:** precompute `val → inorder index` for O(1) lookup → O(N) total
- **Postorder + Inorder:** same idea but postIdx starts at END; build RIGHT before LEFT
- **Preorder + Postorder alone:** NOT uniquely reconstructible (except perfect BT)
